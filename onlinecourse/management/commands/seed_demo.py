from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from onlinecourse.models import Choice, Course, Enrollment, Learner, Lesson, Question


class Command(BaseCommand):
    help = "Create a repeatable sample course, learner, and assessed exam."

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(username="demo_learner", defaults={"email": "learner@example.test"})
        if created:
            user.set_password("DemoLearner-2026")
            user.save()
        learner, _ = Learner.objects.get_or_create(user=user)
        course, _ = Course.objects.get_or_create(name="Foundations of Web Development", defaults={"description": "Learn how the web works, from HTML and CSS to HTTP and accessible design."})
        lessons = [
            ("HTML and the Web", "Explore semantic HTML and how browsers render web pages."),
            ("HTTP and Accessibility", "Understand HTTP requests and build accessible interfaces."),
        ]
        for title, content in lessons:
            lesson, _ = Lesson.objects.get_or_create(course=course, title=title, defaults={"content": content})
            question_text = "Which language structures the content of a web page?" if title.startswith("HTML") else "Which HTTP method is commonly used to retrieve a resource?"
            question, _ = Question.objects.get_or_create(lesson=lesson, question_text=question_text, defaults={"grade": 1})
            choices = (["HTML", "CSS", "SQL", "Bash"] if title.startswith("HTML") else ["GET", "PATCH", "TRACE", "CONNECT"])
            correct = choices[0]
            for answer in choices:
                Choice.objects.get_or_create(question=question, choice_text=answer, defaults={"is_correct": answer == correct})
            Choice.objects.filter(question=question, choice_text=correct).update(is_correct=True)
        Enrollment.objects.get_or_create(learner=learner, course=course)
        self.stdout.write(self.style.SUCCESS(f"Demo course ready; learner username: {user.username}"))
