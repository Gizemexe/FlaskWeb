from datetime import datetime

class ProductDTO:
    def __init__(self, id, name, code, description=None, price=None, image=None, stock=None, category_id=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.price = price
        self.image = image
        self.stock = stock
        self.category_id = category_id
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
