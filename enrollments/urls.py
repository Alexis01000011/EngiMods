from django.urls import path

from . import views

app_name = "enrollments"

urlpatterns = [
    path("", views.my_courses, name="my_courses"),
]
