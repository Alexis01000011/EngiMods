from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.game_list, name="game_list"),
    path("<slug:slug>/", views.game_detail, name="game_detail"),
]
