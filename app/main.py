from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api import transaction, category
from app.db.dependencies import get_db

app = FastAPI(
    title="LedgerLite API",
    description="A lightweight financial management API",
    version="0.1.0",
)

app.include_router(transaction.router)
app.include_router(category.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to LedgerLite API",
        "status": "running",
    }


@app.get("/health")
def health_check(
    db: Session = Depends(get_db)
):

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        return {
            "status": "not healthy",
            "database": "connection error"
        }