import sqlite3
from contextlib import contextmanager

from .config import get_settings


def init_db() -> None:
    settings = get_settings()

    database_path = settings.database_path

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with sqlite3.connect(database_path) as connection:
        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                email TEXT NOT NULL UNIQUE,

                name TEXT NOT NULL,

                password_hash TEXT NOT NULL,

                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                planner TEXT NOT NULL,

                budget REAL NOT NULL,

                request_json TEXT NOT NULL,

                response_json TEXT NOT NULL,

                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            );
            """
        )


@contextmanager
def get_conn():
    settings = get_settings()

    database_path = settings.database_path

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        database_path
    )

    connection.row_factory = sqlite3.Row

    try:
        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        yield connection

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()