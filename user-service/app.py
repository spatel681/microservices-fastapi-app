from codecs import StreamReaderWriter
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI(title="User Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use ["http://localhost:3000"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL
)
''')
conn.commit()

class User(BaseModel):
    username: str
    email: str

@app.post("/users", status_code=201)
def create_user(user: User):
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (user.username, user.email))
        conn.commit()
        return {"message": "User created successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")


@app.get("/users", response_model=List[User])
def get_users():
    cursor.execute("SELECT username, email FROM users")
    users = cursor.fetchall()
    return [{"username": user[0], "email": user[1]} for user in users]