from dataclasses import dataclass
from typing import Optional


@dataclass
class QdrantDoc(object):
    title: str
    content: str
    embedding: Optional[list[float]]
    keywords: Optional[list[str]] = None

    def as_payload(self):
        return {
            'metadata': {
                'title': self.title,
                'keywords': self.keywords or [],
            },
            'page_content': self.content,
        }
