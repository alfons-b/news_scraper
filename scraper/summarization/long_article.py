from scraper.summarization.service import SummarizationService
from scraper.summarization.chunker import TextChunker


class LongArticleSummarizer:

    def __init__(
        self,
        max_tokens: int = 450,
        overlap_paragraphs: int = 2
    ):
        print("Initializing LongArticleSummarizer...")

        # Service model summarization
        self.summarizer = SummarizationService()

        # Chunker menggunakan tokenizer dari model yang sama
        self.chunker = TextChunker(
            tokenizer=self.summarizer.tokenizer,
            max_tokens=max_tokens,
            overlap_paragraphs=overlap_paragraphs
        )

        print("LongArticleSummarizer ready.")

    def summarize_chunks(self, text: str):
        """
        Membagi artikel menjadi beberapa chunk,
        kemudian melakukan summarization pada setiap chunk.

        Return:
            list[dict]
        """

        if not text:
            return []

        text = text.strip()

        if not text:
            return []

        # 1. Buat chunks
        chunks = self.chunker.create_chunks(text)

        results = []

        # 2. Summarize setiap chunk
        for index, chunk in enumerate(chunks, start=1):

            print(
                f"\nSummarizing chunk "
                f"{index}/{len(chunks)}..."
            )

            summary = self.summarizer.summarize(chunk)

            results.append({
                "chunk_index": index,
                "chunk_text": chunk,
                "summary": summary,
                "chunk_tokens": self.chunker.count_tokens(chunk)
            })

        return results