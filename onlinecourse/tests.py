from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .admin import ChoiceInline, LessonAdmin, QuestionAdmin, QuestionInline
from .models import Choice, Course, Enrollment, Learner, Lesson, Question, Submission


class AssessmentFlowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="learner", password="safe-test-password")
        self.learner = Learner.objects.create(user=self.user)
        self.course = Course.objects.create(name="Test course", description="Test description")
        self.enrollment = Enrollment.objects.create(learner=self.learner, course=self.course)
        self.lesson = Lesson.objects.create(course=self.course, title="Lesson", content="Text")
        self.q1 = Question.objects.create(lesson=self.lesson, question_text="One?", grade=2)
        self.correct1 = Choice.objects.create(question=self.q1, choice_text="Right", is_correct=True)
        self.wrong1 = Choice.objects.create(question=self.q1, choice_text="Wrong", is_correct=False)
        self.q2 = Question.objects.create(lesson=self.lesson, question_text="Two?", grade=1)
        self.correct2 = Choice.objects.create(question=self.q2, choice_text="Yes", is_correct=True)
        self.wrong2 = Choice.objects.create(question=self.q2, choice_text="No", is_correct=False)

    def test_submit_scores_and_persists_correct_answers(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("onlinecourse:submit", args=(self.course.id,)), {
            f"question_{self.q1.id}": self.correct1.id,
            f"question_{self.q2.id}": self.correct2.id,
        })
        self.assertEqual(response.status_code, 302)
        submission = Submission.objects.get()
        self.assertEqual((submission.score, submission.total_points, submission.passed), (3, 3, True))
        self.assertRedirects(response, reverse("onlinecourse:show_exam_result_attempt", args=(self.course.id, submission.id)))
        result = self.client.get(response.url)
        self.assertContains(result, "Congratulations!")
        self.assertContains(result, "Right")

    def test_incorrect_and_missing_answers_do_not_score(self):
        self.client.force_login(self.user)
        self.client.post(reverse("onlinecourse:submit", args=(self.course.id,)), {f"question_{self.q1.id}": self.wrong1.id})
        submission = Submission.objects.get()
        self.assertEqual((submission.score, submission.total_points, submission.passed), (0, 3, False))

    def test_rejects_unrelated_choice_and_unenrolled_user(self):
        other_lesson = Lesson.objects.create(course=Course.objects.create(name="Other", description=""), title="Other")
        other_question = Question.objects.create(lesson=other_lesson, question_text="Other?")
        other_choice = Choice.objects.create(question=other_question, choice_text="No")
        self.client.force_login(self.user)
        response = self.client.post(reverse("onlinecourse:submit", args=(self.course.id,)), {f"question_{self.q1.id}": other_choice.id})
        self.assertEqual(response.status_code, 400)
        user2 = get_user_model().objects.create_user(username="outsider", password="password")
        self.client.force_login(user2)
        self.assertEqual(self.client.post(reverse("onlinecourse:submit", args=(self.course.id,))).status_code, 400)

    def test_submission_results_are_private(self):
        submission = Submission.objects.create(enrollment=self.enrollment)
        submission.choices.add(self.correct1)
        user2 = get_user_model().objects.create_user(username="another", password="password")
        Learner.objects.create(user=user2)
        self.client.force_login(user2)
        self.assertEqual(self.client.get(reverse("onlinecourse:show_exam_result_attempt", args=(self.course.id, submission.id))).status_code, 404)

    def test_course_page_contains_lessons_questions_and_csrf(self):
        response = self.client.get(reverse("onlinecourse:course_details", args=(self.course.id,)))
        self.assertContains(response, "Lesson")
        self.assertContains(response, "One?")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_exam_post_requires_csrf_token(self):
        client = self.client_class(enforce_csrf_checks=True)
        client.force_login(self.user)
        response = client.post(reverse("onlinecourse:submit", args=(self.course.id,)), {
            f"question_{self.q1.id}": self.correct1.id,
        })
        self.assertEqual(response.status_code, 403)

    def test_admin_inline_configuration(self):
        self.assertEqual(QuestionAdmin.inlines, (ChoiceInline,))
        self.assertEqual(LessonAdmin.inlines, (QuestionInline,))
