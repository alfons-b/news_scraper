from .service import DirectionService


class DirectionProcessor:

    def __init__(self):
        self.service = DirectionService()

    def process_article(self, article):
        if not article:
            return None

        if not article.summary:
            return article

        result = self.service.predict(
            article.summary
        )

        if result is None:
            return article

        article.direction_prediction = result["label"]

        article.save(
            update_fields=[
                "direction_prediction",
                "updated_at",
            ]
        )

        return article

    def process_articles(self, articles):
        processed_count = 0
        skipped_count = 0

        for article in articles:
            if not article:
                continue

            if not article.summary:
                skipped_count += 1
                continue

            self.process_article(article)

            processed_count += 1

        return {
            "processed": processed_count,
            "skipped": skipped_count,
        }