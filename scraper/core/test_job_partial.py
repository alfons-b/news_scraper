
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
# TEST PARTIAL
# ============================================================

def main():

    print("=" * 70)
    print("TEST SCRAPE JOB - PARTIAL")
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
    print(f"Name : {source.name}")

    # --------------------------------------------------------
    # BUAT PIPELINE
    # --------------------------------------------------------

    pipeline = ScraperPipeline()

    # --------------------------------------------------------
    # SIMPAN FETCHER ASLI
    # --------------------------------------------------------

    original_fetch = pipeline.fetcher.fetch

    # --------------------------------------------------------
    # FETCHER PALSU
    #
    # URL pertama  -> berhasil
    # URL kedua    -> gagal
    # URL berikutnya -> berhasil
    # --------------------------------------------------------

    counter = {
        "value": 0
    }

    def fake_fetch(url):

        counter["value"] += 1

        if counter["value"] == 2:
            raise Exception(
                "SIMULASI FETCH ERROR"
            )

        return original_fetch(url)

    pipeline.fetcher.fetch = fake_fetch

    # --------------------------------------------------------
    # JALANKAN PIPELINE
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("MENJALANKAN PIPELINE")
    print("=" * 70)

    try:

        result = pipeline.run(source)

    except Exception as e:

        print("\nPIPELINE ERROR")
        print(f"Error : {e}")
        return

    # --------------------------------------------------------
    # HASIL JOB
    # --------------------------------------------------------

    job = result.get(
        "job",
        {}
    )

    print("\n" + "=" * 70)
    print("SCRAPE JOB")
    print("=" * 70)

    print(
        f"Job ID              : "
        f"{job.get('id')}"
    )

    print(
        f"Job Status          : "
        f"{job.get('status')}"
    )

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
    # VALIDASI
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("VALIDASI")
    print("=" * 70)

    status_partial = (
        job.get("status")
        == "PARTIAL"
    )

    failed_exists = (
        job.get("articles_failed", 0)
        > 0
    )

    extracted_exists = (
        job.get("articles_extracted", 0)
        > 0
    )

    job_exists = (
        job.get("id") is not None
    )

    print(
        "Job berhasil dibuat       : "
        f"{job_exists}"
    )

    print(
        "Status PARTIAL benar      : "
        f"{status_partial}"
    )

    print(
        "Ada artikel gagal         : "
        f"{failed_exists}"
    )

    print(
        "Ada artikel berhasil      : "
        f"{extracted_exists}"
    )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    all_valid = all([
        job_exists,
        status_partial,
        failed_exists,
        extracted_exists,
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

