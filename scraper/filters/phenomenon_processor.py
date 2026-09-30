from scraper.filters.phenomenon import PhenomenonFilter


class PhenomenonProcessor:

    def __init__(self):
        self.filter = PhenomenonFilter()

    def process_article(self, article):

        if not article:
            return None

        text = f"{article.title} {article.content}".strip()

        result = self.filter.predict(text)

        article.ntt_related = result["ntt_related"]

        article.economic_activity = (
            result["economic_activity"]
        )

        article.matched_economic_keywords = (
            result["matched_economic_keywords"]
        )

        article.phenomenon_prediction = (
            result["phenomenon_prediction"]
        )

        article.save(
            update_fields=[
                "ntt_related",
                "economic_activity",
                "matched_economic_keywords",
                "phenomenon_prediction",
                "updated_at",
            ]
        )

        return article

    def process_articles(self, articles):

        processed_count = 0
        phenomenon_count = 0

        for article in articles:

            if not article:
                continue

            processed_article = self.process_article(article)

            if not processed_article:
                continue

            processed_count += 1

            if processed_article.phenomenon_prediction:
                phenomenon_count += 1

        return {
            "processed": processed_count,
            "phenomenon": phenomenon_count,
        }