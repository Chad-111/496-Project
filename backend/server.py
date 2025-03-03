from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bcrypt
import requests
import os
import random


import subprocess

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend
app.secret_key = "/,&R~Qh}<pl#kI@H#D&b&i>69Fhc?|"  # Change this to a secure key

# Dummy user credentials (can be stored in a database later)
USERS = {"admin": "password123"}

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/draftempire'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Log file paths
APACHE_ACCESS_LOG = "/var/log/apache2/draftempire_access.log"  # Update for your Apache logs
APACHE_ERROR_LOG = "/var/log/apache2/draftempire_error.log"

def check_task_status(task_name):
    """Check if a scheduled task is running"""
    try:
        result = subprocess.run(
            ["systemctl", "is-active", task_name], capture_output=True, text=True
        )
        return "Running" if "active" in result.stdout else "Not Running"
    except Exception as e:
        return f"Error: {e}"
    
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Handle Admin User Login"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("admin_dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/admin/logout")
def admin_logout():
    """Log out user"""
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/admin")
def admin_dashboard():
    """Admin panel - Requires login"""
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("admin_dashboard.html")

@app.route("/admin/ngrok_status", methods=["GET"])
def get_ngrok_status():
    """Fetch Ngrok status"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/admin/apache_access_logs", methods=["GET"])
def get_apache_access_logs():
    """Fetch Apache Access Logs"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    try:
        with open(APACHE_ACCESS_LOG, "r", encoding="utf-8") as f:
            logs = f.readlines()[-20:]
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/admin/apache_error_logs", methods=["GET"])
def get_apache_error_logs():
    """Fetch Apache Error Logs"""
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 403
    try:
        with open(APACHE_ERROR_LOG, "r", encoding="utf-8") as f:
            logs = f.readlines()[-20:]
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"error": str(e)})

# Initialize Database
db = SQLAlchemy(app)

# Define Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(63), nullable=False)

class League(db.Model):
    __tablename__ = 'leagues'
    id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))



# API Routes
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{ 'id': u.id, 'username': u.username, 'email': u.email } for u in users])

@app.route('/api/leagues', methods=['GET'])
def get_leagues():
    leagues = League.query.all()
    return jsonify([{ 'id': l.id, 'league_name': l.league_name, 'manager_id': l.manager_id } for l in leagues])


@app.route('/api/signup', methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    if not email or not password or not username:
        return jsonify({"error": "Missing required fields"}), 400
    

    # Check if user already exists
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    
    
    new_user = User(username=username, password_hash=str(hash), email=email)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    

    
# Handles logins
# Probably needs to be edited using sessions and whatnot
@app.route('/api/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Verify password
    if not bcrypt.checkpw(bytes(password, encoding="utf-8"), bytes(user.password_hash[2:-1], encoding="utf-8")):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "username": user.username}), 200


# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables exist
    app.run(host='0.0.0.0', port=5000, debug=True)
    


