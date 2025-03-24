from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    people_favorites = db.relationship('people_favorite', backref="user")
    planets_favorites = db.relationship('planets_favorites', backref="user")

    def __repr__(self):
        return '<User %r>' % self.email 

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.name,
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.name,
        }
    
class people_favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    people_id = db.Column(db.Integer, db.ForeignKey(People.id))
    people = db.relationship('People', backref='favorites_people')

    def __repr__(self):
        return '<people_favorite %r>' % self.id  

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            
        }

class planets_favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    planet_id = db.Column(db.Integer, db.ForeignKey(Planets.id))
    planet = db.relationship('Planets', backref='favorites_planets')
    
    def __repr__(self):
        return '<planets_favorites %r>' % self.id  

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }