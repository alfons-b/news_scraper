
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

from news.models import NewsSource, ScrapeJob
from scraper.core.pipeline import ScraperPipeline


# ============================================================
# TEST FAILED
# ============================================================

def main():

    print("=" * 70)
    print("TEST SCRAPE JOB - FAILED")
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
    # SIMULASI ERROR FATAL
    #
    # RSS Discovery sengaja dibuat gagal.
    # --------------------------------------------------------

    def fake_rss_discover(source):

        raise RuntimeError(
            "SIMULASI FATAL ERROR - RSS Discovery gagal"
        )

    pipeline.rss_discovery.discover = fake_rss_discover

    # --------------------------------------------------------
    # JALANKAN PIPELINE
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("MENJALANKAN PIPELINE")
    print("=" * 70)

    try:

        pipeline.run(source)

        print(
            "\nERROR: Pipeline seharusnya menghasilkan "
            "exception."
        )

        return

    except Exception as e:

        print("\nEXCEPTION TERTANGKAP")
        print(f"Error : {e}")

    # --------------------------------------------------------
    # AMBIL JOB TERAKHIR
    # --------------------------------------------------------

    job = (
        ScrapeJob.objects
        .filter(source=source)
        .order_by("-id")
        .first()
    )

    # --------------------------------------------------------
    # TAMPILKAN HASIL
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("SCRAPE JOB")
    print("=" * 70)

    if job is None:

        print("Job tidak ditemukan.")
        return

    print(
        f"Job ID              : "
        f"{job.id}"
    )

    print(
        f"Job Status          : "
        f"{job.status}"
    )

    print(
        f"Finished At         : "
        f"{job.finished_at}"
    )

    print(
        f"Error Message       : "
        f"{job.error_message}"
    )

    # --------------------------------------------------------
    # VALIDASI
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("VALIDASI")
    print("=" * 70)

    job_created = (
        job is not None
    )

    status_failed = (
        job.status
        == "FAILED"
    )

    finished_exists = (
        job.finished_at is not None
    )

    error_saved = (
        "SIMULASI FATAL ERROR"
        in job.error_message
    )

    print(
        "Job berhasil dibuat       : "
        f"{job_created}"
    )

    print(
        "Status FAILED benar       : "
        f"{status_failed}"
    )

    print(
        "Finished At tersimpan     : "
        f"{finished_exists}"
    )

    print(
        "Error tersimpan           : "
        f"{error_saved}"
    )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    all_valid = all([
        job_created,
        status_failed,
        finished_exists,
        error_saved,
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

