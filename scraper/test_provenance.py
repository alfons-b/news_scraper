import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from news.models import Article

from scraper.core.fetcher import HTMLFetcher
from scraper.extractors.jsonld import JSONLDExtractor
from scraper.extractors.conventional import ConventionalExtractor
from scraper.extractors.readability import ReadabilityExtractor


def determine_method(jsonld_result, conventional_result, readability_result):
    """
    Menentukan metode ekstraksi berdasarkan extractor
    yang berhasil menghasilkan data.
    """

    if jsonld_result and conventional_result:
        return "COMBINED"

    if conventional_result:
        return "CONVENTIONAL"

    if jsonld_result:
        return "JSONLD"

    if readability_result:
        return "READABILITY"

    return "FAILED"


def main():

    articles = Article.objects.exclude(
        url__icontains="example.com"
    ).order_by("id")[:10]

    fetcher = HTMLFetcher()

    jsonld_extractor = JSONLDExtractor()
    conventional_extractor = ConventionalExtractor()
    readability_extractor = ReadabilityExtractor()

    print("=" * 70)
    print("PROVENANCE VALIDATION - 10 REAL ARTICLES")
    print("=" * 70)

    results = []

    for index, article in enumerate(
        articles,
        start=1
    ):

        print(f"\n[{index}/10]")
        print(f"ID    : {article.id}")
        print(f"Title : {article.title}")
        print(f"URL   : {article.url}")

        try:
            html = fetcher.fetch(article.url)

            jsonld_result = jsonld_extractor.extract(
                html,
                article.url
            )

            conventional_result = conventional_extractor.extract(
                html,
                article.url
            )

            readability_result = readability_extractor.extract(
                html,
                article.url
            )

            method = determine_method(
                jsonld_result,
                conventional_result,
                readability_result
            )

            results.append(method)

            print(
                f"JSON-LD      : "
                f"{'YES' if jsonld_result else 'NO'}"
            )

            print(
                f"Conventional : "
                f"{'YES' if conventional_result else 'NO'}"
            )

            print(
                f"Readability  : "
                f"{'YES' if readability_result else 'NO'}"
            )

            print(
                f"FINAL METHOD : {method}"
            )

        except Exception as e:

            results.append("FAILED")

            print(
                f"ERROR        : {e}"
            )

            print(
                "FINAL METHOD : FAILED"
            )

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for method in [
        "JSONLD",
        "CONVENTIONAL",
        "READABILITY",
        "COMBINED",
        "FAILED",
    ]:

        count = results.count(method)

        print(
            f"{method:<15}: {count}"
        )

    print("=" * 70)


if __name__ == "__main__":
    main()