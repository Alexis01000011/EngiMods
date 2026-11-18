"""Perfil del alumno (EM-032)."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from catalog.models import Game

pytestmark = pytest.mark.django_db


@pytest.fixture
def games():
    first = Game.objects.create(
        name="Juego uno",
        slug="juego-uno",
        description="Uno.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )
    second = Game.objects.create(
        name="Juego dos",
        slug="juego-dos",
        description="Dos.",
        official_url="https://example.com/",
        status=Game.Status.ACTIVE,
    )
    hidden = Game.objects.create(
        name="Juego oculto",
        slug="juego-oculto",
        description="Oculto.",
        official_url="https://example.com/",
        status=Game.Status.HIDDEN,
    )
    return first, second, hidden


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        email="alumno@example.com",
        password="x-12345678",
        display_name="Alumno",
    )


def test_sin_sesion_redirige_al_inicio_de_sesion(client):
    response = client.get(reverse("accounts:profile"))

    assert response.status_code == 302
    assert response.url.startswith(reverse("accounts:login"))


def test_muestra_el_perfil_actual_y_solo_los_juegos_visibles(client, user, games):
    first, _second, hidden = games
    user.discord_username = "alumno#1234"
    user.github_username = "alumno-gh"
    user.save()
    user.interested_games.add(first)
    client.force_login(user)

    html = client.get(reverse("accounts:profile")).content.decode()

    assert "Alumno" in html
    assert "alumno#1234" in html
    assert "alumno-gh" in html
    assert "Juego uno" in html
    assert "Juego oculto" not in html


def test_guardar_actualiza_los_datos_y_los_juegos(client, user, games):
    first, second, _hidden = games
    client.force_login(user)

    response = client.post(
        reverse("accounts:profile"),
        {
            "display_name": "Alumno nuevo",
            "discord_username": "alumno-nuevo",
            "github_username": "alumno-nuevo-gh",
            "interested_games": [first.pk, second.pk],
        },
    )

    assert response.status_code == 302
    user.refresh_from_db()
    assert user.display_name == "Alumno nuevo"
    assert user.discord_username == "alumno-nuevo"
    assert user.github_username == "alumno-nuevo-gh"
    assert set(user.interested_games.values_list("pk", flat=True)) == {first.pk, second.pk}


def test_los_datos_opcionales_se_pueden_dejar_vacios(client, user, games):
    first, _second, _hidden = games
    user.discord_username = "algo"
    user.github_username = "algo-gh"
    user.save()
    user.interested_games.add(first)
    client.force_login(user)

    response = client.post(
        reverse("accounts:profile"),
        {
            "display_name": "Alumno",
            "discord_username": "",
            "github_username": "",
        },
    )

    assert response.status_code == 302
    user.refresh_from_db()
    assert user.discord_username == ""
    assert user.github_username == ""
    assert not user.interested_games.exists()


def test_no_acepta_un_juego_oculto(client, user, games):
    _first, _second, hidden = games
    client.force_login(user)

    response = client.post(
        reverse("accounts:profile"),
        {
            "display_name": "Alumno",
            "discord_username": "",
            "github_username": "",
            "interested_games": [hidden.pk],
        },
    )

    assert response.status_code == 200
    assert not user.interested_games.exists()


def test_no_edita_el_perfil_de_otra_persona(client, user, games):
    other = get_user_model().objects.create_user(
        email="otra@example.com",
        password="x-12345678",
        display_name="Otra persona",
    )
    client.force_login(user)

    client.post(
        reverse("accounts:profile"),
        {
            "display_name": "Alumno",
            "discord_username": "",
            "github_username": "",
            "user": other.pk,
        },
    )

    other.refresh_from_db()
    assert other.display_name == "Otra persona"
