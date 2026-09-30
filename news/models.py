from django.db import models


class NewsSource(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=255, unique=True)

    rss_url = models.URLField(
        blank=True,
        null=True
    )

    sitemap_url = models.URLField(
        blank=True,
        null=True
    )

    enabled = models.BooleanField(default=True)

    scraper_type = models.CharField(
        max_length=50,
        default="generic"
    )

    configuration = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DiscoveredURL(models.Model):

    DISCOVERY_METHODS = [
        ("RSS", "RSS"),
        ("SITEMAP", "Sitemap"),
        ("HTML", "HTML"),
        ("ML", "Machine Learning"),
        ("OTHER", "Other"),
    ]

    source = models.ForeignKey(
        NewsSource,
        on_delete=models.CASCADE,
        related_name="discovered_urls"
    )

    url = models.URLField(
        max_length=2000
    )

    discovery_method = models.CharField(
        max_length=20,
        choices=DISCOVERY_METHODS
    )

    first_seen = models.DateTimeField(
        auto_now_add=True
    )

    last_seen = models.DateTimeField(
        auto_now=True
    )

    processed = models.BooleanField(
        default=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "url"],
                name="unique_source_url"
            )
        ]

    def __str__(self):
        return self.url


class DiscoveryEvidence(models.Model):

    DISCOVERY_METHODS = [
        ("RSS", "RSS"),
        ("SITEMAP", "Sitemap"),
        ("HTML", "HTML"),
        ("ML", "Machine Learning"),
        ("OTHER", "Other"),
    ]

    discovered_url = models.ForeignKey(
        DiscoveredURL,
        on_delete=models.CASCADE,
        related_name="evidences"
    )

    discovery_method = models.CharField(
        max_length=20,
        choices=DISCOVERY_METHODS
    )

    first_seen = models.DateTimeField(
        auto_now_add=True
    )

    last_seen = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "discovered_url",
                    "discovery_method"
                ],
                name="unique_discovery_evidence"
            )
        ]

    def __str__(self):

        return (
            f"{self.discovered_url.url} - "
            f"{self.discovery_method}"
        )

class Article(models.Model):

    EXTRACTION_METHODS = [
        ("JSONLD", "JSON-LD"),
        ("CONVENTIONAL", "Conventional"),
        ("READABILITY", "Readability"),
        ("COMBINED", "Combined"),
        ("LEGACY", "Legacy"),
        ("ML", "Machine Learning"),
        ("OTHER", "Other"),
    ]

    source = models.ForeignKey(
        NewsSource,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    url = models.URLField(
        max_length=2000,
        unique=True
    )

    canonical_url = models.URLField(
        max_length=2000,
        blank=True,
        null=True
    )

    title = models.TextField(
        blank=True
    )

    author = models.CharField(
        max_length=255,
        blank=True
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    content = models.TextField(
        blank=True
    )

    # ==================================================
    # HASIL SUMMARIZATION
    # ==================================================

    summary = models.TextField(
        blank=True
    )

    # ==================================================
    # HASIL FILTER FENOMENA
    # ==================================================

    ntt_related = models.BooleanField(
        null=True,
        blank=True
    )

    economic_activity = models.BooleanField(
        null=True,
        blank=True
    )

    matched_economic_keywords = models.JSONField(
        default=list,
        blank=True
    )

    phenomenon_prediction = models.BooleanField(
        null=True,
        blank=True
    )

    # ==================================================
    # HASIL PREDIKSI MODEL
    # ==================================================

    kbli_prediction = models.CharField(
        max_length=1,
        blank=True,
        null=True
    )

    direction_prediction = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # ==================================================
    # HASIL ANOTASI
    # ==================================================

    annotated_summary = models.TextField(
        blank=True,
        null=True
    )

    phenomenon_annotation = models.BooleanField(
        null=True,
        blank=True
    )

    kbli_annotation = models.CharField(
        max_length=1,
        blank=True,
        null=True
    )

    direction_annotation = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # ==================================================
    # METADATA ARTIKEL
    # ==================================================

    image_url = models.URLField(
        max_length=2000,
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=255,
        blank=True
    )

    raw_html = models.TextField(
        blank=True
    )

    extraction_method = models.CharField(
        max_length=30,
        choices=EXTRACTION_METHODS,
        blank=True
    )

    extraction_confidence = models.FloatField(
        blank=True,
        null=True
    )

    content_hash = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    def __str__(self):
        return self.title or self.url




class ScrapeJob(models.Model):

    STATUS_CHOICES = [
        ("RUNNING", "Running"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("PARTIAL", "Partial"),
    ]

    source = models.ForeignKey(
        NewsSource,
        on_delete=models.CASCADE,
        related_name="scrape_jobs"
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    finished_at = models.DateTimeField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="RUNNING"
    )

    urls_discovered = models.PositiveIntegerField(
        default=0
    )

    articles_extracted = models.PositiveIntegerField(
        default=0
    )

    articles_failed = models.PositiveIntegerField(
        default=0
    )

    error_message = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.source.name} - {self.status}"



class TrainingJob(models.Model):

    MODEL_TYPES = [
        ("summarization", "Summarization"),
        ("kbli", "KBLI"),
        ("direction", "Direction"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("RUNNING", "Running"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    model_type = models.CharField(
        max_length=30,
        choices=MODEL_TYPES,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    dataset_size = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    metrics = models.JSONField(
        default=dict,
        blank=True,
    )

    model_path = models.CharField(
        max_length=1000,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.model_type} - {self.status}"

class ModelVersion(models.Model):

    MODEL_TYPES = [
        ("summarization", "Summarization"),
        ("kbli", "KBLI"),
        ("direction", "Direction"),
    ]

    STATUS_CHOICES = [
        ("CANDIDATE", "Candidate"),
        ("ACTIVE", "Active"),
        ("REJECTED", "Rejected"),
    ]

    model_type = models.CharField(
        max_length=30,
        choices=MODEL_TYPES,
    )

    version = models.CharField(
        max_length=50,
    )

    model_path = models.CharField(
        max_length=1000,
    )

    metrics = models.JSONField(
        default=dict,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="CANDIDATE",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    activated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.model_type} "
            f"{self.version} "
            f"({self.status})"
        )

class EvaluationSet(models.Model):

    MODEL_TYPES = [
        ("summarization", "Summarization"),
        ("kbli", "KBLI"),
        ("direction", "Direction"),
    ]

    model_type = models.CharField(
        max_length=30,
        choices=MODEL_TYPES,
    )

    version = models.CharField(
        max_length=50,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.model_type} "
            f"evaluation {self.version}"
        )


class EvaluationSample(models.Model):

    evaluation_set = models.ForeignKey(
        EvaluationSet,
        on_delete=models.CASCADE,
        related_name="samples",
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="evaluation_samples",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "evaluation_set",
                    "article",
                ],
                name="unique_evaluation_article",
            )
        ]

    def __str__(self):
        return (
            f"{self.evaluation_set} - "
            f"Article {self.article_id}"
        )