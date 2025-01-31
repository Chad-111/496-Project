# Completely basic server app - no functionality

# Import flask and datetime module for showing date and time
from flask import Flask, jsonify
import datetime

x = datetime.datetime.now()

# Initializing flask app
app = Flask(__name__)


# Route for seeing data
@app.route('/api')
def hello_world():

    # Returning an api for showing in  reactjs
    return jsonify({
        'Name':"Joe Biden's America"
    })

    
# Running app
if __name__ == '__main__':
    app.run(debug=True)
