from dataclasses import dataclass

@dataclass
class Resource:
    name: str
    category: str
    location: str