# LedgerLite

**Personal Finance and Invoice Management REST API**

LedgerLite is a backend application designed to manage business finances, clients, invoices, payments, and financial transactions. 
It is built using FastAPI and PostgreSQL, with SQLAlchemy for database operations and Alembic for database migrations.

The project focuses on building a structured, maintainable REST API with automated testing and Docker-based deployment.

## Features

- **Client Management** – Create and manage client records.
- **Invoice Management** – Create and manage invoices associated with clients.
- **Payment Management** – Record invoice payments and track payment status.
- **Category Management** – Organize income and expense categories.
- **Transaction Management** – Record and manage income and expense transactions.
- **Financial Summary** – Calculate total income, expenses, and balance.
- **Database Migrations** – Manage database schema changes using Alembic.
- **Automated Testing** – Test application functionality using Pytest.
- **Containerization** – Run the application and PostgreSQL database using Docker Compose.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Alembic | Database migrations |
| Pydantic | Data validation and serialization |
| Pytest | Automated testing |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Uvicorn | ASGI server |

## Project Structure

```text
ledgerlite/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── migrations/
├── tests/
├── .dockerignore
├── .gitignore
├── alembic.ini
├── compose.yaml
├── dockerfile
├── entrypoint.sh
└── requirements.txt
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Git

### 1. Clone the repository

```bash
git clone https://github.com/marubin-cmd/ledgerlite.git
cd ledgerlite
```

### 2. Configure environment variables

Create a `.env` file in the project root.

```env
DB_PASSWORD=your_secure_password
```

Use your own secure database password.

### 3. Build and run the application

```bash
docker compose up --build
```

Docker Compose starts the FastAPI application and PostgreSQL database.

Database migrations are executed through the application entrypoint.

### 4. Access the API

Once the containers are running, access the following endpoints:

| Endpoint | Description |
|---|---|
| `http://localhost:8000` | API welcome endpoint |
| `http://localhost:8000/health` | Application health check |
| `http://localhost:8000/docs` | Interactive Swagger UI |
| `http://localhost:8000/redoc` | ReDoc API documentation |

## Running Tests

LedgerLite uses Pytest for automated testing.

Tests require a separate test database configured through `TEST_DATABASE_URL`.

Activate your virtual environment and run:

```bash
python -m pytest -v
```

## Development Focus

This project was developed as a practical exercise in backend engineering, focusing on:

- REST API development
- Relational database design
- ORM relationships and constraints
- Database migrations
- Business logic and data validation
- Automated testing
- Docker-based development environments

## Future Improvements

- Frontend integration
- Authentication and authorization
- Improved financial reporting
- Additional API functionality
- CI/CD automation

## License

This project is currently developed for learning and portfolio purposes.
