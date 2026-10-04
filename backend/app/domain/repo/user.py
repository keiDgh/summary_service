from abc import  abstractmethod

from app.domain.models import User
from app.domain.repo.repository import Repository

class UserRepository(Repository[User]):
    @abstractmethod
    async def get_by_username(self, username: str) -> User: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User: ...

    @abstractmethod
    async def add(self, username: str, email: str, password_hash: str) -> User: ...

    @abstractmethod
    async def update_profile(self, user_id: str, username: str | None = None, email: str| None = None) -> User: ...

    @abstractmethod
    async def change_password(self, user_id: int, new_password: str) -> User: ...

    @abstractmethod
    async def logout(self, user_id: int) -> None: ... 