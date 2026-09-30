import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from news.models import ScrapeJob, Article


def percentage(numerator, denominator):
    if denominator == 0:
        return 0

    return (numerator / denominator) * 100


def main():

    print("=" * 70)
    print("SCRAPER PIPELINE EVALUATION")
    print("=" * 70)

    # ==========================================================
    # AMBIL JOB TERAKHIR
    # ==========================================================

    job = (
        ScrapeJob.objects
        .order_by("-started_at")
        .first()
    )

    if job is None:
        print("Tidak ada ScrapeJob.")
        return

    print("\nLATEST SCRAPE JOB")
    print("-" * 70)

    print("Job ID             :", job.id)
    print("Source             :", job.source.name)
    print("Status             :", job.status)
    print("Started            :", job.started_at)
    print("Finished           :", job.finished_at)

    # ==========================================================
    # DATA PIPELINE
    # ==========================================================

    discovered = job.urls_discovered
    extracted = job.articles_extracted
    failed = job.articles_failed

    print("\nPIPELINE COUNTS")
    print("-" * 70)

    print("URLs discovered    :", discovered)
    print("Articles extracted  :", extracted)
    print("Articles failed     :", failed)

    # ==========================================================
    # EXTRACTION SUCCESS RATE
    # ==========================================================

    attempted = extracted + failed

    extraction_success_rate = percentage(
        extracted,
        attempted
    )

    print("\n1. EXTRACTION SUCCESS RATE")
    print("-" * 70)

    print("Extraction attempted :", attempted)
    print("Extraction success   :", extracted)
    print("Extraction failed    :", failed)
    print(
        f"Success rate         : "
        f"{extraction_success_rate:.2f}%"
    )

    # ==========================================================
    # DISCOVERY → EXTRACTION
    # ==========================================================

    discovery_to_extraction = percentage(
        extracted,
        discovered
    )

    print("\n2. DISCOVERY → EXTRACTION")
    print("-" * 70)

    print(
        f"Extracted / Discovered : "
        f"{discovery_to_extraction:.2f}%"
    )

    # ==========================================================
    # DATABASE ARTICLES
    # ==========================================================

    combined_articles = Article.objects.filter(
        source=job.source,
        extraction_method="COMBINED"
    ).count()

    print("\n3. DATABASE")
    print("-" * 70)

    print(
        "COMBINED articles for source :",
        combined_articles
    )

    # ==========================================================
    # SCRAPE JOB HISTORY
    # ==========================================================

    print("\n4. SCRAPE JOB HISTORY")
    print("-" * 70)

    jobs = (
        ScrapeJob.objects
        .filter(source=job.source)
        .order_by("-started_at")[:10]
    )

    for item in jobs:

        print(
            f"Job {item.id:<4} | "
            f"{item.status:<8} | "
            f"discovered={item.urls_discovered:<4} | "
            f"extracted={item.articles_extracted:<4} | "
            f"failed={item.articles_failed:<4}"
        )

    # ==========================================================
    # INTERPRETATION
    # ==========================================================

    print("\n" + "=" * 70)
    print("INTERPRETASI")
    print("=" * 70)

    print(
        "\nCatatan: Discovery → Extraction bukan coverage "
        "terhadap seluruh berita Pos Kupang."
    )

    print(
        "Metrik tersebut hanya menunjukkan berapa bagian "
        "dari URL yang ditemukan sistem yang berhasil "
        "menjadi artikel hasil ekstraksi."
    )

    print(
        "\nUntuk mengukur coverage sebenarnya, kita perlu "
        "dataset pembanding/ground truth."
    )


if __name__ == "__main__":
    main()