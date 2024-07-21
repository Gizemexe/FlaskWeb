from datetime import datetime
from flask_bcrypt import Bcrypt
from src.Infrastructure.Database.database import db


class Users(db.Model):
    __tablename__ = 'Users'
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Email = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(180), nullable=False)
    BirthDay = db.Column(db.Date, unique=False, nullable=True)
    Phone = db.Column(db.String(50), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    RefreshToken = db.Column(db.String(180), onupdate=datetime.now())
    RefreshTokenEndDate = db.Column(db.DateTime, onupdate=datetime.now())

    bcrypt = Bcrypt()

    def __repr__(self):
        return '<User {}>'.format(self.Username)

    def save(self):
        db.session.add(self)
        db.session.commit()
