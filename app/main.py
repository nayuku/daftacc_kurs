'''
import hashlib
import sqlite3
import uuid

from fastapi import FastAPI, Request, Response, status, HTTPException, Query, Cookie, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, JSONResponse
from fastapi.templating import Jinja2Templates
'''

from fastapi import FastAPI
from .views import router as northwind_api_router

app = FastAPI()
app.include_router(northwind_api_router, tags=["northwind"])

'''
templates = Jinja2Templates(directory="templates")

app.counter = 0
app.patient_id = 1
app.patients = []
app.ids = []


class HelloResp(BaseModel):
    msg: str


class Patient(BaseModel):
    name: str
    surname: str


def letters_len(string: str):
    n = 0
    for l in string.lower():
        if (l >= 'a' and l <= 'z') or l in 'ąęćłńóśźż':
            n += 1
    return n


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
@app.post("/register", status_code=201)
def register(patient: Patient):
    register_date = datetime.now().strftime("%Y-%m-%d")
    vaccination_date = datetime.strptime(register_date, "%Y-%m-%d") + timedelta(
        letters_len(patient.name) + letters_len(patient.surname))
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


# 3
@app.get("/request_query_string_discovery/")
def read_items(u: str = Query("default"), q: List[str] = Query(None)):
    query_items = {"q": q, "u": u}
    return query_items


@app.get("/static", response_class=HTMLResponse)
def index_static():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
            <a href="http://thiszone.pl">thiszone</a>
        </body>
    </html>
    """


@app.get("/jinja")
def read_item(request: Request):
    return templates.TemplateResponse("index1.html", {
        "request": request, "my_string": "Wheeeee!", "my_list": [0, 1, 2, 3, 4, 5]})


@app.get("/simple_path_tmpl/{sample_variable}")
def simple_path_tmpl(sample_variable: str):
    print(f"{sample_variable=}")
    print(type(sample_variable))
    return {"sample_variable": sample_variable}


app.secret_key = "very constatn and random secret, best 64+ characters"
app.access_tokens = []


@app.get("/login/")
def login(user: str, password: str, response: Response):
    session_token = hashlib.sha256(f"{user}{password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    return {"message": session_token}


@app.get("/data/")
def secured_data(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=403, detail="Unauthorised")
    else:
        return {"message": "Secure Content"}


# 3.1
@app.get("/hello", response_class=HTMLResponse)
def hello():
    return f"""
    <h1>Hello! Today date is {datetime.now().strftime("%Y-%m-%d")}</h1>"""


# 3.2
security = HTTPBasic()
app.session_tokens = []
app.tokens = []


def auth(login: str, password: str):
    if login == "4dm1n" and password == "NotSoSecurePa$$":
        return True
    return False


@app.post("/login_session", status_code=201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if not auth(credentials.username, credentials.password):
        raise HTTPException(status_code=401)
    session_token = str(uuid.uuid1())
    if session_token not in app.session_tokens:
        app.session_tokens.append(session_token)
    if len(app.session_tokens) > 3:
        app.session_tokens.pop(0)
    print(app.session_tokens)
    response.set_cookie(key="session_token", value=session_token)
    return {}


@app.post("/login_token", status_code=201)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    if not auth(credentials.username, credentials.password):
        raise HTTPException(status_code=401)
    token = str(uuid.uuid1())
    if token not in app.tokens:
        app.tokens.append(token)
    if len(app.tokens) > 3:
        app.tokens.pop(0)
    print(app.tokens)
    return {"token": token}


# 3.3
@app.get("/welcome_session")
def welcome_session(session_token: str = Cookie(None), format: str = None):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401)
    if format == "json":
        return JSONResponse(content={"message": "Welcome!"})
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    return PlainTextResponse(content="Welcome!")


@app.get("/welcome_token")
def welcome_token(token: str, format: str = None):
    if token not in app.tokens:
        raise HTTPException(status_code=401)
    if format == "json":
        return JSONResponse(content={"message": "Welcome!"})
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    return PlainTextResponse(content="Welcome!")


# 3.4
@app.delete("/logout_session")
def logout_session(session_token: str = Cookie(None), format: str = None):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401)
    app.session_tokens.remove(session_token)
    if format is None:
        return RedirectResponse(url="/logged_out", status_code=302)
    return RedirectResponse(url=f"/logged_out?format={format}", status_code=302)


@app.delete("/logout_token")
def logout_token(token: str, format: str = None):
    if token not in app.tokens:
        raise HTTPException(status_code=401)
    app.tokens.remove(token)
    if format is None:
        return RedirectResponse(url="/logged_out", status_code=302)
    return RedirectResponse(url=f"/logged_out?format={format}", status_code=302)


@app.get("/logged_out")
def logged_out(format: str = None):
    if format == 'json':
        return JSONResponse(content={"message": "Logged out!"})
    elif format == 'html':
        return HTMLResponse(content="<h1>Logged out!</h1>")
    return PlainTextResponse(content="Logged out!")


# 4
@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("../northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


# 4.1
@app.get("/categories")
async def get_categories():
    app.db_connection.row_factory = sqlite3.Row
    categories = app.db_connection.execute(
        "SELECT CategoryID as id, CategoryName as name"
        " FROM Categories ORDER BY CategoryID;"
    ).fetchall()
    return {
        "categories": categories
    }


@app.get("/customers")
async def get_customers():
    app.db_connection.row_factory = sqlite3.Row
    customers = app.db_connection.execute(
        "SELECT CustomerID as id, CompanyName as name,"
        "Address||' '||PostalCode||' '||City||' '||Country AS full_address"
        " FROM Customers order by CustomerID collate nocase asc;"
    ).fetchall()
    return {
        "customers": customers
    }


# 4.2
@app.get("/products/{id}")
async def get_product_by_id(id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT ProductID as id, ProductName as name"
        " FROM Products WHERE ProductID = :id",
        {'id': id}).fetchone()
    if data is None:
        raise HTTPException(status_code=404)
    return data


# 4.3
@app.get("/employees")
async def get_employees(limit: int = -1, offset: int = 0, order: str = "id"):
    if order not in ["id", "first_name", "last_name", "city"]:
        raise HTTPException(status_code=400)
    app.db_connection.row_factory = sqlite3.Row
    # in version without sql inj ORDER BY doesn't work :/
    # data = app.db_connection.execute("""SELECT EmployeeID id, LastName last_name, FirstName first_name, City city
    #                                  FROM Employees ORDER BY :order ASC LIMIT :limit OFFSET :offset""",
    #                                  {'order': order, 'limit': limit, 'offset': offset}).fetchall()
    data = app.db_connection.execute(f"SELECT EmployeeID id, LastName last_name, FirstName first_name, City city "
                                     f"FROM Employees ORDER BY {order} ASC LIMIT {limit} OFFSET {offset}").fetchall()
    return {
        "employees": data
    }


# 4.4
@app.get("/products_extended")
async def get_employees():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("""
        SELECT p.ProductID id, p.ProductName name, c.CategoryName category, s.CompanyName supplier 
        FROM Products p 
        JOIN Categories c on p.CategoryID = c.CategoryID 
        JOIN Suppliers s on p.SupplierID = s.SupplierID 
        ORDER BY id;""").fetchall()
    return {
        "products_extended": data
    }


# 4.5
@app.get("/products/{id}/orders")
async def get_prod_orders_by_id(id: int):
    app.db_connection.row_factory = sqlite3.Row
    # this query returns always 2 place after delimiter, e.g. 2->2.00, 2.1 ->2.10
    # PRINTF('%.2f',((od.UnitPrice * od.Quantity) - (od.Discount * (od.UnitPrice * od.Quantity)))) total_price
    data = app.db_connection.execute("""
    SELECT o.OrderID id, c.CompanyName customer, od.Quantity quantity,
    ROUND(((od.UnitPrice * od.Quantity) - (od.Discount * (od.UnitPrice * od.Quantity))),2) total_price
    FROM Orders o 
    JOIN Customers c on o.CustomerID = c.CustomerID
    JOIN 'Order Details' od on o.OrderID = od.OrderID
    JOIN Products p on od.ProductID = p.ProductID 
    WHERE p.ProductID = :id
    ORDER BY id""", {'id': id}).fetchall()
    if not data:
        raise HTTPException(status_code=404)
    return {
        "orders": data
    }


# 4.6

class Cat(BaseModel):
    name: str


@app.post("/categories", status_code=201)
async def add_category(cat: Cat):
    cursor = app.db_connection.execute("INSERT INTO Categories (CategoryName) VALUES (:cat)", {'cat': cat.name})
    app.db_connection.commit()

    last_id = cursor.lastrowid
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT CategoryID id, CategoryName name FROM Categories WHERE id = :id;",
                                     {'id': last_id}).fetchone()
    return data


@app.put("/categories/{id}")
async def edit_category(id: int, cat: Cat):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT * FROM Categories WHERE CategoryID = :id", {'id': id}).fetchone()
    if data is None:
        raise HTTPException(status_code=404)

    app.db_connection.execute("UPDATE Categories SET CategoryName = :cat WHERE CategoryID = :id;",
                              {'cat': cat.name, "id": id})
    app.db_connection.commit()

    data = app.db_connection.execute("SELECT CategoryID id, CategoryName name FROM Categories WHERE CategoryID = :id",
                                     {'id': id}).fetchone()

    return data


@app.delete("/categories/{id}")
async def del_category(id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT * FROM Categories WHERE CategoryID = :id", {'id': id}).fetchone()
    if data is None:
        raise HTTPException(status_code=404)

    app.db_connection.execute("DELETE FROM Categories WHERE CategoryID = :id;", {'id': id})
    app.db_connection.commit()
    return {"deleted": 1}
'''
