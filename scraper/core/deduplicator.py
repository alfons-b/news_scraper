class URLDeduplicator:
    """
    Menghilangkan duplikasi URL dari hasil discovery.

    Prinsip:
    - URL yang sama hanya diproses sekali.
    - Urutan kemunculan pertama dipertahankan.
    """

    def deduplicate(self, urls):

        if not urls:
            return []

        seen = set()
        unique_urls = []

        for url in urls:

            if not url:
                continue

            if url in seen:
                continue

            seen.add(url)
            unique_urls.append(url)

        return unique_urls