from flask_bcrypt import Bcrypt
from flask import Blueprint,jsonify,request
from src.Domain.Entities.User import Users
from src.Infrastructure.Services.AuthService import AuthService
from src.config import JwtSettings

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

auth_Service = AuthService()
bcrypt = Bcrypt()
def get_user(email):
    user = Users.query.filter_by(Email=email).first()
    return user

@auth.route('/Login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = get_user(email)
    print(user)
    print("password:",password)

    if not user or not bcrypt.check_password_hash(user.Password, password):
        return jsonify({'access_token': None}), 401

    access_token = auth_Service.CreateAccessToken(user= user, jwtSettings=JwtSettings)  # AuthService sınıfındaki metodun çağrısı
    return jsonify({'access_token': access_token}), 200
