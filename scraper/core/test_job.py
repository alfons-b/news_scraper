import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from news.models import NewsSource
from scraper.core.job import ScrapeJobManager


source = NewsSource.objects.get(
    name="Pos Kupang"
)

manager = ScrapeJobManager()

print("=" * 70)
print("TEST SCRAPE JOB")
print("=" * 70)

job = manager.start(source)

print()
print("JOB CREATED")
print("-" * 70)
print("ID     :", job.id)
print("Source :", job.source.name)
print("Status :", job.status)

assert job.status == "RUNNING"


manager.success(
    job,
    urls_discovered=448,
    articles_extracted=10,
    articles_failed=0,
)

job.refresh_from_db()

print()
print("JOB FINISHED")
print("-" * 70)
print("ID                  :", job.id)
print("Status              :", job.status)
print("URLs Discovered     :", job.urls_discovered)
print("Articles Extracted  :", job.articles_extracted)
print("Articles Failed     :", job.articles_failed)
print("Finished At         :", job.finished_at)

print()
print("=" * 70)
print("VALIDASI")
print("=" * 70)

print(
    "Job dibuat           :",
    job.id is not None
)

print(
    "Status RUNNING       :",
    True
)

print(
    "Status SUCCESS       :",
    job.status == "SUCCESS"
)

print(
    "Jumlah URL benar     :",
    job.urls_discovered == 448
)

print(
    "Jumlah artikel benar:",
    job.articles_extracted == 10
)

print(
    "Failed benar         :",
    job.articles_failed == 0
)

print(
    "Finished At ada      :",
    job.finished_at is not None
)

if (
    job.status == "SUCCESS"
    and job.urls_discovered == 448
    and job.articles_extracted == 10
    and job.articles_failed == 0
    and job.finished_at is not None
):
    print()
    print("STATUS : BERHASIL")
else:
    print()
    print("STATUS : GAGAL")