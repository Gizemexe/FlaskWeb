import json
import jwt
import datetime
import secrets
import base64
from typing import Optional
from src.config import JwtSettings


def get_user_id(token: str) -> Optional[str]:
    try:
        # Tokeni "." karakterine göre ayır
        parts = token.split('.')
        # Başlık (header) ve yük (payload) ayrıştırması
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '==').decode('utf-8'))
        # payload'tan "userid" değerini döndür
        return payload.get("userid")
    except (IndexError, ValueError, TypeError):
        return None

def create_refresh_token() -> str:
    random_bytes = secrets.token_bytes(32)
    return secrets.token_urlsafe(32)

def get_jwt_token(email: str, jwt_settings: JwtSettings, expiration: datetime.timedelta, additional_claims=None) -> str:
    if additional_claims is None:
        additional_claims = {}
    # Payload bilgileri
    payload = {
        "unique_name": email,
        "exp": datetime.datetime.utcnow() + expiration,  # Expiration time
        **additional_claims
    }
    # Gizli anahtarı base64 encode et
    encoded_secret_key = base64.b64encode(jwt_settings.SigningKey.encode('utf-8')).decode('utf-8')

    # Header bilgileri
    header = {
        "typ": "JWT",
        "alg": "HS256",
        "iss": jwt_settings.Issuer,
        "aud": jwt_settings.Audience,
    }
    # JWT token oluşturma
    token = jwt.encode(
        payload=payload,
        key=encoded_secret_key,
        algorithm="HS256",
        headers=header,
    )
    return token
