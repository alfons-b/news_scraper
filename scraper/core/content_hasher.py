import hashlib


class ContentHasher:
    """
    Membuat hash dari isi artikel.

    Tujuan:
    - menghasilkan identitas konten
    - konten yang sama menghasilkan hash yang sama
    - perubahan konten menghasilkan hash berbeda
    """

    def hash_content(self, content):

        if not content:
            return ""

        normalized_content = content.strip()

        return hashlib.sha256(
            normalized_content.encode(
                "utf-8"
            )
        ).hexdigest()