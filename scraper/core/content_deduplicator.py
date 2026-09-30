from .content_hasher import ContentHasher


class ContentDeduplicator:
    """
    Menghilangkan duplikasi berdasarkan hash konten.

    Prinsip:
    - Konten identik dianggap duplikat.
    - Konten berbeda dianggap unik.
    - Urutan kemunculan pertama dipertahankan.
    """

    def __init__(self):
        self.hasher = ContentHasher()

    def deduplicate(self, contents):

        if not contents:
            return []

        seen_hashes = set()
        unique_contents = []

        for content in contents:

            content_hash = self.hasher.hash_content(
                content
            )

            if not content_hash:
                continue

            if content_hash in seen_hashes:
                continue

            seen_hashes.add(content_hash)
            unique_contents.append(content)

        return unique_contents