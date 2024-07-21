from datetime import datetime

class FavoriteDTO:
    def __init__(self, id, user_id, product_id, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
