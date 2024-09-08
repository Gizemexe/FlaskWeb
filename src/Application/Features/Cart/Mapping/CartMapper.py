# src/Application/Mapping/CartMapper.py
from src.Application.DTOs.CartDto import CartDTO
from src.Domain.Entities.Cart import Carts

class CartMapper:
    @staticmethod
    def to_dto(cart: Carts, product_name: str, category_name: str, price: float) -> CartDTO:
        return CartDTO(
            id=cart.Id,
            user_id=cart.UserId,
            product_id=cart.ProductId,
            product_name=product_name,
            category_name=category_name,
            quantity=cart.Quantity,
            price=price,
            created_at=cart.created_at,
            updated_at=cart.updated_at
        )

    @staticmethod
    def from_dto(cart_dto: CartDTO) -> Carts:
        return Carts(
            Id=cart_dto.id,
            UserId=cart_dto.user_id,
            ProductId=cart_dto.product_id,
            Quantity=cart_dto.quantity,
            created_at=cart_dto.created_at,
            updated_at=cart_dto.updated_at
        )

    @staticmethod
    def to_response(cart_dto: CartDTO) -> dict:
        return {
            "id": str(cart_dto.id),
            "productId": str(cart_dto.product_id),
            "productName": cart_dto.product_name,
            "categoryName": cart_dto.category_name,
            "quantity": cart_dto.quantity,
            "price": cart_dto.price,
        }
