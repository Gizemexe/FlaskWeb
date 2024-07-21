from src.Domain.Repositories.BaseRepository import BaseRepository


class FavoritesRepository(BaseRepository):
    def add_favorite(self, user_id, product_id):
        pass
    def get_favorites_by_user(self, user_id):
        pass

    def remove_favorite(self, user_id, product_id):
        pass

