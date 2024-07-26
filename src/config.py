# config.py
import os
class JwtSettings:
    Issuer = "myapp.com"
    Audience = "myapi"
    SigningKey = os.environ.get("JWT_SIGNING_KEY")

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sqlserver:JzOTAk-}h"jPpBC0@35.242.208.225/Deneme'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = os.environ.get('API_KEY')