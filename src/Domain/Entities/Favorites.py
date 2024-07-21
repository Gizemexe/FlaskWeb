from datetime import datetime
from src.Infrastructure.Database.database import db


class Favorites(db.Model):
    __tablename__ = 'Favorites'
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, nullable=False)
    ProductId = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
