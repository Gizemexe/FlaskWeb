from datetime import datetime

class CategoryDTO:
    def __init__(self, id, name, image, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.image = image
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
