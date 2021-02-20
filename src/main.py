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
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

""" @app.route("/")
def root():
    return render_template('index.html') """
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/api/users', methods=['GET', 'POST'])
@app.route('/api/user/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def user(id = None):
    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id)
            if not user: return jsonify({"msg": "User not found"}), 404
            return jsonify(user.serialize()), 200
        else:
            user = User.query.all()
            user = list(map(lambda user: user.serialize(), user))
            return jsonify(user), 200

   
    if request.method == 'POST':
        user_id = request.json.get("user_id")
        name = request.json.get("name")
        email = request.json.get("email")
        followers = request.json.get("followers")

        if not user_id: return jsonify({"msg": "user_id is required"}), 400
        if not name: return jsonify({"msg": "name is required"}), 400
        if not email: return jsonify({"msg": "email is required"}), 400

        user2 = User.query.filter_by(email=email).first()
        if user2: return jsonify({"msg": "email already exists"}), 400

        user = User()
        user.user_id = user_id
        user.name = name
        user.email = email
        user.followers = followers
        user.save()
        return jsonify(user.serialize()), 201

    if request.method == 'PUT':
        name = request.json.get("name")
        email = request.json.get("email")
        followers = request.json.get("followers")
        print(followers)

        if not name: return jsonify({"msg": "name is required"}), 400
        if not email: return jsonify({"msg": "email is required"}), 400


        user = User.query.get(id)
        user.name = name
        user.email = email
        user.followers = followers
        user.update()

        user2 = User.query.filter_by(email=email).first()
        if user2 and user2.user_id != id: return jsonify({"msg": "email already exists"}), 400
        
        return jsonify(user.serialize()), 200    

    if request.method == 'DELETE':
        user = User.query.get(id)
        if not user: return jsonify({"msg": "User not found"}), 404
        user.delete()
        return jsonify({"result": "User has deleted"}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=PORT, debug=False)
