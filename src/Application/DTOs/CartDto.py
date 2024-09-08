# src/Application/DTOs/CartDTO.py
class CartDTO:
    def __init__(self, id, user_id, product_id, product_name, category_name, quantity, price, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.product_name = product_name
        self.category_name = category_name
        self.quantity = quantity
        self.price = price
        self.created_at = created_at
        self.updated_at = updated_at
