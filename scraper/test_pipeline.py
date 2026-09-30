import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from news.models import NewsSource, Article
from scraper.core.pipeline import ScraperPipeline


def main():

    print("=" * 70)
    print("PIPELINE VALIDATION - 10 ARTICLES")
    print("=" * 70)

    # --------------------------------------------------------
    # AMBIL SOURCE
    # --------------------------------------------------------

    source = NewsSource.objects.filter(
        name="Pos Kupang"
    ).first()

    if source is None:
        print("ERROR: Source 'Pos Kupang' tidak ditemukan.")
        return

    print(f"Source : {source.name}")
    print(f"Domain : {source.domain}")

    # --------------------------------------------------------
    # JUMLAH ARTICLE SEBELUM
    # --------------------------------------------------------

    before_count = Article.objects.filter(
        source=source
    ).count()

    print(
        f"Articles sebelum pipeline : "
        f"{before_count}"
    )

    # --------------------------------------------------------
    # JALANKAN PIPELINE
    # --------------------------------------------------------

    pipeline = ScraperPipeline()

    try:

        result = pipeline.run(
            source=source,
            max_articles=None
        )

    except Exception as e:

        print("\n" + "=" * 70)
        print("PIPELINE ERROR")
        print("=" * 70)

        print(f"Error : {e}")

        raise

    # --------------------------------------------------------
    # HASIL PIPELINE
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("PIPELINE RESULT")
    print("=" * 70)

    job = result.get("job")

    print(
        f"URLs discovered : "
        f"{job.get('urls_discovered')}"
    )

    print(
        f"Articles extracted : "
        f"{job.get('articles_extracted')}"
    )

    print(
        f"Articles failed : "
        f"{job.get('articles_failed')}"
    )

    print(
        f"Job status : "
        f"{job.get('status')}"
    )

    # --------------------------------------------------------
    # AMBIL 10 ARTICLE TERBARU
    # --------------------------------------------------------

    articles = Article.objects.filter(
        source=source
    ).order_by("-updated_at")[:10]

    print("\n" + "=" * 70)
    print("EXTRACTION METHOD - 10 ARTICLES")
    print("=" * 70)

    combined_count = 0
    empty_count = 0

    for index, article in enumerate(
        articles,
        start=1
    ):

        method = (
            article.extraction_method
            or "EMPTY"
        )

        print(f"\n[{index}/10]")
        print(f"ID     : {article.id}")
        print(f"Title  : {article.title}")
        print(f"Method : {method}")
        print(
            f"Content length : "
            f"{len(article.content or '')}"
        )

        if method == "COMBINED":
            combined_count += 1

        if method == "EMPTY":
            empty_count += 1

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)

    print(
        f"COMBINED : "
        f"{combined_count}/10"
    )

    print(
        f"EMPTY    : "
        f"{empty_count}/10"
    )

    print(
        f"Job SUCCESS : "
        f"{job.get('status') == 'SUCCESS'}"
    )

    print(
        f"Pipeline STORAGE_COMPLETE : "
        f"{result.get('status') == 'STORAGE_COMPLETE'}"
    )

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    if (
        combined_count == 10
        and empty_count == 0
        and job.get("status") == "SUCCESS"
        and result.get("status") == "STORAGE_COMPLETE"
    ):

        print("\n" + "=" * 70)
        print("STATUS : BERHASIL")
        print("=" * 70)

    else:

        print("\n" + "=" * 70)
        print("STATUS : PERLU DIPERIKSA")
        print("=" * 70)


if __name__ == "__main__":
    main()