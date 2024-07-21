from datetime import datetime
from src.Infrastructure.Database.database import db

class OrderDetails(db.Model):
    __tablename__ = 'OrderDetails'
    Id = db.Column(db.Integer, primary_key=True)
    OrderId = db.Column(db.Integer, db.ForeignKey('Orders.Id'), nullable=False)
    ProductId = db.Column(db.Integer, nullable=False)
    Quantity = db.Column(db.Float, nullable=False)
    UnitPrice = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())