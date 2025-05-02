from dataclasses import dataclass

@dataclass
class MessageMeta:
    id: str
    subject: str
    sender: str
    date: str
    snippet: str
