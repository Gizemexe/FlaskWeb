from src.Domain.Repositories.UserRepository import UserRepository
from src.Domain.Entities.User import Users
from src.Infrastructure.Database.database import db

class UserRepositoryImpl(UserRepository):
    def add(self, user: Users):
        db.session.add(user)
        db.session.commit()

    def get(self, user_id):
        return Users.query.get(user_id)

    def get_all(self):
        return Users.query.all()

    def update(self, user: Users):
        db.session.merge(user)
        db.session.commit()

    def delete(self, user_id):
        user = self.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    def get_by_username(self, username):
        return Users.query.filter_by(Username=username).first()

    def get_by_email(self, email):
        return Users.query.filter_by(Email=email).first()
