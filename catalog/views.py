from django.shortcuts import get_object_or_404, render

from .models import Game


def game_list(request):
    games = Game.objects.filter(status=Game.Status.ACTIVE)
    return render(request, "catalog/game_list.html", {"games": games})


def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug, status=Game.Status.ACTIVE)
    return render(request, "catalog/game_detail.html", {"game": game})
