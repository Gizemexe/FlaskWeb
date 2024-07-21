from datetime import datetime
from src.Infrastructure.Database.database import db


class Carts(db.Model):
    __tablename__ = 'Carts'
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.String(50), nullable=False)
    ProductId = db.Column(db.String(180), nullable=True)
    Quantity = db.Column(db.String(180), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
