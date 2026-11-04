from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.urls import reverse

from catalog.models import Game, GameVersion, ModdingEnvironment

pytestmark = pytest.mark.django_db


@pytest.fixture
def game():
    return Game.objects.create(
        name="Juego de prueba",
        slug="juego",
        description="Descripción.",
        official_url="https://example.com/",
    )


@pytest.fixture
def other_game():
    return Game.objects.create(
        name="Otro juego",
        slug="otro",
        description="Descripción.",
        official_url="https://example.org/",
    )


@pytest.fixture
def version(game):
    return GameVersion.objects.create(
        game=game, number="edición-alfa", release_date=date(2026, 10, 1), is_current=True
    )


@pytest.fixture
def environment(game):
    return ModdingEnvironment.objects.create(
        game=game, name="Herramienta de prueba", version="beta"
    )


def test_version_admite_identificadores_no_semver_y_guarda_fecha(version):
    version.full_clean()
    assert version.number == "edición-alfa"
    assert version.release_date == date(2026, 10, 1)
    assert str(version) == "Juego de prueba edición-alfa"


def test_solo_una_version_actual_por_juego_en_base_de_datos(game, version, other_game):
    with transaction.atomic(), pytest.raises(IntegrityError):
        GameVersion.objects.create(
            game=game, number="otra", release_date=date(2026, 11, 1), is_current=True
        )
    other = GameVersion.objects.create(
        game=other_game, number="otra", release_date=date(2026, 11, 1), is_current=True
    )
    assert other.is_current
    assert GameVersion.objects.filter(game=game, is_current=True).get() == version


def test_se_puede_cambiar_la_version_actual(game, version):
    version.is_current = False
    version.save()
    current = GameVersion.objects.create(
        game=game, number="nueva", release_date=date(2026, 11, 1), is_current=True
    )
    assert GameVersion.objects.get(game=game, is_current=True) == current


def test_numero_de_version_unico_dentro_del_juego(game, version, other_game):
    with transaction.atomic(), pytest.raises(IntegrityError):
        GameVersion.objects.create(
            game=game, number=version.number, release_date=version.release_date
        )
    GameVersion.objects.create(
        game=other_game, number=version.number, release_date=version.release_date
    )


def test_entorno_con_nombre_version_y_varias_compatibilidades(environment, version, game):
    older = GameVersion.objects.create(game=game, number="previa", release_date=date(2026, 9, 1))
    environment.compatible_versions.add(version, older)
    assert set(environment.compatible_versions.all()) == {version, older}
    assert str(environment) == "Juego de prueba: Herramienta de prueba beta"
    environment.full_clean()


def test_identidad_del_entorno_es_unica_por_juego(environment, other_game):
    with transaction.atomic(), pytest.raises(IntegrityError):
        ModdingEnvironment.objects.create(
            game=environment.game, name=environment.name, version=environment.version
        )
    ModdingEnvironment.objects.create(
        game=other_game, name=environment.name, version=environment.version
    )


@pytest.mark.parametrize("reverse_relation", [False, True])
def test_compatibilidad_rechaza_otro_juego_en_ambos_sentidos(
    environment, other_game, reverse_relation
):
    other_version = GameVersion.objects.create(
        game=other_game, number="1", release_date=date(2026, 10, 1)
    )
    with pytest.raises(ValidationError), transaction.atomic():
        if reverse_relation:
            other_version.modding_environments.add(environment)
        else:
            environment.compatible_versions.add(other_version)
    assert not environment.compatible_versions.exists()


@pytest.mark.parametrize("change_version", [False, True])
def test_validacion_impide_mover_una_compatibilidad_a_otro_juego(
    environment, version, other_game, change_version
):
    environment.compatible_versions.add(version)
    instance = version if change_version else environment
    instance.game = other_game
    with pytest.raises(ValidationError) as error:
        instance.full_clean()
    assert "game" in error.value.message_dict


def test_admin_crea_version_y_entorno_con_compatibilidad(admin_client, game):
    response = admin_client.post(
        reverse("admin:catalog_gameversion_add"),
        {
            "game": game.pk,
            "number": "release-2026",
            "release_date": "2026-11-01",
            "is_current": "on",
        },
    )
    assert response.status_code == 302
    version = GameVersion.objects.get(game=game)
    response = admin_client.post(
        reverse("admin:catalog_moddingenvironment_add"),
        {
            "game": game.pk,
            "name": "SDK de prueba",
            "version": "2026.11",
            "compatible_versions": [version.pk],
        },
    )
    assert response.status_code == 302
    assert ModdingEnvironment.objects.get().compatible_versions.get() == version


def test_admin_muestra_error_si_ya_hay_version_actual(admin_client, version):
    response = admin_client.post(
        reverse("admin:catalog_gameversion_add"),
        {
            "game": version.game_id,
            "number": "otra",
            "release_date": "2026-11-01",
            "is_current": "on",
        },
    )
    assert response.status_code == 200
    assert "Este juego ya tiene una versión actual." in response.content.decode()
    assert GameVersion.objects.count() == 1


def test_admin_rechaza_compatibilidad_de_otro_juego_sin_error_500(
    admin_client, version, other_game
):
    response = admin_client.post(
        reverse("admin:catalog_moddingenvironment_add"),
        {"game": other_game.pk, "name": "SDK", "version": "1", "compatible_versions": [version.pk]},
    )
    assert response.status_code == 200
    assert "compatible_versions" in response.context["adminform"].form.errors
    assert not ModdingEnvironment.objects.exists()


@pytest.mark.parametrize("model", [GameVersion, ModdingEnvironment])
def test_admin_filtra_por_juego(admin_client, model, version, environment, other_game):
    url = reverse(f"admin:catalog_{model._meta.model_name}_changelist")
    response = admin_client.get(url, {"game__id__exact": other_game.pk})
    assert response.status_code == 200
    assert not response.context["cl"].queryset.exists()
    response = admin_client.get(url, {"game__id__exact": version.game_id})
    expected = version if model is GameVersion else environment
    assert list(response.context["cl"].queryset) == [expected]


@pytest.mark.parametrize("model", [GameVersion, ModdingEnvironment])
@pytest.mark.parametrize("role", ["anonimo", "alumno", "tutor", "personal_sin_permiso"])
def test_sin_permiso_no_puede_administrar_catalogo(client, model, role):
    if role != "anonimo":
        user = get_user_model().objects.create_user(
            email=f"{role}@example.com",
            display_name=role,
            is_tutor=role == "tutor",
            is_staff=role == "personal_sin_permiso",
        )
        client.force_login(user)
    response = client.post(reverse(f"admin:catalog_{model._meta.model_name}_add"), {})
    assert response.status_code == (403 if role == "personal_sin_permiso" else 302)
    assert not model.objects.exists()
