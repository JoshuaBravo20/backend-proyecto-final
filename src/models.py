from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id=db.Column(db.String(100), primary_key=True)
    name=db.Column(db.String(120), unique=False, nullable=False)
    email=db.Column(db.String(120), unique=False, nullable=False)
    followers=db.Column(db.Integer, nullable=True)
    posts = db.relationship('Chat', backref='user')

    def serialize(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "followers": self.followers
        }
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

""" class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    users_id = db.Column(db.String(100), db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False) 

    def serialize(self):
        return {
            "id": self.id,
            "message": self.message
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit() """
    
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    commentary=db.Column(db.String(120), nullable=False)
    users_id = db.Column(db.String(100), db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False) 

    def serialize(self):
        return {
            "id": self.id,
            "commentary": self.commentary
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()