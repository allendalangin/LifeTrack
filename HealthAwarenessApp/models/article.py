from dataclasses import dataclass

@dataclass
class Article:
    title: str
    author: str
    published_date: str  # You can also use datetime here if desired.
    content: str = ""