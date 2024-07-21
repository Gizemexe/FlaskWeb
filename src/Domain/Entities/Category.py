from datetime import datetime
from src.Infrastructure.Database.database import db


class Categories(db.Model):
    __tablename__ = 'Categories'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Image = db.Column(db.String(180), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
