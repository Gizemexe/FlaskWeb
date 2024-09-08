from abc import ABC, abstractmethod
from typing import List

from src.Domain.Entities.Cart import Carts


class CartRepository(ABC):

    @abstractmethod
    async def get_cart_items_by_user(self, user_id: str) -> List[Carts]:
        pass

    @abstractmethod
    async def add_cart_item(self, cart_item: Carts) -> Carts:
        pass

    @abstractmethod
    async def update_cart_item(self, cart_item: Carts) -> Carts:
        pass

    @abstractmethod
    async def remove_cart_item(self, cart_id: str, user_id: str) -> bool:
        pass
