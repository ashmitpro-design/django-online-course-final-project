# Final Project Deliverables

**Repository:** Publication in progress for `ashmitpro-design/django-online-course-final-project`. Public URLs will be recorded after the push is verified.

| Task | Marks | Deliverable | Local file | Public GitHub URL |
|---|---:|---|---|---|
| 1 | 3 | Assessment models | [models.py](../onlinecourse/models.py) | Pending publication |
| 2 | 3 | Admin classes and inlines | [admin.py](../onlinecourse/admin.py) | Pending publication |
| 3 | 1 | Admin screenshot | [03-admin-site.png](screenshots/03-admin-site.png) | Pending publication |
| 4 | 2 | Course detail template | [course_details_bootstrap.html](../onlinecourse/templates/onlinecourse/course_details_bootstrap.html) | Pending publication |
| 5 | 2 | Submission and result views | [views.py](../onlinecourse/views.py) | Pending publication |
| 6 | 2 | Application routes | [urls.py](../onlinecourse/urls.py) | Pending publication |
| 7 | 2 | Successful exam screenshot | [07-final.png](screenshots/07-final.png) | Pending publication |

## Local demo

Install dependencies, apply migrations, and run `python manage.py seed_demo`. The demo learner is `demo_learner` with local-only password `DemoLearner-2026`. Sign in at `/accounts/login/`, open the sample course, choose the correct answers, and submit.

The result screenshot is from a real browser session after the learner submitted both correct answers. The result page showed **2 / 2 points**, **Passed**, and **Congratulations!**. The local test suite has 7 passing tests. Public file URLs will be recorded after the repository push is verified.
