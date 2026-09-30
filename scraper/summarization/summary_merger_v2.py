import re


class SummaryMergerV2:
    def __init__(
        self,
        similarity_threshold: float = 0.40,
        containment_threshold: float = 0.80
    ):
        self.similarity_threshold = similarity_threshold
        self.containment_threshold = containment_threshold

    def split_sentences(self, text: str):
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

    def get_tokens(self, sentence: str):
        normalized = self.normalize_sentence(sentence)

        if not normalized:
            return set()

        return set(normalized.split())

    def calculate_similarity(
        self,
        sentence_a: str,
        sentence_b: str
    ):
        tokens_a = self.get_tokens(sentence_a)
        tokens_b = self.get_tokens(sentence_b)

        if not tokens_a or not tokens_b:
            return 0.0

        intersection = tokens_a.intersection(tokens_b)
        union = tokens_a.union(tokens_b)

        return len(intersection) / len(union)

    def calculate_containment(
        self,
        shorter_sentence: str,
        longer_sentence: str
    ):
        shorter_tokens = self.get_tokens(shorter_sentence)
        longer_tokens = self.get_tokens(longer_sentence)

        if not shorter_tokens:
            return 0.0

        intersection = shorter_tokens.intersection(
            longer_tokens
        )

        return len(intersection) / len(shorter_tokens)

    def is_more_informative(
        self,
        sentence_a: str,
        sentence_b: str
    ):
        tokens_a = self.get_tokens(sentence_a)
        tokens_b = self.get_tokens(sentence_b)

        return len(tokens_a) > len(tokens_b)

    def should_merge(
        self,
        sentence_a: str,
        sentence_b: str
    ):
        similarity = self.calculate_similarity(
            sentence_a,
            sentence_b
        )

        if similarity >= self.similarity_threshold:
            return True

        tokens_a = self.get_tokens(sentence_a)
        tokens_b = self.get_tokens(sentence_b)

        if len(tokens_a) == 0 or len(tokens_b) == 0:
            return False

        if len(tokens_a) <= len(tokens_b):
            shorter = sentence_a
            longer = sentence_b
        else:
            shorter = sentence_b
            longer = sentence_a

        containment = self.calculate_containment(
            shorter,
            longer
        )

        return containment >= self.containment_threshold

    def merge(self, summaries):
        if not summaries:
            return ""

        merged_sentences = []

        for summary in summaries:
            if not summary:
                continue

            sentences = self.split_sentences(summary)

            for sentence in sentences:

                if not merged_sentences:
                    merged_sentences.append(sentence)
                    continue

                replaced = False
                redundant = False

                for index, existing in enumerate(
                    merged_sentences
                ):

                    if not self.should_merge(
                        sentence,
                        existing
                    ):
                        continue

                    redundant = True

                    if self.is_more_informative(
                        sentence,
                        existing
                    ):
                        merged_sentences[index] = sentence

                    replaced = True
                    break

                if not redundant and not replaced:
                    merged_sentences.append(sentence)

        return " ".join(merged_sentences)