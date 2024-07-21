from src.Infrastructure.Repositories.UserRepository import UserRepositoryImpl
from src.Infrastructure.Services.UserService import UserService
from src.Domain.Entities.User import Users
from src.Application.DTOs.UserDto import UserDto

class UserMapper:
    @staticmethod
    def to_dto(user: Users) -> UserDto:
        return UserDto(
            id=user.Id,
            username=user.Username,
            email=user.Email,
            phone=user.Phone,
            birth_day=user.BirthDay,
            password=user.Password,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    @staticmethod
    def from_dto(user_dto: UserDto) -> Users:
        user = Users(
            Username=user_dto.username,
            Email=user_dto.email,
            Phone=user_dto.phone,
            BirthDay=user_dto.birth_day,
            created_at=user_dto.created_at,
            updated_at=user_dto.updated_at
        )
        if user_dto.password:
            user_repository = UserRepositoryImpl()
            user_service = UserService(user_repository)
            user_service.set_password(user, user_dto.password)
        return user


    def to_response(user_dto: UserDto) -> dict:
        return {
            "id": user_dto.id,
            "username": user_dto.username,
            "email": user_dto.email,
            "phone": user_dto.phone,
            "birthDay": user_dto.birth_day.isoformat() if user_dto.birth_day else None,
            "created_at": user_dto.created_at.isoformat() if user_dto.created_at else None,
            "updated_at": user_dto.updated_at.isoformat() if user_dto.updated_at else None
        }
