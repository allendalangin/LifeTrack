from dataclasses import dataclass

@dataclass
class Article:
    title: str
    description: str
    source_name: str
    published_date : str
    image : str
    content: str = ""