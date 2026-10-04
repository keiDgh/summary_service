from dataclasses import dataclass
from uuid import UUID

@dataclass
class User:
    user_id: int
    public_user_id: UUID
    username: str
    email: str
    password_hash: str