# vulnerable_example.py
# WARNING: This code is intentionally insecure for SonarQube testing purposes only.
# DO NOT use in production environments.

import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# --- Vulnerability 1: Hardcoded credentials ---
DB_USER = "admin"
DB_PASS = "password123"  # Sensitive data hardcoded

# --- Vulnerability 2: SQL Injection ---
def get_user_info(username):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    # Direct string concatenation with user input (SQL Injection risk)
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

# --- Vulnerability 3: Command Injection ---
@app.route("/ping")
def ping():
    ip = request.args.get("ip", "")
    # Directly passing user input to system command
    os.system(f"ping -c 1 {ip}")
    return f"Pinged {ip}"

# --- Vulnerability 4: Insecure Deserialization ---
import pickle
@app.route("/load")
def load_data():
    data = request.args.get("data", "")
    # Loading untrusted data (RCE risk)
    obj = pickle.loads(bytes.fromhex(data))
    return str(obj)

# --- Vulnerability 5: Debug mode enabled ---
if __name__ == "__main__":
    app.run(debug=True)  # Debug mode exposes sensitive info
