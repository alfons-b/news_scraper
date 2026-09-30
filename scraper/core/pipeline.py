from scraper.direction.processor import DirectionProcessor
from scraper.kbli.processor import KBLIProcessor
from scraper.filters.phenomenon_processor import PhenomenonProcessor
from scraper.summarization.processor import SummarizationProcessor
from scraper.summarization.summary_merger_v2 import SummaryMergerV2
from scraper.core.discovery_service import save_discovered_urls
from scraper.discovery.rss import RSSDiscovery
from scraper.discovery.sitemap import SitemapDiscovery
from scraper.discovery.html import HTMLDiscovery
from scraper.filters.article import GenericArticleFilter
from scraper.core.fetcher import HTMLFetcher
from scraper.core.deduplicator import URLDeduplicator
from scraper.extractors.jsonld import JSONLDExtractor
from scraper.extractors.conventional import ConventionalExtractor
from scraper.extractors.merger import ExtractionMerger
from scraper.extractors.normalizer import ArticleNormalizer
from scraper.core.content_hasher import ContentHasher
from scraper.core.content_deduplicator import ContentDeduplicator
from scraper.core.storage import ArticleStorage
from scraper.core.job import ScrapeJobManager



class ScraperPipeline:
    """
    Orchestrator utama scraper.

    Tahap saat ini:
    1. Discovery RSS
    2. Discovery Sitemap
    3. Discovery HTML
    4. URL Deduplication
    """

    def __init__(self):

        self.rss_discovery = RSSDiscovery()
        self.sitemap_discovery = SitemapDiscovery()
        self.html_discovery = HTMLDiscovery()
        self.article_filter = GenericArticleFilter()
        self.fetcher = HTMLFetcher()
        self.jsonld_extractor = JSONLDExtractor()
        self.conventional_extractor = ConventionalExtractor()
        self.extraction_merger = ExtractionMerger()
        self.url_deduplicator = URLDeduplicator()
        self.normalizer = ArticleNormalizer()
        self.content_hasher = ContentHasher()
        self.storage = ArticleStorage()
        self.phenomenon_processor = PhenomenonProcessor()
        self.summarization_processor = None
        self.kbli_processor = None
        self.direction_processor = None
        self.job_manager = ScrapeJobManager()

    def run(self, source, max_articles=None):
        

        if source is None:
            raise ValueError(
                "Source tidak boleh None"
            )

        job = self.job_manager.start(source)

        try:
            return self._run_pipeline(
                source,
                job,
                max_articles
            )

        except Exception as e:
            self.job_manager.failed(
                job,
                e
            )
            raise

    def _run_pipeline(self, source, job, max_articles=None):
        # ==================================================
        # DISCOVERY
        # ==================================================

        rss_urls = self.rss_discovery.discover(
            source
        )

        save_discovered_urls(
            source,
            "RSS",
            rss_urls,
        )


        sitemap_urls = self.sitemap_discovery.discover(
            source
        )

        save_discovered_urls(
            source,
            "SITEMAP",
            sitemap_urls,
        )


        html_urls = self.html_discovery.discover(
            source
        )

        save_discovered_urls(
            source,
            "HTML",
            html_urls,
        )

        # ==================================================
        # GABUNGKAN URL
        # ==================================================

        all_urls = (
            rss_urls
            + sitemap_urls
            + html_urls
        )

        # ==================================================
        # URL DEDUPLICATION
        # ==================================================

        unique_urls = (
            self.url_deduplicator.deduplicate(
                all_urls
            )
        )

        # ==================================================
        # ARTICLE URL FILTER
        # ==================================================

        article_urls = [
            url
            for url in unique_urls
            if self.article_filter.is_article_url(url)
        ]

        # FETCH HTML
        if max_articles is None:
            test_urls = article_urls
        else:
            test_urls = article_urls[:max_articles]

        fetched_html = []

        for url in test_urls:

            try:
                html = self.fetcher.fetch(url)

                fetched_html.append({
                    "url": url,
                    "html": html,
                })

            except Exception as e:

                fetched_html.append({
                    "url": url,
                    "html": None,
                    "error": str(e),
                })
        # EXTRACTION

        extracted_articles = []
        normalized_articles = []

        for item in fetched_html:

            html = item.get("html")
            url = item.get("url")

            if not html:
                continue

            jsonld_result = (
                self.jsonld_extractor.extract(
                    html,
                    url
                )
            )

            conventional_result = (
                self.conventional_extractor.extract(
                    html,
                    url
                )
            )

            merged_result = (
                self.extraction_merger.merge(
                    jsonld_result,
                    conventional_result
                )
            )

            if merged_result is not None:

                extracted_articles.append(
                    merged_result
                )
                normalized_result = (
                    self.normalizer.normalize(
                        merged_result
                    )
                )

                if normalized_result is not None:
                    content_hash = (
                        self.content_hasher.hash_content(
                            normalized_result.get("content", "")
                        )
                    )

                    normalized_result["content_hash"] = content_hash

                    normalized_articles.append(
                        normalized_result
                    )

        articles_failed = (
            len(test_urls)
            - len(extracted_articles)
        )

        unique_articles = []

        seen_hashes = set()

        for article in normalized_articles:

            content_hash = article.get(
                "content_hash",
                ""
            )

            if not content_hash:
                continue

            if content_hash in seen_hashes:
                continue

            seen_hashes.add(content_hash)

            unique_articles.append(
                article
            )

        storage_result = self.storage.save_articles(
            source,
            unique_articles
        )

        from news.models import Article

        article_urls = [
            article.get("url")
            for article in unique_articles
            if article.get("url")
        ]

        # ==================================================
        # PHENOMENON FILTER
        # ==================================================

        articles_for_processing = Article.objects.filter(
            url__in=article_urls
        )

        phenomenon_result = (
            self.phenomenon_processor.process_articles(
                articles_for_processing
            )
        )

        # ==================================================
        # AMBIL ARTIKEL YANG LOLOS FILTER
        # ==================================================

        articles_for_summary = Article.objects.filter(
            url__in=article_urls,
            phenomenon_prediction=True
        )

        print(
            "ARTICLES FOR SUMMARY:",
            articles_for_summary.count()
        )

        # ==================================================
        # SUMMARIZATION
        # ==================================================

        summary_result = (
            self.get_summarization_processor()
            .process_articles(
                articles_for_summary
            )
        )

        # ==================================================
        # KBLI CLASSIFICATION
        # ==================================================

        articles_for_kbli = Article.objects.filter(
            url__in=article_urls,
            phenomenon_prediction=True
        ).exclude(
            summary=""
        )

        print(
            "ARTICLES FOR KBLI:",
            articles_for_kbli.count()
        )

        kbli_result = (
            self.get_kbli_processor()
            .process_articles(
                articles_for_kbli
            )
        )

        articles_for_direction = Article.objects.filter(
            url__in=article_urls,
            phenomenon_prediction=True
        ).exclude(
            summary=""
        )

        print("ARTICLES FOR DIRECTION:", articles_for_direction.count())

        direction_result = (
            self.get_direction_processor()
            .process_articles(articles_for_direction)
        )

        if articles_failed > 0:

            job = self.job_manager.partial(
                job,
                urls_discovered=len(unique_urls),
                articles_extracted=len(extracted_articles),
                articles_failed=articles_failed,
            )

        else:

            job = self.job_manager.success(
                job,
                urls_discovered=len(unique_urls),
                articles_extracted=len(extracted_articles),
                articles_failed=articles_failed,
            ) 

        return {
            "storage": storage_result,

            "phenomenon": phenomenon_result,

            "summary": summary_result,

            "kbli": kbli_result,

            "direction": direction_result,

            "job": {
                "id": job.id,
                "status": job.status,
                "urls_discovered": job.urls_discovered,
                "articles_extracted": job.articles_extracted,
                "articles_failed": job.articles_failed,
            },

            "status": "SUCCESS",
        }
    def get_summarization_processor(self):

        if self.summarization_processor is None:
            self.summarization_processor = (
                SummarizationProcessor()
            )

        return self.summarization_processor

    def get_kbli_processor(self):

        if self.kbli_processor is None:
            self.kbli_processor = KBLIProcessor()

        return self.kbli_processor

    def get_direction_processor(self):
        if self.direction_processor is None:
            self.direction_processor = DirectionProcessor()
        return self.direction_processor

