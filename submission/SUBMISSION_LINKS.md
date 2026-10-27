# Final Project Deliverables

**Repository:** Not published. GitHub CLI is present, but its saved token for `ashmitpro-design` is invalid. Re-authenticate with `gh auth refresh -h github.com`, then publish the local repository as `django-online-course-final-project`.

The local source links below are ready for review. GitHub URLs are omitted until a push can be verified.

| Task | Marks | Deliverable | Local path / status |
|---|---:|---|---|
| 1 | 3 | Assessment models | [onlinecourse/models.py](../onlinecourse/models.py) |
| 2 | 3 | Admin classes and inlines | [onlinecourse/admin.py](../onlinecourse/admin.py) |
| 3 | 1 | Admin screenshot | Not captured: desktop browser automation was stopped before the admin page loaded. Expected path: `submission/screenshots/03-admin-site.png`. |
| 4 | 2 | Course detail template | [course_details_bootstrap.html](../onlinecourse/templates/onlinecourse/course_details_bootstrap.html) |
| 5 | 2 | Submission and result views | [onlinecourse/views.py](../onlinecourse/views.py) |
| 6 | 2 | Application routes | [onlinecourse/urls.py](../onlinecourse/urls.py) |
| 7 | 2 | Successful exam screenshot | Not captured: desktop browser automation was stopped before the result page could be displayed. Expected path: `submission/screenshots/07-final.png`. |

## Local demo

Install dependencies, apply migrations, and run `python manage.py seed_demo`. The demo learner is `demo_learner` with local-only password `DemoLearner-2026`. Sign in at `/accounts/login/`, open the course, choose the correct answer for each question, and submit.

The successful attempt was submitted through Django's CSRF-enforcing test client and its result page returned HTTP 200 with “Congratulations!”. The local test suite has 6 passing tests. The GitHub URLs and both screenshot artifacts remain outstanding.
