from abc import ABC, abstractmethod
from typing import TypeVar

from uuid import UUID

T = TypeVar("T")

class Repository[T](ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> T: ...

    @abstractmethod
    async def get_by_public_id(self, public_id: UUID) -> T: ...