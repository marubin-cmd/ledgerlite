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

Make sure you have the following installed:

- Python 3.14+
- PostgreSQL
- Git
- Docker and Docker Compose (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ledgerlite.git
cd ledgerlite
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/ledgerlite
TEST_DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/ledgerlite_test
```

Replace `USERNAME` and `PASSWORD` with your PostgreSQL credentials.

**Important:** The default PostgreSQL port is `5432`. If you're connecting to the PostgreSQL Docker container from your host machine using the current Docker Compose configuration, use port `5433` instead.

Never commit your actual `.env` file or database credentials.

### 5. Create the Databases

Create the development and test databases in PostgreSQL:

```sql
CREATE DATABASE ledgerlite;
CREATE DATABASE ledgerlite_test;
```

Make sure your PostgreSQL user has permission to access both databases.

### 6. Apply Database Migrations

```bash
alembic upgrade head
```

This creates the required database tables and schema using Alembic migrations.

### 7. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 8. Run Automated Tests

Make sure `TEST_DATABASE_URL` points to a dedicated test database, not your development database.

Run:

```bash
python -m pytest -v
```

The project currently has **108 passing automated tests**.

### Running with Docker (Optional)

To build and start the application and PostgreSQL containers:

```bash
docker compose up --build -d
```

Check container status:

```bash
docker compose ps
```

Stop the containers:

```bash
docker compose down
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
