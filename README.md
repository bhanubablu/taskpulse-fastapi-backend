# TaskPulse — High-Performance Asynchronous Task & Workflow REST API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00.svg?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A production-grade, asynchronous RESTful microservice built with **Python**, **FastAPI**, **SQLAlchemy ORM**, **Pydantic v2**, and **JWT Authentication**. Demonstrates clean architecture, database persistence, secure password hashing, automated OpenAPI Swagger documentation, and automated testing with `pytest`.

---

## 📌 Architecture & Design Highlights

```
                 [ Client Request (JSON / HTTP) ]
                               │
                               ▼
                   [ FastAPI API Gateway ]
            - CORS Middleware
            - Pydantic v2 Request Validation & Type Hints
            - OpenAPI & Swagger Documentation (/docs)
                               │
                               ▼
                    [ JWT Auth & Security ]
            - OAuth2 Password Bearer Scheme
            - Salted Bcrypt Password Hashing (passlib)
            - Cryptographically Signed Tokens (HS256)
                               │
                               ▼
                     [ Business Controllers ]
            - Task CRUD (Pagination, Filters, Search)
            - Real-Time Completion & Priority Analytics
                               │
                               ▼
               [ SQLAlchemy 2.0 ORM Repository ]
            - User <-> Task 1-to-Many Relationships
            - SQLite (Default) / PostgreSQL Ready
```

---

## 🚀 Key Features

1. **Secure Authentication & RBAC:**
   - Registration with salted password hashing (`bcrypt`).
   - OAuth2-compatible login generating cryptographically signed JWT access tokens.
   - Protected endpoint dependencies ensuring only authenticated users access their own data.
2. **Complete Task Lifecycle Management:**
   - Full CRUD: Create, read, update, delete tasks.
   - Query filters: Filter by status (`pending`, `in_progress`, `completed`), priority (`low`, `medium`, `high`, `urgent`), search keyword in titles, and pagination (`skip`, `limit`).
3. **Data Validation with Pydantic v2:**
   - Strict request body typing, email validation, and clean serialization response schemas.
4. **Live Interactive API Documentation:**
   - Interactive Swagger UI automatically available at `http://localhost:8000/docs`.
   - ReDoc available at `http://localhost:8000/redoc`.
5. **Real-time Task Analytics:**
   - Dedicated endpoint `GET /api/v1/tasks/analytics/summary` computing total tasks, completion rate percentage, and high-priority bottlenecks.
6. **Containerized & Tested:**
   - Production multi-stage `Dockerfile` and `docker-compose.yml`.
   - Comprehensive unit and integration test suite with `pytest` and `httpx`.

---

## 📁 Repository Structure

```
.
├── app/
│   ├── main.py              # Application entrypoint & lifespan events
│   ├── core/
│   │   ├── config.py        # Centralized Pydantic settings & environment vars
│   │   ├── database.py      # SQLAlchemy engine, session maker & Base
│   │   └── security.py      # Bcrypt hashing & JWT token generators
│   ├── models/
│   │   ├── user.py          # SQLAlchemy User database model
│   │   └── task.py          # SQLAlchemy Task database model
│   ├── schemas/
│   │   ├── user.py          # Pydantic validation schemas for Users & Tokens
│   │   └── task.py          # Pydantic validation schemas for Tasks & Analytics
│   └── api/
│       ├── deps.py          # JWT authentication dependency injection
│       ├── auth.py          # /api/v1/auth routes (register, login, me)
│       └── tasks.py         # /api/v1/tasks routes (CRUD, search, analytics)
├── tests/
│   ├── test_auth.py         # Automated tests for registration, auth, & JWT
│   └── test_tasks.py        # Automated tests for Task CRUD & analytics
├── Dockerfile               # Production container image
├── docker-compose.yml       # 1-click local deployment
├── requirements.txt         # Pinned Python dependencies
└── README.md
```

---

## 🛠️ How to Run Locally

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/bhanubablu/taskpulse-fastapi-backend.git
cd taskpulse-fastapi-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
Open **[http://localhost:8000/docs](http://localhost:8000/docs)** in your browser to view and test all endpoints with interactive Swagger UI!

### 3. Run Automated Tests
```bash
pytest
```

### 4. Run via Docker
```bash
docker-compose up --build
```

---

## 🎤 Interview Cheat Sheet (How to Explain This in Interviews)

**Q: Why did you choose FastAPI over Flask or Django?**
> *"FastAPI is built on modern Python type hints and ASGI (Asynchronous Server Gateway Interface), making it one of the fastest Python frameworks available. It provides automatic request validation through Pydantic and generates interactive OpenAPI documentation out of the box, which reduces boilerplate code significantly compared to traditional Flask."*

**Q: How did you implement security and authentication?**
> *"I implemented OAuth2 password bearer authentication with JWT tokens. Passwords are never stored in plain text—they are hashed using bcrypt with dynamic salts via Passlib. When a user logs in, the API generates a cryptographically signed JWT token with an expiration timestamp that the client sends in the `Authorization: Bearer <token>` header for subsequent requests."*

**Q: How is database access structured?**
> *"I used SQLAlchemy ORM with a repository dependency injection pattern (`get_db`). This ensures database connections are automatically yielded per request and safely closed in a `finally` block, preventing database connection leaks under high concurrency."*

---

## 👨‍💻 Author
**Boddu Bhanu Prakash**  
- B.Tech in Electronics & Communication Engineering, **IIIT Dharwad (2021 – 2025)**  
- Email: [boddubhanuprakash7@gmail.com](mailto:boddubhanuprakash7@gmail.com)  
- LinkedIn: [linkedin.com/in/boddu-bhanu-prakash-b5309034b](https://www.linkedin.com/in/boddu-bhanu-prakash-b5309034b)  
- GitHub: [github.com/bhanubablu](https://github.com/bhanubablu)
