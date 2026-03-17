"""
Demo API Server — standalone Flask app.
No dependencies on any test framework. Run: python app.py
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "Alice", "email": "alice@test.com"},
]
TOKENS = {"alice@test.com": "token-alice-123"}


@app.get("/health")
def health():
    """Health check. No auth required."""
    return jsonify({"status": "ok"})


@app.get("/users")
def list_users():
    """List all users. No auth required."""
    return jsonify({"users": USERS})


@app.get("/users/<int:user_id>")
def get_user(user_id):
    """Get user by ID. Returns 404 if not found."""
    u = next((x for x in USERS if x["id"] == user_id), None)
    if u:
        return jsonify(u)
    return jsonify({"error": "not found"}), 404


@app.post("/login")
def login():
    """Login with email and password. Valid: alice@test.com / secret123"""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "invalid json"}), 400
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "missing email or password"}), 400
    if email == "alice@test.com" and password == "secret123":
        return jsonify({"token": TOKENS[email], "user_id": 1})
    return jsonify({"error": "invalid credentials"}), 401


@app.get("/me")
def me():
    """Get current user. Requires Authorization: Bearer <token> header."""
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return jsonify({"error": "unauthorized"}), 401
    token = auth.split(" ", 1)[1]
    if token == "token-alice-123":
        return jsonify(USERS[0])
    return jsonify({"error": "invalid token"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
