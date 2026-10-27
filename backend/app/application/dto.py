from dataclasses import dataclass

@dataclass 
class NewSource:
    resource_key: str
    type: str
    content: str

    title: str | None = None
    author: str | None = None
    image_name: str | None = None

@dataclass
class ParsedFile:
    type: str
    content: str

    author: str | None = None
    title: str | None = None