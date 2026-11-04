from django.urls import path

from . import views

app_name = "enrollments"

urlpatterns = [
    path("", views.my_courses, name="my_courses"),
    path("lecciones/<int:pk>/completada/", views.toggle_lesson, name="toggle_lesson"),
]
