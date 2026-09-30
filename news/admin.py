from django.contrib import admin
from .models import DiscoveryEvidence
from .models import (
    NewsSource,
    DiscoveredURL,
    Article,
    ScrapeJob,
)


@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "domain",
        "enabled",
        "scraper_type",
        "created_at",
    )

    list_filter = (
        "enabled",
        "scraper_type",
    )

    search_fields = (
        "name",
        "domain",
    )


@admin.register(DiscoveredURL)
class DiscoveredURLAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "source",
        "discovery_method",
        "processed",
        "first_seen",
        "last_seen",
    )

    list_filter = (
        "source",
        "discovery_method",
        "processed",
    )

    search_fields = (
        "url",
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "source",
        "extraction_method",
        "extraction_confidence",
        "published_at",
        "created_at",
    )

    list_filter = (
        "source",
        "extraction_method",
    )

    search_fields = (
        "title",
        "author",
        "url",
    )


@admin.register(ScrapeJob)
class ScrapeJobAdmin(admin.ModelAdmin):
    list_display = (
        "source",
        "status",
        "urls_discovered",
        "articles_extracted",
        "articles_failed",
        "started_at",
        "finished_at",
    )

    list_filter = (
        "source",
        "status",
    )

@admin.register(DiscoveryEvidence)
class DiscoveryEvidenceAdmin(admin.ModelAdmin):

    list_display = (
        "discovered_url",
        "discovery_method",
        "first_seen",
        "last_seen",
    )

    list_filter = (
        "discovery_method",
    )

    search_fields = (
        "discovered_url__url",
    )