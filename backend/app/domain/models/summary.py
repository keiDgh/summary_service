from dataclasses import dataclass
from uuid import UUID

@dataclass
class Summary:
    summary_id: int
    public_summary_id: UUID
    resource_key: str
    title: str
    content: str
    author: str | None = None
    # Дать переменную datetime (когда был link to user)