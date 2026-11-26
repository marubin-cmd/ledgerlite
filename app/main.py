from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api import transaction, category, client, invoice, invoice_items, payments
from app.db.dependencies import get_db


from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="LedgerLite API",
    description="A lightweight financial management API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transaction.router)
app.include_router(category.router)
app.include_router(client.router)
app.include_router(invoice.router)
app.include_router(invoice_items.router)
app.include_router(payments.router)

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