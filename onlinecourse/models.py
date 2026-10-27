from django.conf import settings
from django.db import models


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.get_username()


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interests = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.get_username()


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructors = models.ManyToManyField(Instructor, related_name="courses", blank=True)
    learners = models.ManyToManyField(Learner, through="Enrollment", related_name="courses", blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("learner", "course"), name="unique_course_enrollment")]

    def __str__(self):
        return f"{self.learner} — {self.course}"


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    grade = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.question_text[:80]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text[:80]


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="submissions")
    choices = models.ManyToManyField(Choice, related_name="submissions", blank=True)
    score = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.enrollment} — {self.submitted_at:%Y-%m-%d %H:%M}"

    def evaluate(self, passing_percent=70):
        questions = Question.objects.filter(lesson__course=self.enrollment.course).prefetch_related("choices")
        self.total_points = sum(q.grade for q in questions)
        self.score = sum(q.grade for q in questions if self.choices.filter(question=q, is_correct=True).count() == 1)
        self.passed = bool(self.total_points) and self.score * 100 >= self.total_points * passing_percent
        self.save(update_fields=("score", "total_points", "passed"))
        return self.score
