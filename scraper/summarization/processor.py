from scraper.summarization.long_article import LongArticleSummarizer
from scraper.summarization.summary_merger_v2 import SummaryMergerV2


class SummarizationProcessor:

    def __init__(self):

        self.summarizer = LongArticleSummarizer(
            max_tokens=450,
            overlap_paragraphs=2
        )

        self.merger = SummaryMergerV2(
            similarity_threshold=0.40,
            containment_threshold=0.80
        )

    def summarize_article(self, content):

        if not content:
            return ""

        chunk_results = (
            self.summarizer.summarize_chunks(
                content
            )
        )

        summaries = [
            result["summary"]
            for result in chunk_results
            if result.get("summary")
        ]

        return self.merger.merge(
            summaries
        )

    def process_article(self, article):

        if not article:
            return None

        if not article.content:
            return article

        summary = self.summarize_article(
            article.content
        )

        article.summary = summary

        article.save(
            update_fields=[
                "summary",
                "updated_at"
            ]
        )

        return article

    def process_articles(self, articles):

        summarized_count = 0
        skipped_count = 0

        for article in articles:

            if not article:
                continue

            if not article.content:
                skipped_count += 1
                continue

            if article.summary:
                skipped_count += 1
                continue

            self.process_article(article)

            summarized_count += 1

        return {
            "summarized": summarized_count,
            "skipped": skipped_count,
        }