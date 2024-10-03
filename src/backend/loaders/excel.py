import pandas as pd

from backend.interfaces.loader import DocsLoaderInterface


class XLSLoader(DocsLoaderInterface):
    def load_text(self, doc_path: str) -> str:
        sheets_dict = pd.read_excel(doc_path, sheet_name=None)
        text = ''
        for name, sheet in sheets_dict.items():
            text += sheet.to_csv(sep='|', header=True)

        return text.strip()
