import sys
import os
import pytest

# Add repo root to Python path so main.py can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app, get_user_info
from flask.testing import FlaskClient
import sqlite3
import subprocess

# -------------------------------
# Fixture: Flask test client
# -------------------------------
@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

# -------------------------------
# Test get_user_info() function
# -------------------------------
def test_get_user_info(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"

    # Save the original sqlite3.connect
    original_connect = sqlite3.connect

    # Patch sqlite3.connect to use our temp DB
    monkeypatch.setattr(sqlite3, "connect", lambda _: original_connect(db_path))

    # Setup temporary DB
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (username TEXT, email TEXT)")
    cur.execute("INSERT INTO users VALUES ('bob', 'bob@example.com')")
    conn.commit()
    conn.close()

    # Test function
    result = get_user_info("bob")
    assert len(result) == 1
    assert result[0][0] == "bob"

# -------------------------------
# Test /ping endpoint with valid IP
# -------------------------------
def test_ping_valid_ip(client, monkeypatch):
    # Mock subprocess.run so no real ping is executed
    monkeypatch.setattr(subprocess, "run", lambda cmd, check: None)

    response = client.get("/ping?ip=127.0.0.1")
    assert response.status_code == 200
    assert response.json == {"message": "Pinged 127.0.0.1"}

# -------------------------------
# Test /ping endpoint with invalid IP
# -------------------------------
def test_ping_invalid_ip(client):
    response = client.get("/ping?ip=bad_ip$$$")
    assert response.status_code == 400
    assert b"Invalid IP address" in response.data

# -------------------------------
# Test /load endpoint (always blocked)
# -------------------------------
def test_load_blocked(client):
    response = client.get("/load?data=123456")
    assert response.status_code == 400
    assert b"Insecure operation blocked" in response.data

# -------------------------------
# Test debug mode disabled
# -------------------------------
def test_debug_mode_disabled():
    assert app.debug is False
