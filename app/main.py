
from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine
from app.api.transaction import router as transactions_router


app = FastAPI(
    title="LedgerLite API",
    description="A lightweight financial management API",
    version="0.1.0",
)

app.include_router(transactions_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to LedgerLite API",
        "status": "running",
    }


@app.get("/health")
def health_check():

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except:
        return {
            "status": "not healthy",
            "database": "connection error"
        }