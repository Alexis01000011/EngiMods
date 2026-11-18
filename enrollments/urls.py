from django.urls import path

from . import views

app_name = "enrollments"

urlpatterns = [
    path("", views.my_courses, name="my_courses"),
    path("lecciones/<int:pk>/completada/", views.toggle_lesson, name="toggle_lesson"),
    path("laboratorio/<slug:game_slug>/", views.lab_guide, name="lab_guide"),
    path(
        "laboratorio/<slug:game_slug>/pasos/<int:step_pk>/hecho/",
        views.toggle_lab_step,
        name="toggle_lab_step",
    ),
]
