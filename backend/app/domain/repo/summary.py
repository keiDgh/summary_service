from abc import abstractmethod

from app.domain.models import Summary
from app.domain.repo.repository import Repository

class SummaryRepository(Repository[Summary]):
    @abstractmethod
    async def add(self, title: str, author: str, content: str) -> Summary: ...

    @abstractmethod
    async def link_to_user(self, user_id: int, summary_id: int) -> Summary: ...

    @abstractmethod
    async def unlink_from_user(self, user_id: int, summary_id: int) -> None: ...

    @abstractmethod
    async def delete(self, summary_id: int) -> None: ...