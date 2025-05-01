from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI(title="Product Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use ["http://localhost:3000"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

conn = sqlite3.connect('products.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL
    )
''')
conn.commit()


class Product(BaseModel):
    name: str
    description: str = ""
    price: float

@app.post("/products", status_code=201)
def create_product(product: Product):
    cursor.execute(
    "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
    (product.name, product.description, product.price)
    )
    conn.commit()
    return {"message": "Product created"}

@app.get("/products", response_model=List[Product])
def list_products():
    cursor.execute("SELECT name, description, price FROM products")
    rows = cursor.fetchall()
    return [{"name": r[0], "description": r[1], "price": r[2]} for r in rows]