from typing import List


class TextChunker:

    def __init__(
        self,
        tokenizer,
        max_tokens: int = 450,
        overlap_paragraphs: int = 2
    ):
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens
        self.overlap_paragraphs = overlap_paragraphs

    # ========================================================
    # HITUNG TOKEN
    # ========================================================

    def count_tokens(self, text: str) -> int:

        if not text.strip():
            return 0

        tokens = self.tokenizer.encode(
            text,
            add_special_tokens=False
        )

        return len(tokens)

    # ========================================================
    # PISAHKAN PARAGRAF
    # ========================================================

    def split_paragraphs(self, text: str) -> List[str]:

        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n")
            if paragraph.strip()
        ]

        return paragraphs

    # ========================================================
    # BUAT CHUNK
    # ========================================================

    def create_chunks(self, text: str) -> List[str]:

        paragraphs = self.split_paragraphs(text)

        if not paragraphs:
            return []

        chunks = []
        current_paragraphs = []
        current_tokens = 0
        paragraph_index = 0

        while paragraph_index < len(paragraphs):

            paragraph = paragraphs[paragraph_index]
            paragraph_tokens = self.count_tokens(paragraph)

            # ------------------------------------------
            # Paragraf lebih besar dari batas chunk
            # ------------------------------------------

            if paragraph_tokens > self.max_tokens:

                if current_paragraphs:
                    chunks.append(
                        "\n\n".join(current_paragraphs)
                    )

                chunks.append(paragraph)

                current_paragraphs = []
                current_tokens = 0

                paragraph_index += 1

                continue

            # ------------------------------------------
            # Paragraf masih bisa dimasukkan
            # ------------------------------------------

            if (
                not current_paragraphs
                or current_tokens + paragraph_tokens
                <= self.max_tokens
            ):

                current_paragraphs.append(paragraph)
                current_tokens += paragraph_tokens

                paragraph_index += 1

                continue

            # ------------------------------------------
            # Chunk penuh
            # ------------------------------------------

            chunks.append(
                "\n\n".join(current_paragraphs)
            )

            # ------------------------------------------
            # Ambil overlap sebanyak mungkin
            # tetapi jangan sampai membuat paragraf
            # berikutnya tidak bisa masuk.
            # ------------------------------------------

            overlap = current_paragraphs[
                -self.overlap_paragraphs:
            ]

            while overlap:

                overlap_tokens = sum(
                    self.count_tokens(p)
                    for p in overlap
                )

                if (
                    overlap_tokens + paragraph_tokens
                    <= self.max_tokens
                ):
                    break

                overlap = overlap[1:]

            current_paragraphs = overlap.copy()

            current_tokens = sum(
                self.count_tokens(p)
                for p in current_paragraphs
            )

            # Penting:
            # paragraph_index TIDAK dinaikkan di sini.
            # Karena paragraf yang gagal dimasukkan
            # akan dicoba lagi dengan overlap yang baru.

        # ------------------------------------------
        # Simpan chunk terakhir
        # ------------------------------------------

        if current_paragraphs:
            chunks.append(
                "\n\n".join(current_paragraphs)
            )

        return chunks