from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from typing import Generator

from app.infra.db.engine import engine

session_maker = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False, 
    autocommit=False, # True- каждый запрос автоматически коммитится
    future=True, #новая версия async session
    autoflush=False #перед каждым select автоматически делает flush, чтобы запрос увидел свежие изменения из сессии
)

def get_async_db() -> Generator[AsyncSession, None, None]:
    db = session_maker()
    try:
        yield db
    finally:
        db.close()