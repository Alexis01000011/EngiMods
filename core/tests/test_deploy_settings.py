"""Configuración de staging (EM-005): HTTPS, dominio del proveedor y check --deploy."""

import importlib
import os
import secrets
import subprocess
import sys

import pytest
from django.conf import settings as django_settings

import config.settings


def _reload_settings():
    return importlib.reload(config.settings)


@pytest.fixture
def reload_settings(monkeypatch):
    """Recarga config.settings con las variables que ponga la prueba y lo deja como estaba."""
    monkeypatch.setattr("environ.Env.read_env", lambda *args, **kwargs: None)
    monkeypatch.setenv("SECRET_KEY", "solo-para-pruebas")
    for name in ("HTTPS_ONLY", "RENDER_EXTERNAL_HOSTNAME", "SECURE_HSTS_SECONDS"):
        monkeypatch.delenv(name, raising=False)
    yield _reload_settings
    monkeypatch.undo()
    _reload_settings()


def test_staging_pasa_check_deploy_sin_advertencias():
    env = {
        "PATH": os.environ.get("PATH", ""),
        "SECRET_KEY": secrets.token_urlsafe(50),
        "DEBUG": "False",
        "HTTPS_ONLY": "True",
        "ALLOWED_HOSTS": "staging.example.com",
    }
    result = subprocess.run(
        [sys.executable, "manage.py", "check", "--deploy", "--fail-level", "WARNING"],
        cwd=django_settings.BASE_DIR,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_https_only_activa_redireccion_cookies_seguras_y_hsts(reload_settings, monkeypatch):
    monkeypatch.setenv("HTTPS_ONLY", "True")
    module = reload_settings()
    assert module.SECURE_SSL_REDIRECT is True
    assert module.SECURE_PROXY_SSL_HEADER == ("HTTP_X_FORWARDED_PROTO", "https")
    assert module.SESSION_COOKIE_SECURE is True
    assert module.CSRF_COOKIE_SECURE is True
    assert module.SECURE_HSTS_SECONDS > 0


def test_sin_https_only_desarrollo_y_ci_siguen_en_http(reload_settings):
    module = reload_settings()
    assert module.HTTPS_ONLY is False
    assert module.SECURE_SSL_REDIRECT is False
    assert module.SECURE_PROXY_SSL_HEADER is None
    assert module.SESSION_COOKIE_SECURE is False
    assert module.SECURE_HSTS_SECONDS == 0


def test_el_dominio_de_render_se_agrega_a_los_hosts_permitidos(reload_settings, monkeypatch):
    monkeypatch.setenv("ALLOWED_HOSTS", "localhost")
    monkeypatch.setenv("RENDER_EXTERNAL_HOSTNAME", "engimods-staging.onrender.com")
    module = reload_settings()
    assert module.ALLOWED_HOSTS == ["localhost", "engimods-staging.onrender.com"]


def test_con_redireccion_https_el_health_check_responde_por_http(client, settings):
    settings.SECURE_SSL_REDIRECT = True
    settings.SECURE_REDIRECT_EXEMPT = [r"^health/$"]

    assert client.get("/health/").status_code == 200
    assert client.get("/").status_code == 301
