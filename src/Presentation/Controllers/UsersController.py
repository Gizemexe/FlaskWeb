from flask import Blueprint,jsonify,request
from datetime import datetime, timedelta

from src.Application.Features.User.Commands.ChangePasswordCommand import ChangePasswordCommand
from src.Application.Features.User.Commands.UpdateProfileCommand import UpdateProfileCommand
from src.Application.Features.User.Mapping.UserMapper import UserMapper
from src.Application.DTOs.UserDto import UserDto
from src.Application.Features.User.Queries.GetAllUserQuery import GetAllUsersQuery
from src.Application.Features.User.Queries.GetUserQuery import GetUserQuery
from src.Infrastructure.Services.UserService import UserService
from src.Infrastructure.Repositories.UserRepository import UserRepositoryImpl
from src.Application.Security.JWT import Token
from src.Domain.Entities.User import Users
from src.Infrastructure.Services.AuthService import AuthService
from src.Infrastructure.Database.database import db
from src.config import JwtSettings

users = Blueprint('users', __name__, url_prefix='/api/v1/users')

auth_Service = AuthService()
user_repository = UserRepositoryImpl()
user_service = UserService(user_repository)

# get all users
@users.route("/GetAll", methods=["GET"])
def get_users():
    query = GetAllUsersQuery(user_repository)
    users = query.execute()
    return jsonify([user.__dict__ for user in users])


# get specific user
@users.route("/Get", methods=["GET"])
def get_user():
    token = request.headers.get('Authorization')
    print("Received token:", token)
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    jwt_token = token.split('Bearer ')[1]
    print("JWT token:", jwt_token)

    user_id = Token.get_user_id(jwt_token)

    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    user_repository = UserRepositoryImpl()
    query = GetUserQuery(user_repository)
    user_dto = query.execute(user_id)

    if user_dto:
        user_response = UserMapper.to_response(user_dto)
        return jsonify(user_response), 200
    else:
        return jsonify({'message': 'User not found'}), 404


# post users
@users.route("/Register", methods=["POST"])
def register():
    user_data = request.json
    print("Received user data:", user_data)

    refresh_token = Token.create_refresh_token()
    refresh_token_end_date = datetime.utcnow() + timedelta(days=7)

    print("Generated refresh token:", refresh_token)

    # Kullanıcı adı ve e-posta adresini al
    username = user_data.get("username")
    email = user_data.get("email")                    #its working
    password = user_data.get("password")

    print("Username:", username)
    print("Email:", email)
    print("Password:", password)

    # Şifre kontrolü eklendi
    if not password:
        return jsonify("Password field is required!"), 400

    if user_service.get_user_by_username(username) is not None:
        return jsonify("Username already exists!"), 403
    if user_service.get_user_by_email(email) is not None:
        return jsonify("Email already exists!"), 403

    new_user_dto = UserDto(
        id=None,
        username=username,
        email=email,
        phone=None,
        birth_day=None,
        password=password,
        created_at=None,
        updated_at=None
    )

    new_user = UserMapper.from_dto(new_user_dto)
    new_user.RefreshToken = refresh_token
    new_user.RefreshTokenEndDate = refresh_token_end_date

    print("New user:", new_user)

    user_service.create_user(new_user)

    return jsonify({
        "message": "User registered successfully",
        "access_token": auth_Service.CreateAccessToken(user=new_user, jwtSettings=JwtSettings)
    }), 200

@users.route("/UpdateProfile", methods=["PUT"])
def update_profile():
    # Authorization başlığından token al
    token = request.headers.get('Authorization')
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    # Bearer tokeni JWT'den ayır
    jwt_token = token.split('Bearer ')[1]

    # Kullanıcı ID'sini token üzerinden al
    user_id = Token.get_user_id(jwt_token)
    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    # Güncellenmiş kullanıcı bilgilerini JSON'dan al
    user_data = request.json
    username = user_data.get('username')
    email = user_data.get('email')
    phone = user_data.get('phone')
    birthDay = user_data.get('birthDay')

    if not username or not email:
        return jsonify({'message': 'Username and email are required.'}), 400

    # Veritabanından kullanıcıyı getir
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    try:
        command = UpdateProfileCommand(user_id, username, email, phone, birthDay)
        user_service = UserService(UserRepositoryImpl())
        user_service.update_profile(command)
        return jsonify({'message': 'Profile updated successfully'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        print('Error updating profile:', e)
        return jsonify({'message': 'Failed to update profile'}), 500

@users.route("/ChangePassword", methods=["PUT"])
def change_password():
    # Get the JWT token from the request header
    token = request.headers.get('Authorization')
    if token is None or not token.startswith('Bearer '):
        return jsonify({'message': 'Unauthorized'}), 401

    # Extract the JWT token from the 'Bearer' token
    jwt_token = token.split('Bearer ')[1]
    user_id = Token.get_user_id(jwt_token)
    if user_id is None:
        return jsonify({'message': 'Invalid token'}), 401

    # Get the current password, new password, and confirmation from the request body
    user_data = request.json
    current_password = user_data.get('current_password')
    new_password = user_data.get('new_password')

    # Validate that all fields are provided
    if not current_password or not new_password:
        return jsonify({'message': 'All fields are required.'}), 400

    try:
        # Create and handle the command
        command = ChangePasswordCommand(user_id=user_id, current_password=current_password, new_password=new_password)
        user_service = UserService(UserRepositoryImpl())
        user_service.change_password(command)
        return jsonify({'message': 'Password updated successfully.'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of error
        print('Error updating password:', e)
        return jsonify({'message': 'Failed to update password.'}), 500
