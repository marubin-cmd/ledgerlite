from sqlalchemy import text

from app.db.session import engine

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), current_user")
        )
        database, user = result.fetchone()

        print(f"Connected to database: {database}")
        print(f"Connected as user: {user}")

except Exception as error:
    print(f"Database connection failed: {error}")
