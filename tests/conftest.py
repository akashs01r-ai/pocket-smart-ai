import pytest

from fastapi.testclient import TestClient


@pytest.fixture()
def client(
    tmp_path,
    monkeypatch,
):

    database_path = (
        tmp_path / "test.db"
    )

    monkeypatch.setenv(
        "DATABASE_URL",
        f"sqlite:///{database_path}",
    )

    monkeypatch.setenv(
        "SECRET_KEY",
        "test-secret-key",
    )

    monkeypatch.setenv(
        "GEMINI_API_KEY",
        "",
    )

    from app.config import get_settings

    get_settings.cache_clear()

    from app.main import app

    from app.database import init_db

    init_db()

    with TestClient(app) as test_client:
        yield test_client