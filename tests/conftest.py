import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base
from app.db.dependencies import get_db
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.client import Client
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.payment import Payment
# from dotenv import load_dotenv

# load_dotenv()

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://ledgerlite_user:L3dg3r_lite@localhost:5432/ledgerlite_test"
)

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)

    with test_engine.begin() as connection:
        connection.execute(
            text("CREATE SEQUENCE IF NOT EXISTS invoice_number_seq START WITH 1")
        )

    yield

    with test_engine.begin() as connection:
        connection.execute(
            text("DROP SEQUENCE IF EXISTS invoice_number_seq")
        )

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()



@pytest.fixture(autouse=True)
def clean_database(setup_test_database):
    with test_engine.begin() as connection:
        # Delete child records before parent records.
        connection.execute(Transaction.__table__.delete())
        connection.execute(Payment.__table__.delete())
        connection.execute(InvoiceItem.__table__.delete())
        connection.execute(Invoice.__table__.delete())

        connection.execute(Transaction.__table__.delete())
        connection.execute(Category.__table__.delete())
        connection.execute(Client.__table__.delete())


