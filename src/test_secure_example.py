import pytest
import sqlite3
from unittest.mock import patch
from secure_example import app, get_user_info

# ------------------------------------------------
# FIXTURE: Flask test client
# ------------------------------------------------
@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

# ------------------------------------------------
# TEST: get_user_info() with safe parameterized SQL
# ------------------------------------------------
def test_get_user_info(tmp_path, monkeypatch):
    """Ensure SQL query works with parameterized query."""

    # Use a temporary DB path
    db_path = tmp_path / "test.db"

    # Patch sqlite3.connect to use temp DB
    monkeypatch.setattr(sqlite3, "connect", lambda _: sqlite3.connect(db_path))

    # Setup DB
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (username TEXT, email TEXT)")
    cur.execute("INSERT INTO users VALUES ('bob', 'bob@example.com')")
    conn.commit()
    conn.close()

    # Test the function
    result = get_user_info("bob")

    assert len(result) == 1
    assert result[0][0] == "bob"

# ------------------------------------------------
# TEST: /ping with valid IP
# ------------------------------------------------
def test_ping_valid_ip(client):
    with patch("secure_example.subprocess.run") as mock_run:
        mock_run.return_value = None  # simulate success

        response = client.get("/ping?ip=127.0.0.1")

        mock_run.assert_called_once_with(["ping", "-c", "1", "127.0.0.1"], check=True)
        assert response.status_code == 200
        assert response.json == {"message": "Pinged 127.0.0.1"}

# ------------------------------------------------
# TEST: /ping with invalid IP (blocked)
# ------------------------------------------------
def test_ping_invalid_ip(client):
    response = client.get("/ping?ip=bad_ip$$$")
    assert response.status_code == 400
    assert b"Invalid IP address" in response.data

# ------------------------------------------------
# TEST: /load endpoint (always blocked for safety)
# ------------------------------------------------
def test_load_always_blocked(client):
    response = client.get("/load?data=123456")
    assert response.status_code == 400
    assert b"Insecure operation blocked" in response.data

# ------------------------------------------------
# TEST: debug mode disabled
# ------------------------------------------------
def test_debug_mode_disabled():
    assert app.debug is False
