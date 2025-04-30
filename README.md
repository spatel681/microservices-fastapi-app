# 🧩 Microservices App with FastAPI, Docker & SQLite

This project is a simple microservices-based application built with **Python FastAPI**, using **Docker** for containerization and **SQLite** for storage. It's designed as a lightweight portfolio-ready example of how to build independently deployable services that communicate via REST.

---

## 🚀 Services Overview

| Service         | Port  | Endpoints             | Description                           |
|-----------------|-------|------------------------|---------------------------------------|
| User Service    | 8001  | `/users`              | Register and list users               |
| Product Service | 8002  | `/products`           | Add and list products                 |
| Order Service   | 8003  | `/orders`             | Place and list orders (calls others)  |

---

## 🔧 How to Run (with Docker)

> You need Docker and Docker Compose installed.

```bash
git clone https://github.com/spatel681/microservices-fastapi-app.git
cd microservices-fastapi-app
docker-compose up --build
