from django.urls import path

from . import tutor_views

app_name = "revalidation"

urlpatterns = [
    path("", tutor_views.queue, name="queue"),
    path("<int:pk>/", tutor_views.revalidate, name="revalidate"),
]
