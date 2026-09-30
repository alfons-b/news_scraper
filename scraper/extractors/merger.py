class ExtractionMerger:
    """
    Menggabungkan hasil dari beberapa extractor.

    Prinsip:
    - JSON-LD menjadi sumber utama metadata.
    - Conventional menjadi sumber utama content.
    - Field kosong dari JSON-LD dapat diisi oleh extractor lain.
    """

    def merge(self, jsonld_result, conventional_result):

        if jsonld_result is None and conventional_result is None:
            return None

        jsonld_result = jsonld_result or {}
        conventional_result = conventional_result or {}

        return {
            "url": (
                jsonld_result.get("url")
                or conventional_result.get("url")
                or ""
            ),

            "canonical_url": (
                jsonld_result.get("canonical_url")
                or conventional_result.get("canonical_url")
                or ""
            ),

            "title": (
                jsonld_result.get("title")
                or conventional_result.get("title")
                or ""
            ),

            "author": (
                jsonld_result.get("author")
                or conventional_result.get("author")
                or ""
            ),

            "published_at": (
                jsonld_result.get("published_at")
                or conventional_result.get("published_at")
            ),

            "content": (
                conventional_result.get("content")
                or jsonld_result.get("content")
                or ""
            ),

            "summary": "",

            "image_url": (
                jsonld_result.get("image_url")
                or conventional_result.get("image_url")
                or ""
            ),

            "category": (
                jsonld_result.get("category")
                or conventional_result.get("category")
                or ""
            ),
            "extraction_method": "COMBINED",
        }