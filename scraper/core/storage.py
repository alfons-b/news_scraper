from news.models import Article


class ArticleStorage:

    def save_articles(self, source, articles):

        created_count = 0
        updated_count = 0

        for data in articles:

            url = data.get("url")

            if not url:
                continue

            defaults = {
                "source": source,
                "canonical_url": data.get(
                    "canonical_url",
                    ""
                ),
                "title": data.get(
                    "title",
                    ""
                ),
                "author": data.get(
                    "author",
                    ""
                ),
                "published_at": data.get(
                    "published_at"
                ),
                "content": data.get(
                    "content",
                    ""
                ),
                "image_url": data.get(
                    "image_url",
                    ""
                ),
                "category": data.get(
                    "category",
                    ""
                ),
                "raw_html": data.get(
                    "raw_html",
                    ""
                ),
                "extraction_method": data.get(
                    "extraction_method",
                    ""
                ),
                "extraction_confidence": data.get(
                    "extraction_confidence"
                ),
                "content_hash": data.get(
                    "content_hash",
                    ""
                ),
            }

            summary = data.get(
                "summary",
                ""
            ).strip()

            if summary:
                defaults["summary"] = summary

            article, created = Article.objects.update_or_create(
                url=url,
                defaults=defaults
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        return {
            "created": created_count,
            "updated": updated_count,
        }