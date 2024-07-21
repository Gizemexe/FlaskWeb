from src.Application.Features.User.Mapping.UserMapper import UserMapper
from src.Infrastructure.Repositories.UserRepository import UserRepositoryImpl

class GetAllUsersQuery:
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository

    def execute(self):
        users = self.user_repository.get_all()
        return [UserMapper.to_dto(user) for user in users]
