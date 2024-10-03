import re

from pdfminer.high_level import extract_text

from backend.interfaces.loader import DocsLoaderInterface


class PDFLoader(DocsLoaderInterface):
    CID_REGEX = r'\(cid:\d+\)'

    def __clean_cid_placeholders(self, text: str) -> str:
        cleaned_text = re.sub(self.CID_REGEX, "", text)
        return cleaned_text.strip()

    @staticmethod
    def __clean_empty_lines(text: str) -> str:
        cleaned_text = "\n".join(line for line in text.splitlines() if line.strip())
        return cleaned_text

    def load_text(self, pdf_path: str) -> str:
        text = extract_text(pdf_path)
        cleaned_text = self.__clean_cid_placeholders(text)
        return self.__clean_empty_lines(cleaned_text)
