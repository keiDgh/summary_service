from dataclasses import dataclass
from uuid import UUID

from datetime import datetime

@dataclass
class Summary:
    summary_id: int
    public_summary_id: UUID
    title: str
    author: str
    content: str
    created_at: datetime