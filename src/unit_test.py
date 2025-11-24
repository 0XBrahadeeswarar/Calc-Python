import pytest
import sqlite3
from unittest.mock import patch
from vulnerable_example import app, get_user_info

# -----------------------------------------
# FIXTURE: Flask test client
# -----------------------------------------
@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

# -----------------------------------------
# TEST: get_user_info()
# -----------------------------------------
def test_get_user_info(tmp_path, monkeypatch):
    """Test SQL query runs and returns expected results."""

    # Create temp database
    db_path = tmp_path / "test.db"
    
    # Override sqlite connect path
    monkeypatch.setattr(sqlite3, "connect", lambda _: sqlite3.connect(db_path))

    # Prepare database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (username TEXT, email TEXT)")
    cur.execute("INSERT INTO users VALUES ('alice', 'alice@test.com')")
    conn.commit()
    conn.close()

    # Call function
    result = get_user_info("alice")

    assert len(result) == 1
    assert result[0][0] == "alice"

# -----------------------------------------
# TEST: /ping route (mocking os.system)
# -----------------------------------------
def test_ping_route(client):
    with patch("vulnerable_example.os.system") as mock_system:
        response = client.get("/ping?ip=127.0.0.1")
        
        mock_system.assert_called_once_with("ping -c 1 127.0.0.1")
        assert response.status_code == 200
        assert b"Pinged 127.0.0.1" in response.data

# -----------------------------------------
# TEST: /load route (mocking pickle.loads)
# -----------------------------------------
def test_load_route(client):
    fake_hex = "414243"  # hex for ABC

    with patch("vulnerable_example.pickle.loads") as mock_loads:
        mock_loads.return_value = "FAKE_OBJECT"

        response = client.get(f"/load?data={fake_hex}")

        mock_loads.assert_called_once()
        assert response.status_code == 200
        assert b"FAKE_OBJECT" in response.data

# -----------------------------------------
# TEST: Flask debug flag
# -----------------------------------------
def test_flask_debug_disabled_in_tests():
    """Ensure debug is not accidentally on in testing."""
    assert not app.debug
