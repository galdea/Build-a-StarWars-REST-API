import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, People, Planet, Vehicle

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

with app.app_context():
    db.create_all()

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get, Post and Delete User
@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    response_user = [user.serialize() for user in users]
    response_body = {
        "msg": "User list"
    }

    return jsonify(response_user), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def select_user(user_id):
    user = User.query.get(user_id)
    user = user.serialize()
    return jsonify(user), 200

# Get, Post and Delete People
@app.route('/people', methods=['GET'])
def handle_people():
    peoples = People.query.all()
    result_people = [people.serialize() for people in peoples]
    return jsonify(result_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def select_people(people_id):
    person = People.query.get(people_id)
    person = person.serialize()
    return jsonify(person), 200

@app.route('/people', methods=['POST'])
def create_people():
    data = request.data
    data = json.loads(data)

    person = People(name = data['name'], mass = data['mass'])
    db.session.add(person)
    db.session.commit()
    response_body = {
        "msg": "The force is strong on this one! "
    }
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person_delete = People.query.get(people_id)
    db.session.delete(person_delete)
    db.session.commit()

    response_body = {
        "msg": "The force was week on this one! "
    }
    return jsonify(response_body), 200

# Get, Post and Delete Planets
@app.route('/planet', methods=['GET'])
def handle_planet():
    planets = Planet.query.all()
    result = [planet.serialize() for planet in planets]
    return jsonify(result), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def select_planet(planet_id):
    planet = Planet.query.get(planet_id)
    planet = planet.serialize()
    return jsonify(planet), 200

@app.route('/planet', methods=['POST'])
def create_planet():  
    data = request.data
    data = json.loads(data)

    planet = Planet(name = data['name'], rotation_period = data['rotation_period'])
    db.session.add(planet)
    db.session.commit()
    response_body = {
        "msg": "Planet survives! "
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id): 
    planet_delete = Planet.query.get(planet_id)
    db.session.delete(planet_delete)
    db.session.commit()
    
    response_body = {
        "msg": "Planet destroyed by Death Star! "
    }
    return jsonify(response_body), 200    

# Get, Post and Delete Vehicles
@app.route('/vehicle', methods=['GET'])
def handle_vehicle():
    vehicles = Vehicle.query.all()
    result = [vehicle.serialize() for vehicle in vehicles]
    return jsonify(result), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def select_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    vehicle = vehicle.serialize()
    return jsonify(vehicle), 200

@app.route('/vehicle', methods=['POST'])
def create_vehicle():  
    data = request.data
    data = json.loads(data)

    vehicle = Vehicle(name = data['name'], model = data['model'])
    db.session.add(vehicle)
    db.session.commit()
    response_body = {
        "msg": "Vehicle running"
    }
    return jsonify(response_body), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id): 
    vehicle_delete = Vehicle.query.get(vehicle_id)
    db.session.delete(vehicle_delete)
    db.session.commit()
    
    response_body = {
        "msg": "Vehicle deleted! "
    }
    return jsonify(response_body), 200   

# Get, post and delete Favorites
@app.route('/favorite', methods=['GET'])
def handle_fav():
    favorites = Favorites.query.all()
    fav = [favorite.serialize() for favorite in favorites]

    return jsonify(fav), 200

@app.route('/favorite/<int:id>', methods=['GET'])
def select_fav(id):
    fav = Favorites.query.filter_by(user_id = id).all()
    favorite_user = [favorite.serialize() for favorite in fav]
    print(fav)
    return jsonify(favorite_user), 200

@app.route('/favorite', methods=['POST'])
def new_fav_planet():  
    data = request.data
    data = json.loads(data)

    fav = Favorites(user_id = data['user_id'], planet_id = data['planet_id'], vehicle_id = data('vehicle_id'))
    db.session.add(fav)
    db.session.commit()
    response_body = {
        "msg": "Love these guys! "
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3010))
    app.run(host='0.0.0.0', port=PORT, debug=False)