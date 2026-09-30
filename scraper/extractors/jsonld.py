import json

from bs4 import BeautifulSoup

from .base import BaseExtractor


class JSONLDExtractor(BaseExtractor):
    """
    Extractor artikel menggunakan JSON-LD.

    Mencari:
        <script type="application/ld+json">

    Kemudian mencari schema:
        NewsArticle
        Article
        BlogPosting
    """

    ARTICLE_TYPES = {
        "NewsArticle",
        "Article",
        "BlogPosting",
    }

    def extract(self, html, url=None):

        if not html:
            return None

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        scripts = soup.find_all(
            "script",
            attrs={
                "type": "application/ld+json"
            }
        )

        for script in scripts:

            raw_json = script.string

            if not raw_json:
                continue

            try:
                data = json.loads(raw_json)

            except (json.JSONDecodeError, TypeError):
                continue

            candidates = self._flatten_jsonld(data)

            for item in candidates:

                if not isinstance(item, dict):
                    continue

                if self._is_article(item):

                    return self._normalize(
                        item,
                        url
                    )

        return None

    def _flatten_jsonld(self, data):

        if isinstance(data, list):

            result = []

            for item in data:
                result.extend(
                    self._flatten_jsonld(item)
                )

            return result

        if isinstance(data, dict):

            result = [data]

            graph = data.get("@graph")

            if isinstance(graph, list):

                for item in graph:
                    result.extend(
                        self._flatten_jsonld(item)
                    )

            return result

        return []
    

    def _is_article(self, data):

        article_type = data.get("@type")

        if isinstance(article_type, list):

            return any(
                item in self.ARTICLE_TYPES
                for item in article_type
            )

        return article_type in self.ARTICLE_TYPES

    
    def _normalize(self, data, url=None):

        title = data.get("headline")

        author = self._extract_author(
            data.get("author")
        )

        published_at = (
            data.get("datePublished")
        )

        image_url = self._extract_image(
            data.get("image")
        )

        description = data.get(
            "description"
        )

        article_url = (
            data.get("url")
            or url
        )

        return {
            "url": article_url,
            "canonical_url": self._extract_canonical_url(
                data.get("mainEntityOfPage")
            ),
            "title": title or "",
            "author": author or "",
            "published_at": published_at,
            "content": data.get(
                "articleBody",
                ""
            ),
            "summary": description or "",
            "image_url": image_url or "",
            "category": data.get(
                "articleSection",
                ""
            ),
            "extraction_method": "JSONLD",
        }

    def _extract_author(self, author):

        if isinstance(author, str):
            return author

        if isinstance(author, dict):
            return author.get(
                "name",
                ""
            )

        if isinstance(author, list):

            names = []

            for item in author:

                if isinstance(item, str):
                    names.append(item)

                elif isinstance(item, dict):

                    name = item.get("name")

                    if name:
                        names.append(name)

            return ", ".join(names)

        return ""

    def _extract_canonical_url(self, value):

        if isinstance(value, str):
            return value

        if isinstance(value, dict):
            return value.get(
                "@id",
                ""
            )

        return ""

    def _extract_image(self, image):

        if isinstance(image, str):
            return image

        if isinstance(image, dict):
            return image.get(
                "url",
                ""
            )

        if isinstance(image, list):

            if not image:
                return ""

            first = image[0]

            if isinstance(first, str):
                return first

            if isinstance(first, dict):
                return first.get(
                    "url",
                    ""
                )

        return ""