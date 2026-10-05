from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.repo import SummaryRepository
from app.domain.models import Summary
from app.domain.exceptions import SummaryNotFound

from app.application.exceptions import AssociationAlreadyExistsError, AssociationNotFoundError

from app.infra.db.models import Summary as SummaryORM, UserSummaryAssociation

from uuid import UUID
from asyncpg.exceptions import UniqueViolationError


class SqlSummaryRepository(SummaryRepository):
    def __init__(self, db: AsyncSession):
        self._db=db

    def _to_domain(self, summary: SummaryORM):
        summary = Summary(
            summary_id=summary.summary_id, 
            public_summary_id=summary.public_summary_id, 
            resource_key=summary.resource_key, 
            title=summary.title, 
            content=summary.content, 
            author=summary.author
        )
        return summary

    async def get_by_id(self, id: int) -> Summary:
        query = (
            select(SummaryORM).
            where(SummaryORM.summary_id==id)
        )

        summary = (await self._db.execute(query)).scalars().first()

        if summary is None:
            raise SummaryNotFound(f"Summary with ID {id} does not exist")

        return self._to_domain(summary)

    async def get_by_public_id(self, public_id: UUID) -> Summary:
        query = (
            select(SummaryORM).
            where(SummaryORM.public_summary_id==public_id)
        )

        summary = (await self._db.execute(query)).scalars().first()

        if summary is None:
            raise SummaryNotFound(f"Summary with ID {public_id} does not exist")

        return self._to_domain(summary)

    async def add(self, title: str, content: str, author: str | None = None) -> Summary:
        summary = SummaryORM(
            title=title, 
            content=content, 
            author=author
        )

        self._db.add(summary)

        await self._db.commit()
        await self._db.refresh(summary)

        return self._to_domain(summary)

    async def link_to_user(self, user_id: int, summary_id: int) -> None:
        associaton = UserSummaryAssociation(
            user_id=user_id, 
            summary_id=summary_id
        )  
        self._db.add(associaton)

        try:
            await self._db.commit()
        except UniqueViolationError:
            await self._db.rollback()
            raise AssociationAlreadyExistsError(f"Association with IDs {user_id}, {summary_id} already exists")

    async def unlink_from_user(self, user_id: int, summary_id: int) -> None:
        query = (
            select(UserSummaryAssociation).
            where(UserSummaryAssociation.user_id==user_id, UserSummaryAssociation.summary_id==summary_id)
        )
        association = (await self._db.execute(query)).scalar_one_or_none()

        if association is None:
            raise AssociationNotFoundError(f"Association with user_id {user_id} and summary_id {summary_id} was not found. Operation is not available")

        await self._db.delete(association)

    async def delete(self, summary_id: int) -> None:
        query = (
            select(SummaryORM).
            where(SummaryORM.summary_id==summary_id)
        )

        summary = (await self._db.execute(query)).scalars().first()

        if summary is None:
            raise SummaryNotFound(f"Summary with ID {summary_id} does not exist")

        await self._db.delete(summary)
        