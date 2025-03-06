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
from models import db, User, people_favorite
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


@app.route('users/favorites', methods=['GET'])
def get_user_favorites():
    request_body = request.get_json()
    user= User.query.filter_by(id = request_body["user_id"]).first()
    if not user:
         return jsonify({"error": "User nos found"}), 404
    return jsonify({"people_favorite": [fav.serialize() for fav in user.people_favorite], "planets_favorites": [fav.serialize() for fav in user.planets_favorites]})

@app.route('favorite/people/<int:people_id>', methods=['POST', 'DELETE'])
def handle_favorite_people(id):
    if request.method == 'POST':
        request_body = request.get_json()
        existing_favorite = people_favorite.query.filter_by(user_id = request_body["user_id"], people_id = id).first()
        if existing_favorite:
            return jsonify({"msg": "favorite character already exist"}), 404
        new_favorite = people_favorite(user_id = request_body["user_id"], people_id = id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite character added", "new_favorite": new_favorite.serialize()}), 201







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

