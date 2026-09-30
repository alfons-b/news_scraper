import re


class SummaryMerger:

    def __init__(self, similarity_threshold: float = 0.80):
        self.similarity_threshold = similarity_threshold

    def split_sentences(self, text: str):
        """
        Memisahkan teks menjadi kalimat.
        """

        if not text:
            return []

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text.strip()
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

    def normalize_sentence(self, sentence: str):
        """
        Normalisasi sederhana untuk kebutuhan
        perbandingan antar-kalimat.
        """

        sentence = sentence.lower()

        sentence = re.sub(
            r'[^\w\s]',
            ' ',
            sentence
        )

        sentence = re.sub(
            r'\s+',
            ' ',
            sentence
        )

        return sentence.strip()

    def calculate_similarity(self, sentence_a: str, sentence_b: str):
        """
        Menghitung Jaccard similarity berdasarkan token.
        """

        tokens_a = set(
            self.normalize_sentence(
                sentence_a
            ).split()
        )

        tokens_b = set(
            self.normalize_sentence(
                sentence_b
            ).split()
        )

        if not tokens_a or not tokens_b:
            return 0.0

        intersection = tokens_a.intersection(
            tokens_b
        )

        union = tokens_a.union(
            tokens_b
        )

        return len(intersection) / len(union)

    def is_redundant(self, sentence, existing_sentences):
        """
        Mengecek apakah sebuah kalimat terlalu mirip
        dengan kalimat yang sudah ada.
        """

        for existing in existing_sentences:

            similarity = self.calculate_similarity(
                sentence,
                existing
            )

            if similarity >= self.similarity_threshold:
                return True

        return False

    def merge(self, summaries):
        """
        Menggabungkan summary dari beberapa chunk
        dan menghapus kalimat yang redundan.

        Parameters
        ----------
        summaries : list[str]

        Returns
        -------
        str
        """

        if not summaries:
            return ""

        merged_sentences = []

        for summary in summaries:

            if not summary:
                continue

            sentences = self.split_sentences(
                summary
            )

            for sentence in sentences:

                if not self.is_redundant(
                    sentence,
                    merged_sentences
                ):
                    merged_sentences.append(
                        sentence
                    )

        return " ".join(
            merged_sentences
        )