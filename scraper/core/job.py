from django.utils import timezone

from news.models import ScrapeJob


class ScrapeJobManager:

    def start(self, source):
        return ScrapeJob.objects.create(
            source=source,
            status="RUNNING",
        )

    def success(
        self,
        job,
        urls_discovered,
        articles_extracted,
        articles_failed,
    ):
        job.status = "SUCCESS"
        job.finished_at = timezone.now()
        job.urls_discovered = urls_discovered
        job.articles_extracted = articles_extracted
        job.articles_failed = articles_failed

        job.save()

        return job

    def partial(
        self,
        job,
        urls_discovered,
        articles_extracted,
        articles_failed,
    ):
        job.status = "PARTIAL"
        job.finished_at = timezone.now()
        job.urls_discovered = urls_discovered
        job.articles_extracted = articles_extracted
        job.articles_failed = articles_failed

        job.save()

        return job

    def failed(
        self,
        job,
        error_message,
    ):
        job.status = "FAILED"
        job.finished_at = timezone.now()
        job.error_message = str(error_message)

        job.save()

        return job