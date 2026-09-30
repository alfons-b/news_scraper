from news.models import Article
from .validator import AnnotationValidator


class AnnotationProcessor:

    def annotate_article(
        self,
        article,
        phenomenon_annotation=None,
        kbli_annotation=None,
        direction_annotation=None,
        annotated_summary=None,
    ):
        if not article:
            return None

        # ==================================================
        # VALIDASI
        # ==================================================

        validation = AnnotationValidator.validate(
            phenomenon_annotation=phenomenon_annotation,
            kbli_annotation=kbli_annotation,
            direction_annotation=direction_annotation,
        )

        if not validation["valid"]:
            raise ValueError(
                "; ".join(validation["errors"])
            )

        # ==================================================
        # SIMPAN ANOTASI
        # ==================================================

        if phenomenon_annotation is False:

            article.phenomenon_annotation = False
            article.kbli_annotation = None
            article.direction_annotation = None

        else:

            if phenomenon_annotation is not None:
                article.phenomenon_annotation = phenomenon_annotation

            if kbli_annotation is not None:
                article.kbli_annotation = kbli_annotation

            if direction_annotation is not None:
                article.direction_annotation = direction_annotation

        # ==================================================
        # SIMPAN KOREKSI RINGKASAN
        # ==================================================

        if annotated_summary is not None:
            article.annotated_summary = annotated_summary

        # ==================================================
        # SIMPAN KE DATABASE
        # ==================================================

        article.save(
            update_fields=[
                "phenomenon_annotation",
                "kbli_annotation",
                "direction_annotation",
                "annotated_summary",
                "updated_at",
            ]
        )

        return article

    def get_pending_articles(self):
        return Article.objects.filter(
            phenomenon_prediction=True,
            phenomenon_annotation__isnull=True,
        ).order_by("-published_at", "-id")