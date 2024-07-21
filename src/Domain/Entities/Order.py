from datetime import datetime
from src.Infrastructure.Database.database import db


class Orders(db.Model):
    __tablename__ = 'Orders'
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, nullable=False)
    OrderNumber = db.Column(db.String(180), nullable=False)
    Total = db.Column(db.Integer, nullable=True)
    Address = db.Column(db.String(180), nullable=True)
    Status = db.Column(db.String(50), nullable=True, default='Hazırlanıyor')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


    def save(self):
        db.session.add(self)
        db.session.commit()