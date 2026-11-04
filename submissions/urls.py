from django.urls import path

from . import views

app_name = "submissions"

urlpatterns = [
    path("", views.my_submissions, name="my_submissions"),
    path("lecciones/<int:lesson_pk>/", views.submit, name="submit"),
]
