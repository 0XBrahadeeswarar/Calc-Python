# secure_example.py
# This is the secure version of the previous vulnerable code.

import os
import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# -------------------------------
# FIX 1: Remove hardcoded credentials
# -------------------------------
# Credentials must come from environment variables
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")

# -------------------------------
# FIX 2: Prevent SQL Injection using parameterized queries
# -------------------------------
def get_user_info(username):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # SAFE: Use parameterized query
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))

    result = cursor.fetchall()
    conn.close()
    return result

# -------------------------------
# FIX 3: Prevent Command Injection
# Only allow safe IP pattern (digits and dots)
# -------------------------------
import re

@app.route("/ping")
def ping():
    ip = request.args.get("ip", "")

    # Validate IP format (simple IPv4 check)
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        abort(400, "Invalid IP address.")

    # SAFE: Use subprocess with args list (no shell)
    import subprocess
    try:
        subprocess.run(["ping", "-c", "1", ip], check=True)
    except Exception:
        abort(500, "Ping failed.")

    return jsonify({"message": f"Pinged {ip}"})

# -------------------------------
# FIX 4: Prevent Insecure Deserialization
# Reject pickle entirely (SAFE)
# -------------------------------
@app.route("/load")
def load_data():
    data = request.args.get("data", "")

    # NEVER trust pickle data → reject it
    abort(400, "Insecure operation blocked: Deserialization disabled.")

# -------------------------------
# FIX 5: Disable debug mode
# -------------------------------
if __name__ == "__main__":
    app.run(debug=False)  # Safe mode (no debug)
