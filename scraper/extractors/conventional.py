from bs4 import BeautifulSoup

from .base import BaseExtractor


class ConventionalExtractor(BaseExtractor):
    """
    Extractor artikel menggunakan struktur HTML konvensional.

    Baseline untuk situs Tribun/Pos Kupang:
    - Mencari container artikel
    - Mengambil elemen <p>
    - Mengabaikan paragraf kosong
    - Mengabaikan elemen dengan class 'baca'
    - Mengabaikan paragraf promosi/footer
    - Menggabungkan paragraf menjadi content
    """

    ARTICLE_CONTAINER = (
        "div.side-article."
        "txt-article."
        "multi-fontsize."
        "editcontent"
    )

    def extract(self, html, url=None):

        if not html:
            return None

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        container = soup.select_one(
            self.ARTICLE_CONTAINER
        )

        if container is None:
            return None

        paragraphs = container.find_all("p")

        content_parts = []

        for paragraph in paragraphs:

            # Ambil teks yang sudah dibersihkan
            text = paragraph.get_text(
                " ",
                strip=True
            )

            # Abaikan paragraf kosong
            if not text:
                continue

            # Abaikan "Baca juga"
            classes = paragraph.get(
                "class",
                []
            )

            if "baca" in classes:
                continue

            # Abaikan footer/promosi Google News
            if self._is_footer(text):
                continue

            content_parts.append(text)

        if not content_parts:
            return None

        content = "\n\n".join(
            content_parts
        )

        return {
            "url": url or "",

            "canonical_url": "",

            "title": "",

            "author": "",

            "published_at": None,

            "content": content,

            "summary": "",

            "image_url": "",

            "category": "",

            "extraction_method": "CONVENTIONAL",
        }

    def _is_footer(self, text):
        """
        Mendeteksi teks promosi/footer
        yang bukan bagian dari isi artikel.
        """

        normalized = text.lower()

        footer_patterns = [
            "ikuti berita",
            "google news",
        ]

        return any(
            pattern in normalized
            for pattern in footer_patterns
        )

