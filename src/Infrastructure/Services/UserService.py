from src.Application.Features.User.Commands.ChangePasswordCommand import ChangePasswordCommand
from src.Application.Features.User.Commands.UpdateProfileCommand import UpdateProfileCommand
from src.Domain.Entities.User import Users
from src.Infrastructure.Repositories.UserRepository import UserRepositoryImpl
from src.Application.Utilities.utils import normalize_phone_number


class UserService:
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository

    def get_user_by_username(self, username):
        return self.user_repository.get_by_username(username)

    def get_user_by_email(self, email):
        return self.user_repository.get_by_email(email)

    def create_user(self, user):
        if user.Password is None:
            raise ValueError("Password cannot be None")
        self.set_password(user, user.Password)  # Hash the password
        self.user_repository.add(user)
        return user

    def update_profile(self, command: UpdateProfileCommand):
        user = self.user_repository.get(command.user_id)
        if not user:
            raise ValueError(f"User with ID {command.user_id} not found")

        user.Username = command.username
        user.Email = command.email
        user.Phone = normalize_phone_number(command.phone)
        user.BirthDay = command.birthDay

        self.user_repository.update(user)

    def change_password(self, command: ChangePasswordCommand):
        user = self.user_repository.get(command.user_id)
        if not user:
            raise ValueError("User not found")

        # Verify the current password
        if not self.check_password(user, command.current_password):
            raise ValueError("Current password is incorrect")

        # Ensure the new password is different from the current password
        if self.check_password(user, command.new_password):
            raise ValueError("New password must be different from the current password")

        # Hash the new password and update the user
        self.set_password(user, command.new_password)
        self.user_repository.update(user)

    def set_password(self, user, password):
        user.Password = Users.bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, user, password):
        return Users.bcrypt.check_password_hash(user.Password, password)
