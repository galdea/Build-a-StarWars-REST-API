"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from flask import jsonify, request
from models import db, User, Favorites, Character, Planet
#from models import Person

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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.serialize()), 200

@app.route('/users/', methods=['POST'])
def create_user():
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    user = User(firstname=firstname, lastname=lastname, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

@app.route('/favorites/', methods=['GET'])
def get_favorites():
    favorites = Favorites.query.all()
    return jsonify([f.serialize() for f in favorites]), 200

@app.route('/favorites/<int:favorite_id>', methods=['GET'])
def get_favorite(favorite_id):
    favorite = Favorites.query.filter_by(id=favorite_id).first()
    return jsonify(favorite.serialize()), 200

@app.route('/favorites/', methods=['POST'])
def create_favorite():
    user_id = request.json.get('user_id')
    character_id = request.json.get('character_id')
    planet_id = request.json.get('planet_id')
    favorite = Favorites(user_id=user_id, character_id=character_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/characters/', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([c.serialize() for c in characters]), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.filter_by(id=character_id).first()
    return jsonify(character.serialize()), 200

@app.route('/planets/', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    return jsonify(planet.serialize()), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
