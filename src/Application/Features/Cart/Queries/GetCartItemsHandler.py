
from src.Application.Features.Cart.Queries.GetCartItemsQuery import GetCartItemsQuery
from src.Application.Features.Cart.Mapping.CartMapper import CartMapper
from src.Infrastructure.Repositories.CartRepository import CartRepositoryImpl

class GetCartItemsHandler:
    def __init__(self, cart_repository: CartRepositoryImpl):
        self.cart_repository = cart_repository

    async def handle(self, query: GetCartItemsQuery):
        cart_items = await self.cart_repository.get_all_cart_items(query.user_id)
        cart_items_dto = []
        for cart_item in cart_items:
            product_name = cart_item.Product.Name if cart_item.Product else None
            price = cart_item.Product.Price if cart_item.Product else None
            category_name = cart_item.Product.Category.Name if cart_item.Product and cart_item.Product.Category else None
            cart_dto = CartMapper.to_dto(cart_item, product_name, category_name, price)
            cart_items_dto.append(cart_dto)
        return cart_items_dto
