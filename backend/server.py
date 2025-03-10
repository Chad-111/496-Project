from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bcrypt
import requests
from sqlalchemy import PrimaryKeyConstraint, Column, ForeignKey, create_engine, Integer, String, Float, text
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


import subprocess

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend
app.config['CORS_HEADERS'] = 'Content-Type' # maybe needed for CORS? try this out
app.secret_key = "/,&R~Qh}<pl#kI@H#D&b&i>69Fhc?|"  # Change this to a secure key

# Dummy user credentials (can be stored in a database later)
USERS = {"admin": "password123"}

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password123@localhost/draftempire'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

# Define Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Increased length to 255 for safety


class League(db.Model):
    __tablename__ = 'leagues'
    id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)  # Changed team_id to id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"))
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)


class TeamPlayer(db.Model):
    __tablename__ = "teamplayers"
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))  # Fixed reference to id
    starting_position = db.Column(db.String(3), default="BEN")
    __table_args__ = (
        db.PrimaryKeyConstraint(player_id, league_id),
    )


# Matchup Model
class Matchup(db.Model):
    __tablename__ = "matchups"
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"))
    week_num = db.Column(db.Integer, default=1)
    away_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    away_team_score = db.Column(db.Float, default=0)
    home_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    home_team_score = db.Column(db.Float, default=0)

class Ruleset(db.Model):
    __tablename__ = "rulesets"
    
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"), primary_key=True)

    # Passing stats
    points_passtd = db.Column(db.Float, default=4.0)  # Passing TD
    points_passyd = db.Column(db.Float, default=0.04)  # Passing yard
    points_int = db.Column(db.Float, default=-2.0)  # Interception

    # Rushing stats
    points_rushtd = db.Column(db.Float, default=6.0)  # Rushing TD
    points_rushyd = db.Column(db.Float, default=0.1)  # Rushing yard

    # Receiving stats
    points_rectd = db.Column(db.Float, default=6.0)  # Receiving TD
    points_recyd = db.Column(db.Float, default=0.1)  # Receiving yard
    points_reception = db.Column(db.Float, default=1.0)  # PPR (Points Per Reception)

    # Fumbles
    points_fumble = db.Column(db.Float, default=-2.0)  # Fumble lost

    # Defensive scoring
    points_sack = db.Column(db.Float, default=1.0)  # Sack
    points_int_def = db.Column(db.Float, default=2.0)  # Defensive interception
    points_fumble_def = db.Column(db.Float, default=2.0)  # Defensive fumble recovery
    points_safety = db.Column(db.Float, default=2.0)  # Safety
    points_def_td = db.Column(db.Float, default=6.0)  # Defensive TD
    points_block_kick = db.Column(db.Float, default=2.0)  # Blocked kick

    # Defense points allowed
    points_shutout = db.Column(db.Float, default=10.0)  # 0 points allowed
    points_1_6_pa = db.Column(db.Float, default=7.0)  # 1-6 points allowed
    points_7_13_pa = db.Column(db.Float, default=4.0)  # 7-13 points allowed
    points_14_20_pa = db.Column(db.Float, default=1.0)  # 14-20 points allowed
    points_21_27_pa = db.Column(db.Float, default=0.0)  # 21-27 points allowed
    points_28_34_pa = db.Column(db.Float, default=-1.0)  # 28-34 points allowed
    points_35plus_pa = db.Column(db.Float, default=-4.0)  # 35+ points allowed

    # Special teams scoring
    points_kick_return_td = db.Column(db.Float, default=6.0)  # Kick return TD
    points_punt_return_td = db.Column(db.Float, default=6.0)  # Punt return TD

    # Kicking stats
    points_fg_0_39 = db.Column(db.Float, default=3.0)  # Field goal 0-39 yards
    points_fg_40_49 = db.Column(db.Float, default=4.0)  # Field goal 40-49 yards
    points_fg_50plus = db.Column(db.Float, default=5.0)  # Field goal 50+ yards
    points_fg_miss = db.Column(db.Float, default=-1.0)  # Missed FG
    points_xp = db.Column(db.Float, default=1.0)  # Extra point made
    points_xp_miss = db.Column(db.Float, default=-1.0)  # Missed extra point

# Player Model
class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(3), nullable=False)
    team_name = db.Column(db.String, default="FA")
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)


# WeeklyStats Model
class WeeklyStats(db.Model):
    __tablename__ = "weeklystats"
    week_num = db.Column(db.Integer, nullable=False, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False, primary_key=True)

    # Passing stats
    passing_tds = db.Column(db.Integer, default=0)
    passing_yds = db.Column(db.Integer, default=0)
    interceptions = db.Column(db.Integer, default=0)

    # Rushing stats
    rushing_tds = db.Column(db.Integer, default=0)
    rushing_yds = db.Column(db.Integer, default=0)

    # Receiving stats
    receiving_tds = db.Column(db.Integer, default=0)
    receiving_yds = db.Column(db.Integer, default=0)
    receptions = db.Column(db.Integer, default=0)

    # Fumbles
    fumbles_lost = db.Column(db.Integer, default=0)

    # Defensive stats
    sacks = db.Column(db.Integer, default=0)
    interceptions_def = db.Column(db.Integer, default=0)
    fumbles_recovered = db.Column(db.Integer, default=0)
    safeties = db.Column(db.Integer, default=0)
    defensive_tds = db.Column(db.Integer, default=0)
    blocked_kicks = db.Column(db.Integer, default=0)

    # Defense points allowed
    points_allowed = db.Column(db.Integer, default=0)

    # Special teams stats
    kick_return_tds = db.Column(db.Integer, default=0)
    punt_return_tds = db.Column(db.Integer, default=0)

    # Kicking stats
    fg_made_0_39 = db.Column(db.Integer, default=0)
    fg_made_40_49 = db.Column(db.Integer, default=0)
    fg_made_50plus = db.Column(db.Integer, default=0)
    fg_missed = db.Column(db.Integer, default=0)
    xp_made = db.Column(db.Integer, default=0)
    xp_missed = db.Column(db.Integer, default=0)

# TeamPlayerPerformance Model
class TeamPlayerPerformance(db.Model):
    __tablename__ = "teamplayerperformance"
    week_num = db.Column(db.Integer, nullable=False, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"), primary_key=True)
    starting_position = db.Column(db.String(3), default="BEN")
    fantasy_points = db.Column(db.Float, default=0)

    __table_args__ = (
        PrimaryKeyConstraint(week_num, player_id, league_id),
    )
    


# API Routes
@app.route('/api/')
def api_root():
    return "API is working!"

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{ 'id': u.id, 'username': u.username, 'email': u.email } for u in users])

@app.route('/api/leagues', methods=['GET'])
def get_leagues():
    leagues = League.query.all()
    return jsonify([{ 'id': l.id, 'league_name': l.league_name, 'manager_id': l.manager_id } for l in leagues])


# User Signup
@app.route('/api/signup', methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")

    if not email or not password or not username:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user already exists
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Create user
    new_user = User(username=username, password_hash=hashed_password, email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    

    
# User Login
@app.route('/api/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return jsonify({"error": "Invalid email or password"}), 401

    session["user_id"] = user.id
    return jsonify({"message": "Login successful", "username": user.username}), 200


# Test Database Connection
@app.route('/test_db')
def test_db():
    try:
        db.session.execute(text("SELECT 1"))
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {e}"

# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
    


