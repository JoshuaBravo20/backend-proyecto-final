"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, render_template
from flask_socketio import SocketIO
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Post, Chat
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secreto'
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app, cors_allowed_origins='*') # Inicializar Socket

db.init_app(app)
MIGRATE = Migrate(app, db)
CORS(app)
setup_admin(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints

@socketio.on('connected')
def connected(data):
    print(data)

@socketio.on('json')
def get_message(json, method='POST'):
    print("message", json)

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
        photo = request.json.get("photo")
        recentTracks = request.json.get("recentTracks")
        topArtists = request.json.get("topArtists")

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
        user.photo = photo
        user.recentTracks = recentTracks
        user.topArtists = topArtists
        user.save()
        return jsonify(user.serialize()), 201

    if request.method == 'PUT':
        name = request.json.get("name")
        email = request.json.get("email")
        followers = request.json.get("followers")
        photo = request.json.get("photo")
        recentTracks = request.json.get("recentTracks")
        topArtists = request.json.get("topArtists")

        if not name: return jsonify({"msg": "name is required"}), 400
        if not email: return jsonify({"msg": "email is required"}), 400


        user = User.query.get(id)
        user.name = name
        user.email = email
        user.followers = followers
        user.photo = photo
        user.recentTracks = recentTracks
        user.topArtists = topArtists
        user.update() 

        user2 = User.query.filter_by(email=email).first()
        if user2 and user2.user_id != id: return jsonify({"msg": "email already exists"}), 400
        
        return jsonify(user.serialize()), 200    

    if request.method == 'DELETE':
        user = User.query.get(id)
        if not user: return jsonify({"msg": "User not found"}), 404
        user.delete()
        return jsonify({"result": "User has been deleted"}), 200

@app.route('/api/posts', methods=['GET', 'POST'])
@app.route('/api/post/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def posts(id = None):
    if request.method == 'GET':
        if id is not None:
            post = Post.query.get(id)
            if not post: return jsonify({"msg": "Post not found"}), 404
            return jsonify(post.serialize()), 200
        else:
            post = Post.query.all()
            post = list(map(lambda post: post.serialize(), post))
            return jsonify(post), 200

   
    if request.method == 'POST':
        commentary = request.json.get("commentary")
        user_id = request.json.get("user_id")
        
        if not commentary: return jsonify({"msg": "commentary is required"}), 400
        if not user_id: return jsonify({"msg": "commentary is required"}), 400

        post = Post()
        post.commentary = commentary
        post.user_id = user_id

        post.save()

        return jsonify(post.serialize()), 201

    """ if request.method == 'PUT':
        commentary = request.json.get("commentary")
        user_id = request.json.get("user_id")

        if not commentary: return jsonify({"msg": "Commentary is required"}), 400
        if not user_id: return jsonify({"msg": "Commentary is required"}), 400


        post = Post.query.get(id)
        post.commentary = commentary
        post.user_id = user_id
        post.update()

                
        return jsonify(post.serialize()), 200    """

    if request.method == 'DELETE':
        post = Post.query.get(id)
        if not post: return jsonify({"msg": "Post not found"}), 404
        post.delete()
        return jsonify({"result": "Post has been deleted"}), 200 

    
@app.route('/api/chats', methods=['GET', 'POST'])
@app.route('/api/chat/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def chats(id = None):
    if request.method == 'GET':
        if id is not None:
            chat = Chat.query.get(id)
            if not chat: return jsonify({"msg": "chat not found"}), 404
            return jsonify(chat.serialize()), 200
        else:
            chat = Chat.query.all()
            chat = list(map(lambda chat: chat.serialize(), chat))
            return jsonify(chat), 200

   
    if request.method == 'POST':
        user_id = request.json.get("user_id")
        message = request.json.get("message")
        
        
        if not message: return jsonify({"msg": "message is required"}), 400
        if not user_id: return jsonify({"msg": "message is required"}), 400

        chat = Chat()
        chat.user_id = user_id
        chat.message = message
        chat.save()

        return jsonify(chat.serialize()), 201
   
    if request.method == 'DELETE':
        chat = Chat.query.get(id)
        if not chat: return jsonify({"msg": "Chat not found"}), 404
        chat.delete()
        return jsonify({"result": "Chat has been deleted"}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=PORT, debug=False)
