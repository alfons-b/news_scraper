from scraper.summarization.service import SummarizationService


class FinalSummarizer:

    def __init__(self):
        print("Initializing FinalSummarizer...")

        self.summarizer = SummarizationService()

        print("FinalSummarizer ready.")

    def summarize(self, chunk_summaries):
        """
        Menggabungkan summary dari setiap chunk,
        kemudian menghasilkan satu summary akhir.

        Parameters
        ----------
        chunk_summaries : list[str]
            Daftar summary hasil summarization per chunk.

        Returns
        -------
        str
            Summary akhir artikel.
        """

        if not chunk_summaries:
            return ""

        # Bersihkan summary kosong
        valid_summaries = [
            summary.strip()
            for summary in chunk_summaries
            if summary and summary.strip()
        ]

        if not valid_summaries:
            return ""

        # Jika hanya ada satu summary,
        # tidak perlu melakukan summarization ulang.
        if len(valid_summaries) == 1:
            return valid_summaries[0]

        # Gabungkan summary per chunk
        combined_text = "\n\n".join(
            valid_summaries
        )

        print("\nCombined summaries:")
        print(combined_text)

        # Summarization tahap akhir
        final_summary = self.summarizer.summarize(
            combined_text
        )

        return final_summary.strip()