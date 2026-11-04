import importlib

from django.conf import settings
from django.views.debug import SafeExceptionReporterFilter

import config.settings

STRIPE_SETTINGS = ("STRIPE_SECRET_KEY", "STRIPE_PUBLISHABLE_KEY", "STRIPE_WEBHOOK_SECRET")


def _reload_settings():
    return importlib.reload(config.settings)


def test_las_llaves_de_stripe_se_leen_de_variables_de_entorno(monkeypatch):
    # Valores falsos y cortos a propósito: el pre-commit bloquea lo que parece una llave real.
    monkeypatch.setenv("STRIPE_SECRET_KEY", "secreta-de-prueba")
    monkeypatch.setenv("STRIPE_PUBLISHABLE_KEY", "publicable-de-prueba")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "webhook-de-prueba")
    try:
        module = _reload_settings()
        assert module.STRIPE_SECRET_KEY == "secreta-de-prueba"
        assert module.STRIPE_PUBLISHABLE_KEY == "publicable-de-prueba"
        assert module.STRIPE_WEBHOOK_SECRET == "webhook-de-prueba"
    finally:
        monkeypatch.undo()
        _reload_settings()


def test_sin_variables_el_proyecto_arranca_con_llaves_vacias(monkeypatch):
    for name in STRIPE_SETTINGS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr("environ.Env.read_env", lambda *args, **kwargs: None)
    monkeypatch.setenv("SECRET_KEY", "solo-para-pruebas")
    try:
        module = _reload_settings()
        for name in STRIPE_SETTINGS:
            assert getattr(module, name) == ""
    finally:
        monkeypatch.undo()
        _reload_settings()


def test_las_llaves_no_aparecen_en_los_reportes_de_error(settings):
    settings.STRIPE_SECRET_KEY = "secreta-de-prueba"
    settings.STRIPE_PUBLISHABLE_KEY = "publicable-de-prueba"
    settings.STRIPE_WEBHOOK_SECRET = "webhook-de-prueba"
    safe = SafeExceptionReporterFilter().get_safe_settings()
    for name in STRIPE_SETTINGS:
        assert safe[name] == SafeExceptionReporterFilter.cleansed_substitute


def test_settings_tiene_las_tres_llaves():
    for name in STRIPE_SETTINGS:
        assert hasattr(settings, name)
