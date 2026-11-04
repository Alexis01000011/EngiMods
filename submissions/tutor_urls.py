from django.urls import path

from . import tutor_views

app_name = "reviews"

urlpatterns = [
    path("", tutor_views.queue, name="queue"),
    path("<int:pk>/", tutor_views.review, name="review"),
    path("<int:pk>/tomar/", tutor_views.start_review, name="start_review"),
]
