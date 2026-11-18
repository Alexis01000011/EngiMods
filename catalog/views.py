from django.shortcuts import get_object_or_404, render

from courses.models import Course

from .models import Game


def game_list(request):
    games = Game.objects.filter(status=Game.Status.ACTIVE)
    return render(request, "catalog/game_list.html", {"games": games})


def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug, status=Game.Status.ACTIVE)
    # Solo los cursos publicados del juego; los borradores no salen en público.
    courses = list(Course.objects.published().filter(game=game).order_by("title", "pk"))
    return render(
        request,
        "catalog/game_detail.html",
        {"game": game, "courses": courses, "has_courses": bool(courses)},
    )
