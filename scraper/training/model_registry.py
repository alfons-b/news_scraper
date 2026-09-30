from news.models import ModelVersion
from pathlib import Path


class ModelRegistry:

    def __init__(self):
        self.active_models = {
            "kbli": "models/KBLI/model_kbli",
            "direction": "models/direction/finbert-indonesia",
            "summarization": "models/summarizer/model_indonesian_summarizer",
        }

    def get_active_model(self, model_type):

        if model_type not in {
            "summarization",
            "kbli",
            "direction",
        }:
            raise ValueError(
                f"Model type tidak dikenal: {model_type}"
            )

        model = (
            ModelVersion.objects
            .filter(
                model_type=model_type,
                status="ACTIVE",
            )
            .order_by("-activated_at", "-id")
            .first()
        )

        if model is None:
            raise ValueError(
                f"Tidak ada model aktif untuk "
                f"{model_type}."
            )

        return model

    def register_candidate(
        self,
        model_type,
        model_path,
        metrics,
    ):

        if model_type not in {
            "summarization",
            "kbli",
            "direction",
        }:
            raise ValueError(
                f"Model type tidak dikenal: {model_type}"
            )

        latest = (
            ModelVersion.objects
            .filter(model_type=model_type)
            .order_by("-id")
            .first()
        )

        if latest is None:
            next_version = "v1"
        else:
            latest_number = int(
                latest.version.replace("v", "")
            )
            next_version = f"v{latest_number + 1}"

        candidate = ModelVersion.objects.create(
            model_type=model_type,
            version=next_version,
            model_path=model_path,
            metrics=metrics,
            status="CANDIDATE",
        )

        return candidate


    def should_promote(
        self,
        candidate_metrics,
        active_metrics,
    ):
        candidate_f1 = candidate_metrics.get("macro_f1")
        active_f1 = active_metrics.get("macro_f1")

        candidate_accuracy = candidate_metrics.get("accuracy")
        active_accuracy = active_metrics.get("accuracy")

        if candidate_f1 is None:
            raise ValueError(
                "Candidate tidak memiliki macro_f1."
            )

        if active_f1 is None:
            raise ValueError(
                "Active model tidak memiliki macro_f1."
            )

        if candidate_accuracy is None:
            raise ValueError(
                "Candidate tidak memiliki accuracy."
            )

        if active_accuracy is None:
            raise ValueError(
                "Active model tidak memiliki accuracy."
            )

        if candidate_f1 > active_f1 and candidate_accuracy >= active_accuracy:
            return True

        return False


    def promote_candidate(self, candidate):

        if candidate.status != "CANDIDATE":
            raise ValueError(
                "Hanya model dengan status "
                "CANDIDATE yang dapat dipromosikan."
            )

        candidate_path = Path(candidate.model_path)

        if not candidate_path.exists():
            raise ValueError(
                f"File model candidate tidak ditemukan: "
                f"{candidate.model_path}"
            )

        ModelVersion.objects.filter(
            model_type=candidate.model_type,
            status="ACTIVE",
        ).update(
            status="REJECTED"
        )

        candidate.status = "ACTIVE"

        from django.utils import timezone

        candidate.activated_at = timezone.now()

        candidate.save(
            update_fields=[
                "status",
                "activated_at",
            ]
        )

        return candidate

    def resolve_model_path(self, model):

        project_root = (
            Path(__file__).resolve().parents[2]
        )

        model_path = Path(
            model.model_path
        )

        if not model_path.is_absolute():
            model_path = (
                project_root / model_path
            )

        return model_path