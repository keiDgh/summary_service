import argon2

import uuid

from app.infra.api.schemas import SignUp, SignIn, TokenPairResponse
from app.infra.services.jwt import TokenService

from app.application.services import UserService
from app.application.exceptions import UserExistsError, WrongPasswordError, InternalServerError

from app.domain.exceptions import UserNotFoundError


class AuthService:
    def __init__(self, token_service: TokenService, user_service: UserService):
        self._ph = argon2.PasswordHasher()
        self._token_service=token_service
        self._user_service = user_service

    async def register(self, data: SignUp) -> TokenPairResponse:
        try:
            await self._user_service.get_by_username_or_email(
                username=data.username, 
                email=data.email
            )
        except UserNotFoundError:
            password_hash = self._ph.hash(data.password)

            user = await self._user_service.add(
                username=data.username, 
                email=data.email, 
                password_hash=password_hash
                )

            pair = await self._token_service.create_pair(public_user_id=user.public_user_id)
            return pair
        else:
            raise UserExistsError(f"User with this email or username already exists")

    async def login(self, data: SignIn) -> TokenPairResponse:
        user = await self._user_service.get_by_username_or_email(
            username=data.login, 
            email=data.login
        )

        self._validate_password(
                raw_password=data.password, 
                password_hash=user.password_hash
            )

        pair = await self._token_service.create_pair(public_user_id=user.public_user_id)
        return pair

    async def logout(self, refresh_token: uuid.UUID, access_token: str) -> None:
        public_user_id = self._token_service.validate_jwt(access_token)
        await self._token_service.invalidate_refresh(refresh_token, public_user_id)

    def _validate_password(self, raw_password: str, password_hash: str) -> None:

        try:
            self._ph.verify(
                hash=password_hash, 
                password=raw_password
                )

        except argon2.exceptions.VerifyMismatchError:
            raise WrongPasswordError("The password is wrong")
        
        except argon2.exceptions.InvalidHashError:
            raise InternalServerError("Hash is invalid")