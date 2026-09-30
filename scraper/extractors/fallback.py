from .conventional import ConventionalExtractor
from .readability import ReadabilityExtractor


class FallbackExtractor:
    """
    Menjalankan extractor secara berurutan.

    Urutan:
    1. Conventional
    2. Readability
    """

    def __init__(self):
        self.extractors = [
            ConventionalExtractor(),
            ReadabilityExtractor(),
        ]

    def extract(self, html, url=None):

        for extractor in self.extractors:

            result = extractor.extract(
                html,
                url
            )

            if result is not None:
                return result

        return None