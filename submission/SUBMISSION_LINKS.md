# Final Project Deliverables

**Repository:** [ashmitpro-design/django-online-course-final-project](https://github.com/ashmitpro-design/django-online-course-final-project)

| Task | Marks | Deliverable | Local file | Public GitHub URL |
|---|---:|---|---|---|
| 1 | 3 | Assessment models | [models.py](../onlinecourse/models.py) | [GitHub](https://github.com/ashmitpro-design/django-online-course-final-project/blob/main/onlinecourse/models.py) |
| 2 | 3 | Admin classes and inlines | [admin.py](../onlinecourse/admin.py) | [GitHub](https://github.com/ashmitpro-design/django-online-course-final-project/blob/main/onlinecourse/admin.py) |
| 3 | 1 | Admin screenshot | [03-admin-site.png](screenshots/03-admin-site.png) | [GitHub](https://github.com/ashmitpro-design/django-online-course-final-project/blob/main/submission/screenshots/03-admin-site.png) |
| 4 | 2 | Course detail template | [course_details_bootstrap.html](../onlinecourse/templates/onlinecourse/course_details_bootstrap.html) | [GitHub](https://github.com/ashmitpro-design/django-online-course-final-project/blob/main/onlinecourse/templates/onlinecourse/course_details_bootstrap.html) |
| 5 | 2 | Submission and result views | [views.py](../onlinecourse/views.py) | [GitHub](https://github.com/ashmitpro-design/django-online-course-final-project/blob/main/onlinecourse/views.py) |
| 6 | 2 | Application routes | [urls.py](../onlinecourse/urls.py) | [GitHub](https://github.com/ashmitpro-design/django-online-course-final-project/blob/main/onlinecourse/urls.py) |
| 7 | 2 | Successful exam screenshot | [07-final.png](screenshots/07-final.png) | [GitHub](https://github.com/ashmitpro-design/django-online-course-final-project/blob/main/submission/screenshots/07-final.png) |

## Local demo

Install dependencies, apply migrations, and run `python manage.py seed_demo`. The demo learner is `demo_learner` with local-only password `DemoLearner-2026`. Sign in at `/accounts/login/`, open the sample course, choose the correct answers, and submit.

The result screenshot is from a real browser session after the learner submitted both correct answers. The result page showed **2 / 2 points**, **Passed**, and **Congratulations!**. The local test suite has 7 passing tests.
