from backend.interfaces.loader import DocsLoaderInterface


class TXTLoader(DocsLoaderInterface):
    def load_text(self, doc_path: str) -> str:
        with open(doc_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
