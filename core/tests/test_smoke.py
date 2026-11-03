from django.urls import reverse


def test_home_responde(client):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    assert "EngiMods" in response.content.decode()


def test_health_responde_ok(client):
    response = client.get(reverse("core:health"))
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
