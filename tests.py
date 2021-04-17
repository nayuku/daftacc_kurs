import pytest
from fastapi.testclient import TestClient
from main import app, datetime, timedelta

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


@pytest.mark.parametrize("name", ["Zenek", "Mario", "Abc Def"])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {"msg": f"Hello {name}"}


def test_counter():
    for i in range(1, 3):
        response = client.get("/counter")
        assert response.status_code == 200
        assert response.text == str(i)


def test_method_type_get():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}


def test_method_type_post():
    response = client.post("/method")
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}


def test_method_type_delete():
    response = client.delete("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}


def test_method_type_put():
    response = client.put("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}


def test_method_type_options():
    response = client.options("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}


def test_check_password():
    response = client.get(
        "/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ce"
        "aabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response.status_code == 204
    response = client.get(
        "/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e0"
        "9fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091")
    assert response.status_code == 401


def test_register():
    patient = {
        "name": "Jan",
        "surname": "Kowalski"
    }
    response = client.post("/register", json=patient)
    vaccination_date = datetime.now() + timedelta(len(patient["name"]) + len(patient["surname"]))
    vaccination_date = vaccination_date.strftime("%Y-%m-%d")
    assert response.json() == {
        "id": 1,
        "name": "Jan",
        "surname": "Kowalski",
        "register_date": datetime.now().strftime("%Y-%m-%d"),
        "vaccination_date": vaccination_date
    }


def test_get_patient_info():
    # < 0
    response = client.get("/patient/0")
    assert response.status_code == 400

    # > num of patients
    response = client.get(f"/patient/{len(app.patients)+1}")
    assert response.status_code == 404

    # return first patient
    patient = {
        "name": "Jan",
        "surname": "Kowalski"
    }
    client.post("/register", json=patient)
    response = client.get(f"/patient/1")
    assert response.status_code == 200
    assert response.json() == app.patients[0]
