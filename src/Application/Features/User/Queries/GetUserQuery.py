from src.Application.Features.User.Mapping.UserMapper import UserMapper
from src.Infrastructure.Repositories.UserRepository import UserRepositoryImpl

class GetUserQuery:
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository

    def execute(self, user_id):
        user = self.user_repository.get(user_id)
        if user:
            return UserMapper.to_dto(user)
        return None
