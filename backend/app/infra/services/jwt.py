from datetime import UTC, datetime, timedelta
import jwt
import uuid

from app.infra.api.schemas import TokenPairResponse, RefreshTokenResponse, JWTResponse
from app.infra.settings.config import settings

from app.infra.services import RedisClient

from app.application.exceptions import RefreshTokenInvalidError, ExpiredJWTError, InvalidJWTError


class TokenService:
    def __init__(self, redis: RedisClient):
        self._access_token_exp=settings.access_token_expire_minutes
        self._refresh_token_exp=settings.refresh_token_expire_hours
        self._algorithm=settings.algorithm
        self._key=settings.secret_key.get_secret_value()
        self._redis=redis


    async def create_pair(self, public_user_id: uuid.UUID) -> TokenPairResponse:
        access_token = self.create_jwt(public_user_id)
        refresh_token = await self.create_refresh(public_user_id)

        return TokenPairResponse(
            access_token=access_token.token, 
            token_type=access_token.type, 
            access_token_expire=access_token.expires, 

            refresh_token=refresh_token.token, 
            refresh_token_expire=refresh_token.expires
        )


    async def refresh(self, refresh_token: uuid.UUID) -> TokenPairResponse:
        try:
            public_user_id = await self.validate_refresh(refresh_token)
        except RefreshTokenInvalidError:
            raise 

        else:
            await self._redis.delete(f"refresh_token:{refresh_token}")
            return await self.create_pair(public_user_id=public_user_id)


    def create_jwt(self, public_user_id: uuid.UUID) -> JWTResponse:
        to_encode = {"sub": str(public_user_id)} # UUID is not JSON serializable type

        expires = datetime.now(UTC) + timedelta(minutes=self._access_token_exp)

        to_encode.update({"exp" : int(expires.timestamp())}) 
        # timestamp() converts datetime obj datetime(Year, Month, Day, Hour, Minute) into Unix timestamp number (seconds since 01.01.1970)

        encoded_jwt = jwt.encode(
            payload=to_encode,  
            algorithm=self._algorithm, 
            key=self._key
            )
        
        return JWTResponse(
            token=encoded_jwt, 
            type="bearer", 
            expires=expires
        )


    def validate_jwt(self, access_token: str) -> uuid.UUID | None: 

        try:
            payload = jwt.decode(
                jwt=access_token, 
                key=self._key,
                algorithms=[self._algorithm],
                options={"require_exp": True, "require_sub": True}
                )

        except jwt.ExpiredSignatureError:
            raise ExpiredJWTError("Access token is expired")
        
        except jwt.InvalidTokenError:
            raise InvalidJWTError("Token is not valid JWT")

        else:
            public_user_id = payload.get("sub")
            return public_user_id


    async def create_refresh(self, public_user_id: uuid.UUID) -> RefreshTokenResponse:
        refresh_token = uuid.uuid4()
        expires=datetime.now(UTC) + timedelta(hours=self._refresh_token_exp)
        ttl = int(timedelta(hours=self._refresh_token_exp).total_seconds())
        
        await self._redis.set(
            id=f"refresh_token:{refresh_token}", 
            value=str(public_user_id), 
            ex=ttl
            )

        return RefreshTokenResponse(
            token=refresh_token, 
            expires=expires
        )

    async def validate_refresh(self, refresh_token: uuid.UUID | None) -> uuid.UUID:
        if refresh_token is None or str(refresh_token).strip() == "":
            raise RefreshTokenInvalidError("Refresh token is not passed in")
        
        token_value = await self._redis.get(f"refresh_token:{refresh_token}")

        if token_value is None:
            raise RefreshTokenInvalidError(f"Refresh token {refresh_token} is invalid or expired")

        return uuid.UUID(token_value)


    async def invalidate_refresh(self, refresh_token: uuid.UUID) -> None:
        await self.validate_refresh(refresh_token)
        await self._redis.delete(f"refresh_token:{refresh_token}")