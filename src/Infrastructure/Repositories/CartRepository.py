from typing import List
from src.Domain.Repositories.CartRepository import CartRepository
from src.Domain.Entities.Cart import Carts

class CartRepositoryImpl(CartRepository):

    def __init__(self, db_session):
        self.db_session = db_session

    async def get_all_cart_items(self, user_id):
        return Carts.query.filter_by(UserId=user_id).all()

    async def add_cart_item(self, cart_item: Carts) -> Carts:
        # Veritabanına ekleme işlemi burada yapılacak
        pass

    async def update_cart_item(self, cart_item: Carts) -> Carts:
        # Veritabanında güncelleme işlemi burada yapılacak
        pass

    async def remove_cart_item(self, cart_id: str, user_id: str) -> bool:
        # Veritabanından silme işlemi burada yapılacak
        pass
