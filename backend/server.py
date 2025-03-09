from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bcrypt
import requests
import os
import random
from sqlalchemy import PrimaryKeyConstraint, Column, ForeignKey, create_engine, Integer, String, Float
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


import subprocess

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend
app.secret_key = "/,&R~Qh}<pl#kI@H#D&b&i>69Fhc?|"  # Change this to a secure key

# Dummy user credentials (can be stored in a database later)
USERS = {"admin": "password123"}

# PostgreSQL Database Configuration
SQLALCHEMY_URI = 'postgresql://admin:admin@localhost/draftempire'

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
engine = create_engine(SQLALCHEMY_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

# Define Models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(63), nullable=False)


class League(Base):
    __tablename__ = 'leagues'
    id = Column(Integer, primary_key=True)
    league_name = Column(String(100), nullable=False)
    manager_id = Column(Integer, ForeignKey('users.id'))


class Team(Base):
    __tablename__ = "teams"
    team_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    league_id = Column(Integer, ForeignKey("leagues.id"))
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)


class TeamPlayer(Base):
    __tablename__ = "teamplayers"
    player_id = Column(Integer, ForeignKey("players.id"))
    league_id = Column(Integer, ForeignKey("leagues.id"))
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    starting_position = Column(String(3), default="BEN") # bench default
    __table_args__ = (
        PrimaryKeyConstraint(player_id, league_id),
    )


class Matchup(Base):
    __tablename__ = "matchups"
    id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey("leagues.id"))
    week_num = Column(Integer, default=1)
    away_team_id = Column(Integer, ForeignKey("teams.team_id"))
    away_team_score = Column(Float(5), default=0)
    home_team_id = Column(Integer, ForeignKey("teams.team_id"))
    home_team_score = Column(Float(5), default=0)


class Ruleset(Base):
    __tablename__ = "rulesets"
    
    league_id = Column(Integer, ForeignKey("leagues.id"), primary_key=True)
    
    # Passing stats
    points_passtd = Column(Float, default=4.0)  # Passing TD
    points_passyd = Column(Float, default=0.04)  # Passing yard
    points_int = Column(Float, default=-2.0)  # Interception
    
    # Rushing stats
    points_rushtd = Column(Float, default=6.0)  # Rushing TD
    points_rushyd = Column(Float, default=0.1)  # Rushing yard
    
    # Receiving stats
    points_rectd = Column(Float, default=6.0)  # Receiving TD
    points_recyd = Column(Float, default=0.1)  # Receiving yard
    points_reception = Column(Float, default=1.0)  # PPR (Points Per Reception)
    
    # Fumbles
    points_fumble = Column(Float, default=-2.0)  # Fumble lost
    
    # Defensive scoring
    points_sack = Column(Float, default=1.0)  # Sack
    points_int_def = Column(Float, default=2.0)  # Defensive interception
    points_fumble_def = Column(Float, default=2.0)  # Defensive fumble recovery
    points_safety = Column(Float, default=2.0)  # Safety
    points_def_td = Column(Float, default=6.0)  # Defensive TD
    points_block_kick = Column(Float, default=2.0)  # Blocked kick
    
    # Defense points allowed
    points_shutout = Column(Float, default=10.0)  # 0 points allowed
    points_1_6_pa = Column(Float, default=7.0)  # 1-6 points allowed
    points_7_13_pa = Column(Float, default=4.0)  # 7-13 points allowed
    points_14_20_pa = Column(Float, default=1.0)  # 14-20 points allowed
    points_21_27_pa = Column(Float, default=0.0)  # 21-27 points allowed
    points_28_34_pa = Column(Float, default=-1.0)  # 28-34 points allowed
    points_35plus_pa = Column(Float, default=-4.0)  # 35+ points allowed
    
    # Special teams scoring
    points_kick_return_td = Column(Float, default=6.0)  # Kick return TD
    points_punt_return_td = Column(Float, default=6.0)  # Punt return TD
    
    # Kicking stats
    points_fg_0_39 = Column(Float, default=3.0)  # Field goal 0-39 yards
    points_fg_40_49 = Column(Float, default=4.0)  # Field goal 40-49 yards
    points_fg_50plus = Column(Float, default=5.0)  # Field goal 50+ yards
    points_fg_miss = Column(Float, default=-1.0)  # Missed FG
    points_xp = Column(Float, default=1.0)  # Extra point made
    points_xp_miss = Column(Float, default=-1.0)  # Missed extra point


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)

    position = Column(String(3), nullable=False)
    team_name = Column(String, default="FA")
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)


class WeeklyStats(Base):
    __tablename__ = "weeklystats"
    
    week_num = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(week_num, player_id),
    )

    # Passing stats
    passing_tds = Column(Integer, default=0)
    passing_yds = Column(Integer, default=0)
    interceptions = Column(Integer, default=0)

    # Rushing stats
    rushing_tds = Column(Integer, default=0)
    rushing_yds = Column(Integer, default=0)

    # Receiving stats
    receiving_tds = Column(Integer, default=0)
    receiving_yds = Column(Integer, default=0)
    receptions = Column(Integer, default=0)

    # Fumbles
    fumbles_lost = Column(Integer, default=0)

    # Defensive stats
    sacks = Column(Integer, default=0)
    interceptions_def = Column(Integer, default=0)
    fumbles_recovered = Column(Integer, default=0)
    safeties = Column(Integer, default=0)
    defensive_tds = Column(Integer, default=0)
    blocked_kicks = Column(Integer, default=0)

    # Defense points allowed
    points_allowed = Column(Integer, default=0)

    # Special teams stats
    kick_return_tds = Column(Integer, default=0)
    punt_return_tds = Column(Integer, default=0)

    # Kicking stats
    fg_made_0_39 = Column(Integer, default=0)
    fg_made_40_49 = Column(Integer, default=0)
    fg_made_50plus = Column(Integer, default=0)
    fg_missed = Column(Integer, default=0)
    xp_made = Column(Integer, default=0)
    xp_missed = Column(Integer, default=0)


class TeamPlayerPerformance(Base):
    __tablename__ = "teamplayerperformance"
    week_num = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"))
    league_id = Column(Integer, ForeignKey("leagues.id"))
    starting_position = Column(String(3), default="BEN")
    fantasy_points = Column(Float(5), default=0)

    __table_args__ = (
        PrimaryKeyConstraint(week_num, player_id, league_id),
    )
    


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
        db_session.add(new_user)
        db_session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(e)
        db_session.rollback()
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
        init_db()  # Ensure tables exist
    app.run(host='0.0.0.0', port=5000, debug=True)
    


