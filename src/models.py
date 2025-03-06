from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    people_favorite = db.relationship('people_favorite', backref="user")
    planets_favorites = db.relationship('planets_favorites', backref="user")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    planets_favorites = db.relationship('planets_favorites', backref="planets")
    
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.name,
            "planets_favorites": [fav.serialize() for fav in self.planets_favorites],
        }
    
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    people_favorite = db.relationship('people_favorite', backref="people")

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.name,
            "people_favorite": [fav.serialize() for fav in self.people_favorite],
        }
    

class people_favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    people_id = db.Column(db.Integer, db.ForeignKey(People.id))
    people = db.relationship('People', backref='people_favorite', lazy=True)

    def __repr__(self):
        return '<characters_favorites %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "people": self.people.serialize()
        }

class planets_favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    planet_id = db.Column(db.Integer, db.ForeignKey(Planets.id))
    planet = db.relationship('Planets', backref='planets_favorites', lazy=True)
    
    def __repr__(self):
        return '<planets_favorites %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet": self.planet.serialize()
        }
