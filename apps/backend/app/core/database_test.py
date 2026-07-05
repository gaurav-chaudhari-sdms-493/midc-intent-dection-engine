from sqlalchemy import text

from app.core.database import engine


def test_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return True
