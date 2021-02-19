from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    followers = db.Column(db.Integer, nullable=True)
    """ chats = db.relationship('Chat', backref='user') """

    def serialize(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "followers": self.followers
            # do not serialize the password, its a security breach
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

""" class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100))
    users_id = db.Column(db.String(100), db.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False) """