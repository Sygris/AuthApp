# AuthApp

AuthApp is a slim, production-oriented authentication API built with **FastAPI** and **PostgreSQL (Docker)**. It provides JWT-based authentication with clean dependency separation and is designed to be easy to extend as the project grows.

## Features

* User registration and login
* Secure password hashing (bcrypt)
* JWT access tokens
* Refresh token support (server-side)
* Protected routes using FastAPI dependencies
* Role-based access control (user / admin)
* PostgreSQL database (Dockerized)

## Tech Stack

* **Backend:** FastAPI (Python)
* **Auth:** JWT (python-jose)
* **Database:** PostgreSQL (Docker)
* **ORM:** SQLAlchemy

## Project Structure

```
AuthApp/
├─ app/
│  ├─ api/          # Route definitions
│  ├─ core/         # Auth, config, security
│  ├─ models/       # SQLAlchemy models
│  ├─ schemas/      # Pydantic schemas
│  └─ main.py
├─ docker-compose.yml
├─ .env
├─ requirements.txt
└─ README.md
```

## Getting Started

### Prerequisites

* Python 3.10+
* Docker & Docker Compose

### Setup

```bash
git clone https://github.com/Sygris/AuthApp.git
cd AuthApp
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/authapp
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run PostgreSQL

```bash
docker-compose up -d
```

### Run the API

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

## Roles & Permissions

Users have a single role stored as an enum:

* `user`
* `admin`

Admin-only routes are protected using role-based dependencies.

## Security Notes

* Passwords are hashed using bcrypt
* JWTs are signed and time-limited
* Tokens are validated before every protected request
* Secrets must never be committed to source control
