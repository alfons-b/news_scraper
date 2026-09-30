from bs4 import BeautifulSoup
from readability import Document

from .base import BaseExtractor


class ReadabilityExtractor(BaseExtractor):
    """
    Extractor artikel menggunakan algoritma Readability.

    Readability mencoba menentukan bagian utama artikel
    dari struktur HTML tanpa bergantung pada selector
    khusus suatu website.
    """

    def extract(self, html, url=None):

        if not html:
            return None

        try:
            document = Document(html)

        except Exception:
            return None

        title = document.title()
        summary_html = document.summary()

        if not summary_html:
            return None

        soup = BeautifulSoup(
            summary_html,
            "html.parser"
        )

        content = soup.get_text(
            "\n\n",
            strip=True
        )

        if not content:
            return None

        return {
            "url": url or "",
            "canonical_url": "",
            "title": title or "",
            "author": "",
            "published_at": None,
            "content": content,
            "summary": "",
            "image_url": "",
            "category": "",
            "extraction_method": "READABILITY",
        }