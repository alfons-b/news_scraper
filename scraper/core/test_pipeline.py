import os

import django


# ============================================================
# DJANGO SETUP
# ============================================================

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()


# ============================================================
# IMPORT
# ============================================================

from news.models import NewsSource
from scraper.core.pipeline import ScraperPipeline


# ============================================================
# TEST PIPELINE
# ============================================================

def main():

    print("=" * 70)
    print("TEST SCRAPER PIPELINE")
    print("=" * 70)

    # --------------------------------------------------------
    # SOURCE
    # --------------------------------------------------------

    try:
        source = NewsSource.objects.get(
            name="Pos Kupang"
        )
    except NewsSource.DoesNotExist:
        print("\nERROR: Source 'Pos Kupang' tidak ditemukan.")
        return

    print("\nSOURCE")
    print("-" * 70)
    print(f"Name       : {source.name}")
    print(f"Domain     : {source.domain}")
    print(f"RSS        : {source.rss_url}")
    print(f"Sitemap    : {source.sitemap_url}")

    # --------------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("MENJALANKAN PIPELINE")
    print("=" * 70)

    pipeline = ScraperPipeline()

    try:
        result = pipeline.run(source, max_articles=None)

    except Exception as e:
        print("\n" + "=" * 70)
        print("PIPELINE ERROR")
        print("=" * 70)

        print(f"Error : {e}")

        return

    # --------------------------------------------------------
    # DISCOVERY
    # --------------------------------------------------------

    rss_urls = result.get(
        "rss_urls",
        []
    )

    sitemap_urls = result.get(
        "sitemap_urls",
        []
    )

    html_urls = result.get(
        "html_urls",
        []
    )

    unique_urls = result.get(
        "unique_urls",
        []
    )

    article_urls = result.get(
        "article_urls",
        []
    )

    print("\n" + "=" * 70)
    print("DISCOVERY")
    print("=" * 70)

    print(f"RSS URLs           : {len(rss_urls)}")
    print(f"Sitemap URLs       : {len(sitemap_urls)}")
    print(f"HTML URLs          : {len(html_urls)}")
    print(f"Unique URLs        : {len(unique_urls)}")
    print(f"Article Candidates : {len(article_urls)}")

    # --------------------------------------------------------
    # FETCH
    # --------------------------------------------------------

    fetched_html = result.get(
        "fetched_html",
        []
    )

    fetch_success = sum(
        1
        for item in fetched_html
        if item.get("html")
    )

    fetch_failed = len(fetched_html) - fetch_success

    print("\n" + "=" * 70)
    print("FETCH")
    print("=" * 70)

    print(f"URLs Attempted : {len(fetched_html)}")
    print(f"Fetch Success  : {fetch_success}")
    print(f"Fetch Failed   : {fetch_failed}")

    # --------------------------------------------------------
    # EXTRACTION
    # --------------------------------------------------------

    extracted_articles = result.get(
        "extracted_articles",
        []
    )

    normalized_articles = result.get(
        "normalized_articles",
        []
    )

    unique_articles = result.get(
        "unique_articles",
        []
    )

    print("\n" + "=" * 70)
    print("EXTRACTION")
    print("=" * 70)

    print(f"Extracted Articles   : {len(extracted_articles)}")
    print(f"Normalized Articles  : {len(normalized_articles)}")
    print(f"Unique Articles      : {len(unique_articles)}")

    # --------------------------------------------------------
    # STORAGE
    # --------------------------------------------------------

    storage = result.get(
        "storage",
        {}
    )

    created = storage.get(
        "created",
        0
    )

    updated = storage.get(
        "updated",
        0
    )

    print("\n" + "=" * 70)
    print("STORAGE")
    print("=" * 70)

    print(f"Created             : {created}")
    print(f"Updated             : {updated}")

    # --------------------------------------------------------
    # JOB
    # --------------------------------------------------------

    job = result.get(
        "job",
        {}
    )

    print("\n" + "=" * 70)
    print("SCRAPE JOB")
    print("=" * 70)

    print(f"Job ID              : {job.get('id')}")
    print(f"Job Status          : {job.get('status')}")
    print(
        f"URLs Discovered     : "
        f"{job.get('urls_discovered')}"
    )
    print(
        f"Articles Extracted  : "
        f"{job.get('articles_extracted')}"
    )
    print(
        f"Articles Failed     : "
        f"{job.get('articles_failed')}"
    )

    # --------------------------------------------------------
    # PIPELINE STATUS
    # --------------------------------------------------------

    pipeline_status = result.get(
        "status"
    )

    print("\n" + "=" * 70)
    print("PIPELINE STATUS")
    print("=" * 70)

    print(
        f"Pipeline Status     : "
        f"{pipeline_status}"
    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("VALIDASI")
    print("=" * 70)

    pipeline_generated_articles = (
        len(unique_articles) > 0
    )

    storage_processed_articles = (
        created + updated == len(unique_articles)
    )

    job_created = (
        job.get("id") is not None
    )

    job_success = (
        job.get("status") == "SUCCESS"
    )

    job_urls_correct = (
        job.get("urls_discovered")
        == len(unique_urls)
    )

    job_articles_correct = (
        job.get("articles_extracted")
        == len(extracted_articles)
    )

    job_failed_correct = (
        job.get("articles_failed")
        == len(article_urls)
        - len(extracted_articles)
    )

    job_finished_correct = (
        job.get("status")
        in ["SUCCESS", "PARTIAL"]
    )

    print(
        "Pipeline menghasilkan artikel : "
        f"{pipeline_generated_articles}"
    )

    print(
        "Storage memproses semua       : "
        f"{storage_processed_articles}"
    )

    print(
        "Job berhasil dibuat           : "
        f"{job_created}"
    )

    print(
        "Job status SUCCESS             : "
        f"{job_success}"
    )

    print(
        "Jumlah URL Job benar          : "
        f"{job_urls_correct}"
    )

    print(
        "Jumlah artikel Job benar      : "
        f"{job_articles_correct}"
    )

    print(
        "Jumlah failed Job benar       : "
        f"{job_failed_correct}"
    )

    print(
        "Job selesai dengan benar      : "
        f"{job_finished_correct}"
    )

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    all_valid = all([
        pipeline_generated_articles,
        storage_processed_articles,
        job_created,
        job_success,
        job_urls_correct,
        job_articles_correct,
        job_failed_correct,
        job_finished_correct,
    ])

    print("\n" + "=" * 70)

    if all_valid:
        print("STATUS : BERHASIL")
    else:
        print("STATUS : GAGAL")

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()

