from datetime import datetime
from src.Infrastructure.Database.database import db


class Products(db.Model):
    __tablename__ = 'Products'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Code = db.Column(db.String(180), unique=True, nullable=False)
    Description = db.Column(db.String(180), nullable=True)
    Price = db.Column(db.Integer, nullable=False)
    Image = db.Column(db.String(180), nullable=False)
    Stock = db.Column(db.Integer, nullable=False)
    CategoryId = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


