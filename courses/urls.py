from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("<slug:slug>/lecciones/<int:pk>/", views.lesson_detail, name="lesson_detail"),
    path("<slug:slug>/", views.course_detail, name="course_detail"),
]
