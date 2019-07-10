from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    bookings = db.relationship('Booking', backref='booker', lazy='dynamic')
   

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Pitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pitchName = db.Column(db.String(20), nullable=False)
    bookings = db.relationship('Booking', backref = 'pitch', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.pitchName}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pitchId = db.Column(db.Integer, db.ForeignKey('pitch.id'))
    bookerId =db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, nullable=False)
    startTime = db.Column(db.Integer, nullable=False)
    endTime = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Booking {self.id} for {self.id} last for {self.duration}'





