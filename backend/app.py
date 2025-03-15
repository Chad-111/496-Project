from flask import Flask, jsonify, send_from_directory, Response
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="../frontend/dist")  # Adjust if needed
CORS(app)  # Enable CORS for all routes

@app.route('/api/message')
def get_message():
    response = jsonify({"message": "Hello from Flask!"})
    response.headers["Content-Type"] = "application/json"
    return response

# Serve React Frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == '__main__':
    app.run(debug=True)
