from datetime import datetime

class UserDto:
    def __init__(self, id, username, email, phone=None, birth_day=None, password=None, created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.phone = phone
        self.birth_day = birth_day
        self.password = password
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
