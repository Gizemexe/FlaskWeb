from src.config import JwtSettings
from src.Domain.Entities import User
from src.Application.Security.JWT import Token
from datetime import timedelta

class AuthService:
    @staticmethod
    def CreateAccessToken(user: User, jwtSettings: JwtSettings) -> str:
        claims = {
            "userid": str(user.Id),
            "email": user.Email,
            "displayname": user.Username
        }

        # JWT tokeni oluşturma
        accesstoken = Token.get_jwt_token(user.Email, jwtSettings, timedelta(days=7), claims)

        return accesstoken
