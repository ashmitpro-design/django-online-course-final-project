from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Choice, Course, Enrollment, Question, Submission


def course_list(request):
    return render(request, "onlinecourse/course_list.html", {"courses": Course.objects.all()})


def course_details(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related("lessons__questions__choices"), pk=course_id)
    enrolled = request.user.is_authenticated and Enrollment.objects.filter(learner__user=request.user, course=course).exists()
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course, "enrolled": enrolled})


@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(learner__user=request.user, course=course).first()
    if enrollment is None:
        return HttpResponseBadRequest("You must be enrolled in this course to take the exam.")

    questions = Question.objects.filter(lesson__course=course)
    question_ids = set(questions.values_list("id", flat=True))
    selected = []
    for key, value in request.POST.items():
        if not key.startswith("question_"):
            continue
        try:
            question_id = int(key.removeprefix("question_"))
            choice_id = int(value)
        except (TypeError, ValueError):
            return HttpResponseBadRequest("Invalid exam answer.")
        if question_id not in question_ids:
            return HttpResponseBadRequest("Answer is not part of this course exam.")
        choice = Choice.objects.filter(pk=choice_id, question_id=question_id).first()
        if choice is None:
            return HttpResponseBadRequest("Answer is not a choice for this question.")
        selected.append(choice)

    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(selected)
    submission.evaluate()
    return redirect("onlinecourse:show_exam_result_attempt", course_id=course.id, submission_id=submission.id)


@login_required
def show_exam_result(request, course_id, submission_id=None):
    course = get_object_or_404(Course, pk=course_id)
    submissions = Submission.objects.filter(enrollment__course=course, enrollment__learner__user=request.user)
    submission = get_object_or_404(submissions, pk=submission_id) if submission_id else get_object_or_404(submissions.order_by("-submitted_at"))
    questions = Question.objects.filter(lesson__course=course).prefetch_related("choices")
    answers = []
    selected_ids = set(submission.choices.values_list("id", flat=True))
    for question in questions:
        choices = list(question.choices.all())
        correct = [choice for choice in choices if choice.is_correct]
        selected = [choice for choice in choices if choice.id in selected_ids]
        answers.append({"question": question, "choices": choices, "correct": correct, "selected": selected,
                        "is_correct": len(selected) == 1 and len(correct) == 1 and selected[0].id == correct[0].id})
    return render(request, "onlinecourse/exam_result.html", {"course": course, "submission": submission, "answers": answers})
