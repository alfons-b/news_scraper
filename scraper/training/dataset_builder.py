from news.models import Article


class DatasetBuilder:

    VALID_KBLI = set("ABCDEFGHIJKLMNOPQRSTU")

    VALID_DIRECTIONS = {
        "meningkat",
        "menurun",
        "netral",
    }

    def _build_result(self, dataset, total, skipped):
        return {
            "data": dataset,
            "stats": {
                "total": total,
                "valid": len(dataset),
                "skipped": skipped,
            },
        }

    def build_kbli_dataset(self):
        articles = (
            Article.objects
            .filter(
                phenomenon_annotation=True,
                kbli_annotation__isnull=False,
            )
            .exclude(
                kbli_annotation=""
            )
            .exclude(
                annotated_summary__isnull=True
            )
            .exclude(
                annotated_summary=""
            )
            .order_by("id")
        )

        dataset = []
        skipped = 0

        for article in articles:

            if article.kbli_annotation not in self.VALID_KBLI:
                skipped += 1
                continue

            dataset.append({
                "text": article.annotated_summary,
                "label": article.kbli_annotation,
                "article_id": article.id,
            })

        return self._build_result(
            dataset=dataset,
            total=articles.count(),
            skipped=skipped,
        )

    def build_direction_dataset(self):
        articles = (
            Article.objects
            .filter(
                phenomenon_annotation=True,
                direction_annotation__isnull=False,
            )
            .exclude(
                direction_annotation=""
            )
            .exclude(
                annotated_summary__isnull=True
            )
            .exclude(
                annotated_summary=""
            )
            .order_by("id")
        )

        dataset = []
        skipped = 0

        for article in articles:

            if article.direction_annotation not in self.VALID_DIRECTIONS:
                skipped += 1
                continue

            dataset.append({
                "text": article.annotated_summary,
                "label": article.direction_annotation,
                "article_id": article.id,
            })

        return self._build_result(
            dataset=dataset,
            total=articles.count(),
            skipped=skipped,
        )

    def build_summarization_dataset(self):
        articles = (
            Article.objects
            .filter(
                annotated_summary__isnull=False,
            )
            .exclude(
                content=""
            )
            .exclude(
                annotated_summary=""
            )
            .order_by("id")
        )

        dataset = []
        skipped = 0

        for article in articles:

            if not article.content.strip():
                skipped += 1
                continue

            dataset.append({
                "text": article.content,
                "target": article.annotated_summary,
                "article_id": article.id,
            })

        return self._build_result(
            dataset=dataset,
            total=articles.count(),
            skipped=skipped,
        )