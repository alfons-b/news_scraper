from news.models import Article, EvaluationSet, EvaluationSample


class EvaluationSetManager:

    VALID_MODEL_TYPES = {
        "kbli",
        "direction",
        "summarization",
    }

    def get_annotated_articles(self, model_type):
        if model_type not in self.VALID_MODEL_TYPES:
            raise ValueError(
                f"Model type tidak valid: {model_type}"
            )

        queryset = Article.objects.filter(
            phenomenon_annotation=True,
        )

        if model_type == "kbli":
            queryset = (
                queryset
                .filter(
                    kbli_annotation__isnull=False,
                )
                .exclude(kbli_annotation="")
                .exclude(annotated_summary__isnull=True)
                .exclude(annotated_summary="")
            )

        elif model_type == "direction":
            queryset = (
                queryset
                .filter(
                    direction_annotation__isnull=False,
                )
                .exclude(direction_annotation="")
                .exclude(annotated_summary__isnull=True)
                .exclude(annotated_summary="")
            )

        elif model_type == "summarization":
            queryset = (
                queryset
                .exclude(content="")
                .exclude(annotated_summary__isnull=True)
                .exclude(annotated_summary="")
            )

        return queryset.order_by("id")

    def get_dataset_count(self, model_type):
        return self.get_annotated_articles(
            model_type
        ).count()

    def check_readiness(self, model_type):
        articles = self.get_annotated_articles(model_type)

        if model_type == "kbli":
            class_counts = {
                label: 0
                for label in "ABCDEFGHIJKLMNOPQRSTU"
            }

            for article in articles:
                label = article.kbli_annotation
                if label in class_counts:
                    class_counts[label] += 1

            insufficient_classes = [
                label
                for label, count in class_counts.items()
                if count < 10
            ]

            return {
                "ready": len(insufficient_classes) == 0,
                "model_type": model_type,
                "total": articles.count(),
                "classes": class_counts,
                "insufficient_classes": insufficient_classes,
                "reason": (
                    "Evaluation set KBLI siap dibuat."
                    if not insufficient_classes
                    else
                    "Evaluation set KBLI belum dapat dibuat "
                    "karena setiap kelas membutuhkan minimal "
                    "10 data."
                ),
            }

        if model_type == "direction":
            class_counts = {
                "meningkat": 0,
                "menurun": 0,
                "netral": 0,
            }

            for article in articles:
                label = article.direction_annotation
                if label in class_counts:
                    class_counts[label] += 1

            insufficient_classes = [
                label
                for label, count in class_counts.items()
                if count < 10
            ]

            return {
                "ready": len(insufficient_classes) == 0,
                "model_type": model_type,
                "total": articles.count(),
                "classes": class_counts,
                "insufficient_classes": insufficient_classes,
                "reason": (
                    "Evaluation set Direction siap dibuat."
                    if not insufficient_classes
                    else
                    "Evaluation set Direction belum dapat dibuat "
                    "karena setiap kelas membutuhkan minimal "
                    "10 data."
                ),
            }

        if model_type == "summarization":
            total = articles.count()

            return {
                "ready": total >= 10,
                "model_type": model_type,
                "total": total,
                "classes": {},
                "insufficient_classes": [],
                "reason": (
                    "Evaluation set Summarization siap dibuat."
                    if total >= 10
                    else
                    "Evaluation set Summarization belum dapat dibuat "
                    "karena minimal diperlukan 10 data."
                ),
            }

    def create_evaluation_set(self, model_type, version):
        readiness = self.check_readiness(model_type)

        if not readiness["ready"]:
            raise ValueError(
                f"Evaluation set {model_type} belum siap: "
                f"{readiness['reason']}"
            )

        if EvaluationSet.objects.filter(
            model_type=model_type,
            version=version,
        ).exists():
            raise ValueError(
                f"Evaluation set {model_type} {version} "
                f"sudah ada."
            )

        articles = self.get_annotated_articles(model_type)

        selected_articles = []

        if model_type == "kbli":
            for label in "ABCDEFGHIJKLMNOPQRSTU":
                class_articles = articles.filter(
                    kbli_annotation=label
                ).order_by("id")[:10]

                selected_articles.extend(class_articles)

        elif model_type == "direction":
            for label in [
                "meningkat",
                "menurun",
                "netral",
            ]:
                class_articles = articles.filter(
                    direction_annotation=label
                ).order_by("id")[:10]

                selected_articles.extend(class_articles)

        elif model_type == "summarization":
            selected_articles = list(
                articles.order_by("id")[:10]
            )

        evaluation_set = EvaluationSet.objects.create(
            model_type=model_type,
            version=version,
            description=(
                f"Frozen evaluation set {model_type} "
                f"{version}."
            ),
            is_active=True,
        )

        EvaluationSample.objects.bulk_create(
            [
                EvaluationSample(
                    evaluation_set=evaluation_set,
                    article=article,
                )
                for article in selected_articles
            ]
        )

        return {
            "evaluation_set": evaluation_set,
            "sample_count": len(selected_articles),
            "article_ids": [
                article.id
                for article in selected_articles
            ],
        }

    def get_evaluation_set(self, model_type, version=None):
        queryset = EvaluationSet.objects.filter(
            model_type=model_type,
        )

        if version is not None:
            queryset = queryset.filter(
                version=version,
            )

        evaluation_set = (
            queryset
            .order_by("-created_at", "-id")
            .first()
        )

        return evaluation_set

    def get_evaluation_samples(self, model_type, version=None):
        evaluation_set = self.get_evaluation_set(
            model_type=model_type,
            version=version,
        )

        if evaluation_set is None:
            return EvaluationSample.objects.none()

        return (
            EvaluationSample.objects
            .filter(
                evaluation_set=evaluation_set,
            )
            .select_related("article")
            .order_by("article_id")
        )