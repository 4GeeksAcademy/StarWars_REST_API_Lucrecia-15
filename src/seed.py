from app import app
from models import db, Planets


with app.app_context():
    p1= Planets( name = "Tatooine")
    p2= Planets( name = "Coruscant")

    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
    
