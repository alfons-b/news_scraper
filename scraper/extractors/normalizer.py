import re
from urllib.parse import urlsplit, urlunsplit


class ArticleNormalizer:
    """
    Normalisasi hasil ekstraksi sebelum disimpan.

    Prinsip:
    - Tidak mengubah makna isi artikel.
    - Hanya membersihkan format.
    - Tidak melakukan koreksi ejaan otomatis.
    """

    def normalize(self, data):

        if not data:
            return None

        result = data.copy()

        result["url"] = self._normalize_url(
            result.get("url", "")
        )

        result["canonical_url"] = self._normalize_url(
            result.get("canonical_url", "")
        )

        result["title"] = self._normalize_text(
            result.get("title", "")
        )

        result["author"] = self._normalize_text(
            result.get("author", "")
        )

        result["content"] = self._normalize_content(
            result.get("content", "")
        )

        result["summary"] = self._normalize_text(
            result.get("summary", "")
        )

        result["image_url"] = self._normalize_url(
            result.get("image_url", "")
        )

        result["category"] = self._normalize_text(
            result.get("category", "")
        )

        return result

    def _normalize_text(self, value):

        if value is None:
            return ""

        value = str(value)

        value = re.sub(
            r"\s+",
            " ",
            value
        )

        return value.strip()

    def _normalize_content(self, value):

        if value is None:
            return ""

        value = str(value)

        lines = []

        for line in value.splitlines():

            line = re.sub(
                r"[ \t]+",
                " ",
                line
            ).strip()

            if line:
                lines.append(line)

        return "\n\n".join(lines)

    def _normalize_url(self, value):

        if not value:
            return ""

        value = str(value).strip()

        try:
            parts = urlsplit(value)

            return urlunsplit(
                (
                    parts.scheme,
                    parts.netloc,
                    parts.path,
                    parts.query,
                    ""
                )
            )

        except Exception:
            return value