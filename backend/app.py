from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import bcrypt

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# Security settings (change for production)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True  # Change to False if testing without HTTPS

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://admin:password@postgres:5432/draftempire")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Add Migrate

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# Routes
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Flask Backend with PostgreSQL"})

@app.route('/api/test', methods=['GET'])
def api_test():
    return jsonify({"message": "Hello from Flask!"})

# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
