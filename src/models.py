from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favourite_characters = db.relationship('FavouritesCharacters', backref='user', lazy=True)
    favourite_planets = db.relationship('FavouritesPlanets', backref='user', lazy=True)
    favourite_vehicles = db.relationship('FavouritesVehicles', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column (db.String(120), nullable=False)
    eye_color = db.Column(db.String(10))
    hair_color = db.Column(db.String(10))

    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "hair_color": self.eye_color,
        }
    

    class Planets (db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name= db.Column (db.String(120), nullable=False)


        def serialize(self):
            return {
             "id" : self.id,
             "name": self.name
            }
    

    class Vehicles(db.Model):
     id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
        }


class FavouritesCharacters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class FavouritesPlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

class FavouritesVehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id
        }
