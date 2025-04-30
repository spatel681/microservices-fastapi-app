from site import USER_SITE
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import requests

app = FastAPI(title="Order Service")

conn = sqlite3.connect('orders.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        product_name TEXT NOT NULL
    )
 """)
conn.commit()

USER_SERVICE_URL = "http://user-service:8001/users"
PRODUCT_SERVICE_URL = "http://product-service:8002/products"


class Order(BaseModel):
    username: str
    product_name: str


@app.post("/orders", status_code=201)
def create_order(order: Order):
    try:
        users = requests.get(USER_SERVICE_URL).json()
        if not any(u['username'] == order.username for u in users):
            raise HTTPException(status_code=400, detail="User does not exist")
    except:
        raise HTTPException(status_code=500, detail="User service is unavailable")

    try:
        products = requests.get(PRODUCT_SERVICE_URL).json()
        if not any(p['name'] == order.product_name for p in products):
            raise HTTPException(status_code=400, detail="Product does not exist")
    except:
        raise HTTPException(status_code=500, detail="Product service is unavailable")

    cursor.execute(
        "INSERT INTO orders (username, product_name) VALUES (?, ?)",
        (order.username, order.product_name)
     )
    conn.commit()
    return {"message": "Order created successfully"}


@app.get("/orders", response_model=List[Order])
def list_orders():
    cursor.execute("SELECT username, product_name FROM orders")
    rows = cursor.fetchall()
    return [{"username": r[0], "product_name": r[1]} for r in rows]