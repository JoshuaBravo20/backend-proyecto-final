from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id=db.Column(db.String(100), primary_key=True)
    name=db.Column(db.String(120), unique=False, nullable=False)
    email=db.Column(db.String(120), unique=False, nullable=False)
    followers=db.Column(db.Integer, nullable=True)
    photo = db.Column(db.String(255), nullable=False)
    recentTracks = db.Column(db.PickleType, nullable = False)
    topArtists = db.Column(db.PickleType, nullable = False)
    posts = db.relationship('Post', cascade="all,delete", backref='user')
    chats = db.relationship('Chat', cascade="all,delete", backref='user')
    #notificationLikes = db.relationship('NotificationLike', cascade="all,delete", backref='user')
    friends = db.relationship('Friend', cascade="all,delete", backref='user')
    likes = db.relationship('LikesPost', cascade="all,delete", backref='user')
    commentsPost = db.relationship('CommentaryPost', cascade="all,delete", backref='user')

    def serialize(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "followers": self.followers,
            "photo": self.photo,
            "recentTracks": self.recentTracks,
            "topArtists": self.topArtists
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.PickleType)
    user_id = db.Column(db.String(100), db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False) 

    def serialize(self):
        return {
            "id": self.id,
            "message": self.message,
            "user_id": self.user_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    commentary = db.Column(db.String(120), nullable=False)
    image  = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(120), db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    likes = db.relationship('LikesPost', cascade="all,delete", backref='posts') 
    commentaryPost = db.relationship('CommentaryPost', cascade="all,delete", backref='posts') 

    def serialize(self):
        return {
            "id": self.id,
            "commentary": self.commentary,
            "image": self.image,
            "user_id": self.user_id,
            "name": self.user.name,
            "photo": self.user.photo
        }


    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class LikesPost(db.Model):
    __tablename__ = 'likespost'
    id = db.Column(db.Integer, primary_key=True)
    likes  = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id',ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False) 

    def serialize(self):
        return {
            "id": self.id,
            "likes": self.likes,
            "active": self.active,
            "user_id": self.user_id,
            "post_id": self.post_id
        }


    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class CommentaryPost(db.Model):
    __tablename__ = 'commentsPost'
    id = db.Column(db.Integer, primary_key=True)
    commentary  = db.Column(db.String(250), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id',ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False) 

    def serialize(self):
        return {
            "id": self.id,
            "commentary": self.commentary,
            "post_id": self.post_id,
            "user_id": self.user_id
        }


    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Friend(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key=True)
    personId = db.Column(db.String(250), nullable=False)
    friends = db.Column(db.String(250), nullable=False) 
    photo = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.String(120), db.ForeignKey('user.user_id', ondelete='CASCADE')) 

    def serialize(self):
        return {
           
            "friends": self.friends,
            "user_id": self.user_id,
            "personId": self.personId,
            "photo": self.photo
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# class NotificationLike(db.Model):
#     __tablename__ = 'notificationLikes'
    
#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.String(250), nullable=False) 
#     active = db.Column(db.Boolean)
#     personId = db.Column(db.String(250), nullable=False)
#     user_id = db.Column(db.String(120), db.ForeignKey('user.user_id', ondelete='CASCADE')) 

#     def serialize(self):
#         return {
           
#             "message": self.message,
#             "personId": self.personId,
#             "active": self.active,
#             "user_id": self.user_id,
#         }

#     def save(self):
#         db.session.add(self)
#         db.session.commit()
    
#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()