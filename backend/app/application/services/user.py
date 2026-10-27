from app.domain.models import User
from app.domain.repo import UserRepository

from uuid import UUID

class UserService:
    def __init__(self, user_service: UserRepository):
        self._user = user_service

    async def get_by_id(self, id: int) -> User:
        return await self._user.get_by_id(id)
    
    async def get_by_email(self, email: str) -> User:
        return await self._user.get_by_email(email)

    async def get_by_username(self, username: int) -> User:
        return await self._user.get_by_username(username)
        
    async def get_by_public_id(self, public_id: UUID) -> User:
        return await self._user.get_by_public_id(public_id)

    async def get_by_username_or_email(self, username: str, email: str) -> User: 
        user = await self._user.get_by_username(username)
        if not user:
            user = await self._user.get_by_email(email)
        return user

    async def add(self, username: str, email: str, password_hash: str) -> User:
        return await self._user.add(
            username=username, 
            email=email, 
            password_hash=password_hash
        ) 

    async def update_profile(
            self, 
            user_id: int, 
            username: str | None = None, 
            email: str| None = None
    ) -> User:
        return await self._user.update_profile(
            user_id=user_id, 
            username=username, 
            email=email
        )