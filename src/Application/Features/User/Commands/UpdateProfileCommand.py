from dataclasses import dataclass

@dataclass
class UpdateProfileCommand:
    user_id: int
    username: str
    email: str
    phone: str
    birthDay: str  # Assuming birthDate comes as a string from JSON
