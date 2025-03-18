from flask import Flask, request, jsonify, session
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = "your-secret-key"  # Change this for production

# Temporary user storage (dictionary instead of a database)
USERS = {}

@app.route('/api/', methods=['GET'])
def home():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/signup', methods=["POST"])
def signup():
    """Minimal signup without a database"""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")

    if not email or not password or not username:
        return jsonify({"error": "Missing required fields"}), 400

    if email in USERS:
        return jsonify({"error": "User already exists"}), 400

    # Hash password before storing
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

    USERS[email] = {"username": username, "password_hash": password_hash}

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=["POST"])
def login():
    """Minimal login without a database"""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = USERS.get(email)
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
        return jsonify({"error": "Invalid email or password"}), 401

    session["user-email"] = email
    return jsonify({"message": "Login successful", "username": user["username"]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
