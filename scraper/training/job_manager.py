from django.utils import timezone

from news.models import TrainingJob


class TrainingJobManager:

    VALID_MODEL_TYPES = {
        "summarization",
        "kbli",
        "direction",
    }

    def create_job(self, model_type):
        if model_type not in self.VALID_MODEL_TYPES:
            raise ValueError(
                f"Model type tidak valid: {model_type}"
            )

        return TrainingJob.objects.create(
            model_type=model_type,
            status="PENDING",
        )

    def start_job(self, job):
        if job is None:
            raise ValueError("Training job tidak boleh None.")

        if job.status != "PENDING":
            raise ValueError(
                f"Job tidak dapat dimulai karena status = {job.status}"
            )

        job.status = "RUNNING"
        job.started_at = timezone.now()

        job.save(
            update_fields=[
                "status",
                "started_at",
                "updated_at",
            ]
        )

        return job

    def success_job(
        self,
        job,
        dataset_size=None,
        metrics=None,
        model_path=None,
    ):
        if job is None:
            raise ValueError("Training job tidak boleh None.")

        if job.status != "RUNNING":
            raise ValueError(
                f"Job tidak dapat diselesaikan karena status = {job.status}"
            )

        job.status = "SUCCESS"
        job.finished_at = timezone.now()

        if dataset_size is not None:
            job.dataset_size = dataset_size

        if metrics is not None:
            job.metrics = metrics

        if model_path is not None:
            job.model_path = model_path

        job.save(
            update_fields=[
                "status",
                "finished_at",
                "dataset_size",
                "metrics",
                "model_path",
                "updated_at",
            ]
        )

        return job

    def failed_job(self, job, error):
        if job is None:
            raise ValueError("Training job tidak boleh None.")

        if job.status != "RUNNING":
            raise ValueError(
                f"Job tidak dapat gagal karena status = {job.status}"
            )

        job.status = "FAILED"
        job.finished_at = timezone.now()
        job.error_message = str(error)

        job.save(
            update_fields=[
                "status",
                "finished_at",
                "error_message",
                "updated_at",
            ]
        )

        return job