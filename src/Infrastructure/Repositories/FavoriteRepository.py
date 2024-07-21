from src.Domain.Entities.Favorites import Favorites
from src.Infrastructure.Database.database import db

class FavoritesRepositoryImpl:
    def add_favorite(self, favorite: Favorites) -> Favorites:
        db.session.add(favorite)
        db.session.commit()
        return favorite

    def get_favorites_by_user(self, user_id: int) -> list[Favorites]:
        return Favorites.query.filter_by(UserId=user_id).all()

    def get_favorite_by_user_and_product(self, user_id: int, product_id: int) -> Favorites:
        return Favorites.query.filter_by(UserId=user_id, ProductId=product_id).first()

    def remove_favorite(self, favorite: Favorites) -> None:
        db.session.delete(favorite)
        db.session.commit()
