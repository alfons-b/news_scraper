import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from news.models import NewsSource, DiscoveredURL
from scraper.filters.article import GenericArticleFilter


def main():

    source = NewsSource.objects.get(name="Pos Kupang")

    urls = list(
        DiscoveredURL.objects
        .filter(source=source)
        .values_list("url", flat=True)
    )

    article_filter = GenericArticleFilter()

    article_urls = []
    non_article_urls = []

    for url in urls:

        if article_filter.is_article_url(url):
            article_urls.append(url)
        else:
            non_article_urls.append(url)

    total = len(urls)
    articles = len(article_urls)
    non_articles = len(non_article_urls)

    print("=" * 70)
    print("ARTICLE FILTER EVALUATION")
    print("=" * 70)

    print("\nTOTAL")
    print("-" * 70)

    print("Total discovered URLs :", total)
    print("Article candidates    :", articles)
    print("Non-article URLs      :", non_articles)

    print("\nRATIO")
    print("-" * 70)

    if total > 0:

        print(
            f"Article candidate rate : "
            f"{articles / total * 100:.2f}%"
        )

        print(
            f"Non-article rate       : "
            f"{non_articles / total * 100:.2f}%"
        )

    print("\nCONTOH NON-ARTICLE URL")
    print("-" * 70)

    for url in non_article_urls[:20]:
        print(url)

    print("\nCONTOH ARTICLE URL")
    print("-" * 70)

    for url in article_urls[:20]:
        print(url)


if __name__ == "__main__":
    main()