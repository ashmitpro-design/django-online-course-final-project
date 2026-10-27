# Django Online Course Final Project

A Django app for browsing courses, lessons, and questions; enrolled learners can submit an exam and receive question-by-question results. Scores are calculated from the stored choices, with a 70% passing threshold.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the course list and `/admin/` for administration. `seed_demo` creates the sample learner `demo_learner` with the local-only password `DemoLearner-2026`. Change it before using the app beyond local demonstration. The command creates a sample course with two lessons and four choices per assessment question.

For deployment, set `DJANGO_SECRET_KEY` through the hosting environment and configure `DEBUG` and `ALLOWED_HOSTS` for that environment. The checked-in fallback secret is for local development only.

To try the assessment, sign in at `/accounts/login/` as `demo_learner`, open the sample course, and submit answers. The test suite covers submission and result behavior.

## Validation

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py test
```

The sample database is local and excluded from version control. See `submission/SUBMISSION_LINKS.md` for assignment deliverables.
