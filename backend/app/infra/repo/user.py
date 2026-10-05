from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.repo import UserRepository
from app.domain.models import User
from app.domain.exceptions import UserNotFoundError, UserAlreadyExistsError

from app.infra.db.models import User as UserORM

from uuid import UUID
from asyncpg.exceptions import UniqueViolationError

class SqlUserRepository(UserRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    def _to_domain(self, user: UserORM) -> User:
        user = User(
            user_id=user.user_id, 
            public_user_id=user.public_user_id, 
            username=user.username, 
            email=user.email, 
            password_hash=user.password_hash
        )
        return user

    async def get_by_id(self, id: int) -> User:
        query = (
            select(UserORM).
            where(UserORM.user_id==id)
        )

        user = (await self._db.execute(query)).scalars().first()

        if user is None:
            raise UserNotFoundError(f"User with ID {id} does not exist")

        return self._to_domain(user)

    async def get_by_public_id(self, public_id: UUID) -> User:
        query = (
            select(UserORM).
            where(UserORM.public_user_id==public_id)
        )

        user = (await self._db.execute(query)).scalars().first()

        if user is None:
            raise UserNotFoundError(f"User with ID {public_id} does not exist")

        return self._to_domain(user)

    async def get_by_username(self, username: str) -> User:
        query = (
            select(UserORM).
            where(UserORM.username==username)
        )

        user = (await self._db.execute(query)).scalars().first()

        if user is None:
            raise UserNotFoundError(f"User with username {username} does not exist")

        return self._to_domain(user)    


    async def get_by_email(self, email: str) -> User:
        query = (
            select(UserORM).
            where(UserORM.email==email)
        )

        user = (await self._db.execute(query)).scalars().first()

        if user is None:
            raise UserNotFoundError(f"User with email {email} does not exist")

        return self._to_domain(user)

    async def add(self, username: str, email: str, password_hash: str) -> User:
        user = UserORM(
            username=username, 
            email=email, 
            password_hash=password_hash
        )

        self._db.add(user)

        try:
            await self._db.commit()
        except UniqueViolationError:
            await self._db.rollback()
            raise UserAlreadyExistsError("User with this username or email already exists")

        user = await self._db.refresh(user)

        return self._to_domain(user)

    async def update_profile(
            self, 
            user_id: int, 
            username : str | None = None, 
            email: str | None = None
    ) -> User:

        query = (
            select(UserORM).
            where(UserORM.user_id==id)
        )

        user = (await self._db.execute(query)).scalars().first()

        if user is None:
            raise UserNotFoundError(f"User with ID {user_id} does not exist")

        if username is not None:
            user.username=username
        if email is not None:
            user.email=email

        try:
            await self._db.commit()
        except UniqueViolationError:
            await self._db.rollback()
            raise UserAlreadyExistsError("User with this username or email already exists")

        await self._db.refresh(user)

        return self._to_domain(user)

    async def change_password(self, user_id: int, new_password: str):
        query = (
            select(UserORM).
            where(UserORM.user_id==id)
        )

        user = (await self._db.execute(query)).scalars().first()

        if user is None:
            raise UserNotFoundError(f"User with ID {user_id} does not exist")

        user.password_hash=new_password

        await self._db.commit()
        await self._db.refresh(user)

        return self._to_domain(user)

    