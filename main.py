import hashlib

from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

app = FastAPI()
app.counter = 0
app.patient_id = 1
app.patients = []
app.ids = []


class HelloResp(BaseModel):
    msg: str


class Patient(BaseModel):
    name: str
    surname: str


@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter


@app.get("/hello/{name}", response_model=HelloResp)
def test_hello_name(name: str):
    return HelloResp(msg=f"Hello {name}")


# 1.1
@app.get("/")
def root():
    return {"message": "Hello world!"}


# 1.2
@app.api_route("/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"], status_code=200)
def method_type(request: Request, response: Response):
    if request.method == "POST":
        response.status_code = status.HTTP_201_CREATED
    return {"method": request.method}


# 1.3
@app.get("/auth", status_code=401)
def check_password(password: Optional[str] = None, password_hash: Optional[str] = None):
    if not password or not password_hash:
        return

    calc_hash = hashlib.sha512(password.encode("utf-8")).hexdigest()
    if calc_hash == password_hash:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


# 1.4
@app.post("/register")
def register(patient: Patient):
    register_date = datetime.now().strftime("%Y-%m-%d")
    vaccination_date = datetime.strptime(register_date, "%Y-%m-%d") + timedelta(
        len(patient.name) + len(patient.surname))
    vaccination_date = vaccination_date.strftime("%Y-%m-%d")
    patient_info = {
        "id": app.patient_id,
        "name": patient.name,
        "surname": patient.surname,
        "register_date": register_date,
        "vaccination_date": vaccination_date
    }
    app.patients.append(patient_info)
    app.patient_id += 1
    return patient_info


# 1.5
@app.get("/patient/{id}")
def get_patient_info(id: int):
    if id < 1:
        raise HTTPException(status_code=400)
    elif id > len(app.patients):
        raise HTTPException(status_code=404)
    return app.patients[id - 1]
