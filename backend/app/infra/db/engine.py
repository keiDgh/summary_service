from sqlalchemy.ext.asyncio import create_async_engine

from app.infra.settings.config import settings


engine = create_async_engine(
    url=settings.db_url
)