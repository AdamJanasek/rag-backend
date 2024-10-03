from typing import Any

from backend.interfaces.loader import DocsLoaderInterface
from backend.loaders.excel import XLSLoader
from backend.loaders.pdf import PDFLoader
from backend.loaders.txt import TXTLoader


class DocsLoader(DocsLoaderInterface):
    def __init__(self):
        self.adapters = {
            'txt': TXTLoader(),
            'pdf': PDFLoader(),
            'xls': XLSLoader(),
            'xlsx': XLSLoader(),
        }

    def get_adapter(self, file_path: str) -> Any:
        file_ext = file_path.split('.')[-1]
        return self.adapters.get(file_ext)

    def load_text(self, doc_path: str) -> str:
        adapter = self.get_adapter(doc_path)
        if adapter:
            return adapter.load_text(doc_path)
        raise ValueError(f'No adapter found for the file type: {doc_path.split('.')[-1]}')
