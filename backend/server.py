import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db, User
from routes import auth_bp

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Allow CORS only for frontend domain
CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_URL", "https://draftempire.win")}})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

# Register Routes
app.register_blueprint(auth_bp, url_prefix="/auth")

# Ensure tables exist
with app.app_context():
    db.create_all()

# API Test Route
@app.route('/api/')
def hello_world():
    return jsonify({'message': "DraftEmpire Backend Running Successfully"})

if __name__ == '__main__':
    app.run(debug=False)  # Change debug to False in production!
