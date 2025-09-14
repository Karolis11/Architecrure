import pytest
from fastapi.testclient import TestClient
from app import app
from repositories.client_repository import InMemoryClientRepository
from services.client_service import ClientService
from core.container import get_client_service

# python -m pytest -q --cov=api.clients --cov-report=term-missing

@pytest.fixture()
def client():
# Fresh, isolated repo/service per test so state doesn't leak
    repo = InMemoryClientRepository()
    service = ClientService(repo)

    def override():
        return service

    app.dependency_overrides[get_client_service] = override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_create_client_201(client):
    res = client.post(
    "/api/clients",
    json={"full_name": "Alice Doe", "email": "a@x.com", "phone": "+370 600 00000", "age": 28},
    )
    assert res.status_code == 201, res.text
    body = res.json()
    assert body["id"] > 0
    assert body["full_name"] == "Alice Doe"


def test_create_invalid_email_422(client):
    res = client.post(
    "/api/clients",
    json={"full_name": "Bob", "email": "not-an-email", "phone": "+1 222 333", "age": 30},
    )
    assert res.status_code == 422


def test_list_and_get(client):
    # create two
    r1 = client.post("/api/clients", json={"full_name": "Abra", "email": "a@a.com", "phone": "+1 111 111", "age": 20})
    r2 = client.post("/api/clients", json={"full_name": "Babra", "email": "b@b.com", "phone": "+1 222 222", "age": 21})
    id1 = r1.json()["id"]
    id2 = r2.json()["id"]

    # list
    res = client.get("/api/clients")
    assert res.status_code == 200
    first_client_name = res.json()[0]["full_name"]
    assert first_client_name == ("Abra")
    second_client_email = res.json()[1]["email"]
    assert second_client_email == ("b@b.com")

    # get one
    show = client.get(f"/api/clients/{id1}")
    assert show.status_code == 200
    assert show.json()["full_name"] == "Abra"

def test_get_404(client):
    res = client.get("/api/clients/9999")
    assert res.status_code == 404


def test_update_ok_and_invalid(client):
    created = client.post("/api/clients", json={"full_name": "Cipolinas", "email": "c@c.com", "phone": "+1 333 333", "age": 40}).json()
    cid = created["id"]

    # ok
    upd = client.put(f"/api/clients/{cid}", json={"full_name": "C Prime", "email": "c@c.com", "phone": "+1 333 333", "age": 41})
    assert upd.status_code == 200
    assert upd.json()["full_name"] == "C Prime"

    # invalid (age too low)
    bad = client.put(f"/api/clients/{cid}", json={"full_name": "Cinkas", "email": "c@c.com", "phone": "+1 333 333", "age": 10})
    assert bad.status_code == 422


def test_update_404(client):
    res = client.put("/api/clients/12345", json={"full_name": "Zebras", "email": "z@z.com", "phone": "+1 999 999", "age": 50})
    assert res.status_code == 404


def test_delete_ok_and_404(client):
    cid = client.post("/api/clients", json={"full_name": "Darbas", "email": "d@d.com", "phone": "+1 444 444", "age": 32}).json()["id"]

    # delete ok
    res = client.delete(f"/api/clients/{cid}")
    assert res.status_code == 204

    # now it's gone
    res2 = client.get(f"/api/clients/{cid}")
    assert res2.status_code == 404


def test_phone_validation(client):
    res = client.post("/api/clients", json={"full_name": "E", "email": "e@e.com", "phone": "86", "age": 23})
    assert res.status_code == 422