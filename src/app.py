"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, FavouritesCharacters, FavouritesPlanets, FavouritesVehicles


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

@app.route('/people', methods=['GET'])
def get_people():
    people = people.query.all()
    people_list = [person.serialize() for person in people]

    response_body = {
        "people" : people_list
    }

    return jsonify(response_body), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    person = person.query.filter_by(id=people_id).first()
    person_serialize= person.serialize()

    response_body= {
        "msg" : "the character is getting by id",
        "data" : person_serialize
    }

    return jsonify(response_body), 200



@app.route('/planets', methods=['GET'])
def get_planets():
    planets = planets.query.all()
    planets_list = [planet.serialize() for planet in planets]

    response_body = {
        "msg": "All planets are getting "
    }

    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = planet.query.filter_by(id=planet_id).first()
    planet_serialize= planet.serialize()

    response_body= {
        "msg" : "the planet is getting by id",
        "data" : planet_serialize
    }

    return jsonify(response_body), 200


@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [user.serialize() for user in users]

    response_body = {
        "users" :users_list
    }

    return jsonify(response_body), 200


@app.route('/user/<int:user_id>favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = user.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    

    favorite_characters = [favorite.serialize() for favorite in user.favourite_characters]
    favorite_planets = [favorite.serialize() for favorite in user.favourite_planets]
    favorite_vehicles = [favorite.serialize() for favorite in user.favourite_vehicles]

    
    response_body = {
        "favorite_characters": favorite_characters,
        "favorite_planets" : favorite_planets,
        "favorite_vehicles": favorite_vehicles
    }

    return jsonify(response_body), 200


@app.route('/user/', methods=['POST'])
def create_user():
    body =request.json
    me = User(email=body["email"], password = body["password"], us_active=body["is_active"])
    db.session.add(me)
    db.session.commit()

    response_body= {
        "msg" : "The user has been successfully created"
     }
    return jsonify(response_body), 200
    
                


        




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
