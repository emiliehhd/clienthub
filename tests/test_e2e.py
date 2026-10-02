import requests


BASE_URL = "http://localhost:8012"


def test_health_e2e():
    response = requests.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_clients_e2e():
    response = requests.get(f"{BASE_URL}/clients")

    assert response.status_code == 200

    clients = response.json()

    assert isinstance(clients, list)
    assert len(clients) > 0
    assert "id" in clients[0]
    assert "name" in clients[0]
