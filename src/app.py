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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    people_list = [person.serialize() for person in people]
    return jsonify({"people": people_list}), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify({"msg": "The character is getting by id", "data": person.serialize()}), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_list = [planet.serialize() for planet in planets]
    return jsonify({"planets": planets_list}), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify({"msg": "The planet is getting by id", "data": planet.serialize()}), 200

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [user.serialize() for user in users]
    return jsonify({"users": users_list}), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    favorite_characters = [favorite.serialize() for favorite in user.favourite_characters]
    favorite_planets = [favorite.serialize() for favorite in user.favourite_planets]
    favorite_vehicles = [favorite.serialize() for favorite in user.favourite_vehicles]

    return jsonify({
        "favorite_characters": favorite_characters,
        "favorite_planets": favorite_planets,
        "favorite_vehicles": favorite_vehicles
    }), 200

@app.route('/user', methods=['POST'])
def create_user():
    body = request.json
    new_user = User(
        email=body.get("email"),
        password=body.get("password"),
        username=body.get("username"),
        is_active=body.get("is_active", True)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "The user has been successfully created"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.headers.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({'error': 'Planet not found'}), 404

    if any(favorite.planet_id == planet_id for favorite in user.favourite_planets):
        return jsonify({'error': 'Planet is already in the list of favorites'}), 400

    new_favorite = FavouritesPlanets(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'message': f'The planet {planet.name} has been added to {user.username}\'s favorites list'}), 200

@app.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    user_id = request.headers.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    person = People.query.get(person_id)
    if not person:
        return jsonify({'error': 'Person not found'}), 404

    if any(favorite.character_id == person_id for favorite in user.favourite_characters):
        return jsonify({'error': 'Person is already in the list of favorites'}), 400

    new_favorite = FavouritesCharacters(user_id=user_id, character_id=person_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'msg': f'The character {person.name} has been added to {user.username}\'s favorites list'}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.headers.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    favorite = FavouritesPlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({'error': 'Planet is not in the list of favorites'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': f'The planet with ID {planet_id} has been removed from {user.username}\'s favorites list.'}), 200

@app.route('/favorite/person/<int:person_id>', methods=['DELETE'])
def delete_favorite_person(person_id):
    user_id = request.headers.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    favorite = FavouritesCharacters.query.filter_by(user_id=user_id, character_id=person_id).first()
    if not favorite:
        return jsonify({'error': 'Character is not in the list of favorites'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': f'The character with ID {person_id} has been removed from {user.username}\'s favorites list.'}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
