# config.py
import os
class JwtSettings:
    Issuer = "myapp.com"
    Audience = "myapi"
    SigningKey = os.environ.get("JWT_SIGNING_KEY")

class Config:

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = os.environ.get('API_KEY')
