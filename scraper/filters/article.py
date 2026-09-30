import re
from urllib.parse import urlparse

from .base import BaseArticleFilter


class GenericArticleFilter(BaseArticleFilter):
    """
    Filter URL artikel generik.

    Baseline:
    URL dianggap sebagai kandidat artikel apabila memiliki pola:

        /segment/angka/slug

    Contoh:
        /news/979242/judul-artikel
        /regional-ntt/979265/judul-artikel
        /lifestyle/979236/judul-artikel
    """

    ARTICLE_PATTERN = re.compile(
        r"^/[^/]+/\d+/[^/]+/?$"
    )

    def is_article_url(self, url):
        if not url:
            return False

        try:
            parsed = urlparse(url)
        except Exception:
            return False

        path = parsed.path

        return bool(
            self.ARTICLE_PATTERN.match(path)
        )