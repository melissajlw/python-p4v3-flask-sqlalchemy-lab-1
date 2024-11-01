# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here

# View get_earthquake(id)
# Queries the database to get the earthquake with that id
# Params: integer that represents an id
# Returns: a response containing the model attributes and values formatted as a JSON string or an error message if no row is found
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    
    if earthquake:
        body = earthquake.to_dict()
        status = 200
    else:
        body = {"message" : f"Earthquake {id} not found."}
        status = 404

    return make_response(body, status)

# View get_magnitude_earthquake(magnitude)
# Queries the database to get all earthquakes with magnitude greater than or equal to the parameter value
# Params: flat representing a magnitude
# Returns: JSON response containing the count of matching rows along with a list containing data for each row
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_magnitude_earthquake(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    earthquakes_list = [earthquake.to_dict() for earthquake in earthquakes]

    body = {"count" : len(earthquakes),
            "quakes" : earthquakes_list}
    
    return make_response(body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
