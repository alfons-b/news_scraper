import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()


from news.models import NewsSource
from scraper.core.pipeline import ScraperPipeline


def main():

    # =========================
    # SOURCE
    # =========================

    source = NewsSource.objects.get(
        name="Pos Kupang"
    )

    pipeline = ScraperPipeline()

    # =========================
    # DISCOVERY
    # =========================

    print("\n" + "=" * 60)
    print("FULL PIPELINE MEASUREMENT")
    print("=" * 60)

    print("\n[1] DISCOVERY")

    rss_urls = pipeline.rss_discovery.discover(
        source
    )

    sitemap_urls = pipeline.sitemap_discovery.discover(
        source
    )

    html_urls = pipeline.html_discovery.discover(
        source
    )

    print(
        "RSS      :", len(rss_urls)
    )

    print(
        "SITEMAP  :", len(sitemap_urls)
    )

    print(
        "HTML     :", len(html_urls)
    )

    # =========================
    # GABUNGKAN URL
    # =========================

    all_urls = (
        rss_urls
        + sitemap_urls
        + html_urls
    )

    print(
        "TOTAL RAW:",
        len(all_urls)
    )

    # =========================
    # URL DEDUP
    # =========================

    unique_urls = (
        pipeline.url_deduplicator.deduplicate(
            all_urls
        )
    )

    print(
        "UNIQUE   :",
        len(unique_urls)
    )

    # =========================
    # ARTICLE FILTER
    # =========================

    article_urls = [
        url
        for url in unique_urls
        if pipeline.article_filter.is_article_url(
            url
        )
    ]

    non_article_urls = [
        url
        for url in unique_urls
        if not pipeline.article_filter.is_article_url(
            url
        )
    ]

    print("\n[2] ARTICLE FILTER")

    print(
        "ARTICLE     :",
        len(article_urls)
    )

    print(
        "NON-ARTICLE :",
        len(non_article_urls)
    )

    article_rate = (
        len(article_urls)
        / len(unique_urls)
        * 100
        if unique_urls
        else 0
    )

    print(
        "ARTICLE RATE:",
        round(article_rate, 2),
        "%"
    )

    # =========================
    # SAMPLE
    # =========================

    print("\n[3] SAMPLE ARTICLE URL")

    for url in article_urls[:10]:

        print(
            url
        )

    # =========================
    # FETCH MEASUREMENT
    # =========================

    print("\n[4] FETCH")

    fetch_success = []
    fetch_failed = []

    for index, url in enumerate(article_urls, start=1):

        try:

            html = pipeline.fetcher.fetch(url)

            fetch_success.append({
                "url": url,
                "html": html,
            })

        except Exception as e:

            fetch_failed.append({
                "url": url,
                "error": str(e),
            })

        print(
            f"\rProgress: {index}/{len(article_urls)}",
            end=""
        )

    print()

    print(
        "FETCH SUCCESS :",
        len(fetch_success)
    )

    print(
        "FETCH FAILED  :",
        len(fetch_failed)
    )

    fetch_rate = (
        len(fetch_success)
        / len(article_urls)
        * 100
        if article_urls
        else 0
    )

    print(
        "FETCH RATE    :",
        round(fetch_rate, 2),
        "%"
    )

    if fetch_failed:

        print("\nFETCH FAILED DETAILS")

        for item in fetch_failed:

            print(
                "\nURL   :",
                item["url"]
            )

            print(
                "ERROR :",
                item["error"]
            )

    # =========================
    # EXTRACTION MEASUREMENT
    # =========================

    print("\n[5] EXTRACTION")

    extraction_success = []
    extraction_failed = []

    jsonld_success = 0
    jsonld_failed = 0

    conventional_success = 0
    conventional_failed = 0

    merger_success = 0
    merger_failed = 0

    for index, item in enumerate(
        fetch_success,
        start=1
    ):

        url = item["url"]
        html = item["html"]

        try:

            jsonld_result = (
                pipeline.jsonld_extractor.extract(
                    html,
                    url
                )
            )

            if jsonld_result is not None:
                jsonld_success += 1
            else:
                jsonld_failed += 1

            conventional_result = (
                pipeline.conventional_extractor.extract(
                    html,
                    url
                )
            )

            if conventional_result is not None:
                conventional_success += 1
            else:
                conventional_failed += 1

            merged_result = (
                pipeline.extraction_merger.merge(
                    jsonld_result,
                    conventional_result
                )
            )

            if merged_result is None:

                merger_failed += 1

                extraction_failed.append({
                    "url": url,
                    "error": "Merger returned None",
                })

                continue

            merger_success += 1

            extraction_success.append({
                "url": url,
                "result": merged_result,
            })

        except Exception as e:

            extraction_failed.append({
                "url": url,
                "error": str(e),
            })

        print(
            f"\rProgress: {index}/{len(fetch_success)}",
            end=""
        )

    print()

    print(
        "JSON-LD SUCCESS      :",
        jsonld_success
    )

    print(
        "JSON-LD FAILED       :",
        jsonld_failed
    )

    print(
        "CONVENTIONAL SUCCESS :",
        conventional_success
    )

    print(
        "CONVENTIONAL FAILED  :",
        conventional_failed
    )

    print(
        "MERGER SUCCESS       :",
        merger_success
    )

    print(
        "MERGER FAILED        :",
        merger_failed
    )

    print(
        "EXTRACTION SUCCESS   :",
        len(extraction_success)
    )

    print(
        "EXTRACTION FAILED    :",
        len(extraction_failed)
    )

    extraction_rate = (
        len(extraction_success)
        / len(fetch_success)
        * 100
        if fetch_success
        else 0
    )

    print(
        "EXTRACTION RATE      :",
        round(extraction_rate, 2),
        "%"
    )

    if extraction_failed:

        print("\nEXTRACTION FAILED DETAILS")

        for item in extraction_failed:

            print(
                "\nURL   :",
                item["url"]
            )

            print(
                "ERROR :",
                item["error"]
            )

    # =========================
    # NORMALIZATION + HASH MEASUREMENT
    # =========================

    print("\n[6] NORMALIZATION + HASH")

    normalization_success = []
    normalization_failed = []

    hash_success = 0
    hash_failed = 0

    for index, item in enumerate(
        extraction_success,
        start=1
    ):

        url = item["url"]
        extracted_result = item["result"]

        try:

            normalized_result = (
                pipeline.normalizer.normalize(
                    extracted_result
                )
            )

            if normalized_result is None:

                normalization_failed.append({
                    "url": url,
                    "error": "Normalizer returned None",
                })

                continue

            normalization_success.append(
                normalized_result
            )

            content = normalized_result.get(
                "content",
                ""
            )

            try:

                content_hash = (
                    pipeline.content_hasher.hash_content(
                        content
                    )
                )

                if content_hash:

                    hash_success += 1

                    normalized_result["content_hash"] = (
                        content_hash
                    )

                else:

                    hash_failed += 1

            except Exception as e:

                hash_failed += 1

                print(
                    "\nHASH ERROR:",
                    url,
                    e
                )

        except Exception as e:

            normalization_failed.append({
                "url": url,
                "error": str(e),
            })

        print(
            f"\rProgress: {index}/{len(extraction_success)}",
            end=""
        )

    print()

    print(
        "NORMALIZATION SUCCESS :",
        len(normalization_success)
    )

    print(
        "NORMALIZATION FAILED  :",
        len(normalization_failed)
    )

    print(
        "HASH SUCCESS          :",
        hash_success
    )

    print(
        "HASH FAILED           :",
        hash_failed
    )

    normalization_rate = (
        len(normalization_success)
        / len(extraction_success)
        * 100
        if extraction_success
        else 0
    )

    hash_rate = (
        hash_success
        / len(normalization_success)
        * 100
        if normalization_success
        else 0
    )

    print(
        "NORMALIZATION RATE    :",
        round(normalization_rate, 2),
        "%"
    )

    print(
        "HASH RATE             :",
        round(hash_rate, 2),
        "%"
    )

    if normalization_failed:

        print("\nNORMALIZATION FAILED DETAILS")

        for item in normalization_failed:

            print(
                "\nURL   :",
                item["url"]
            )

            print(
                "ERROR :",
                item["error"]
            )

    # =========================
    # CONTENT DEDUPLICATION
    # =========================

    print("\n[7] CONTENT DEDUPLICATION")

    unique_articles = []
    duplicate_articles = []

    seen_hashes = set()

    for article in normalization_success:

        content_hash = article.get(
            "content_hash",
            ""
        )

        if not content_hash:
            continue

        if content_hash in seen_hashes:

            duplicate_articles.append(article)

        else:

            seen_hashes.add(content_hash)

            unique_articles.append(article)

    print(
        "INPUT ARTICLES     :",
        len(normalization_success)
    )

    print(
        "UNIQUE CONTENT     :",
        len(unique_articles)
    )

    print(
        "DUPLICATE CONTENT  :",
        len(duplicate_articles)
    )

    dedup_rate = (
        len(unique_articles)
        / len(normalization_success)
        * 100
        if normalization_success
        else 0
    )

    duplicate_rate = (
        len(duplicate_articles)
        / len(normalization_success)
        * 100
        if normalization_success
        else 0
    )

    print(
        "UNIQUE RATE        :",
        round(dedup_rate, 2),
        "%"
    )

    print(
        "DUPLICATE RATE     :",
        round(duplicate_rate, 2),
        "%"
    )

    if duplicate_articles:

        print("\nDUPLICATE CONTENT DETAILS")

        for article in duplicate_articles:

            print(
                "\nURL   :",
                article.get("url")
            )

            print(
                "HASH  :",
                article.get("content_hash")
            )

    # =========================
    # STORAGE MEASUREMENT
    # =========================

    print("\n[8] STORAGE")

    try:

        storage_result = (
            pipeline.storage.save_articles(
                source,
                unique_articles
            )
        )

        created = storage_result.get(
            "created",
            0
        )

        updated = storage_result.get(
            "updated",
            0
        )

        storage_failed = (
            len(unique_articles)
            - created
            - updated
        )

        print(
            "INPUT ARTICLES   :",
            len(unique_articles)
        )

        print(
            "CREATED          :",
            created
        )

        print(
            "UPDATED          :",
            updated
        )

        print(
            "STORAGE FAILED   :",
            storage_failed
        )

        storage_rate = (
            (created + updated)
            / len(unique_articles)
            * 100
            if unique_articles
            else 0
        )

        print(
            "STORAGE RATE     :",
            round(storage_rate, 2),
            "%"
        )

    except Exception as e:

        print(
            "STORAGE ERROR    :",
            str(e)
        )

    # =========================
    # EXTRACTION QUALITY AUDIT
    # =========================

    print("\n[9] EXTRACTION QUALITY AUDIT")

    total_articles = len(unique_articles)

    title_empty = 0
    content_empty = 0
    author_empty = 0
    published_empty = 0
    image_empty = 0

    content_under_200 = 0
    content_under_500 = 0

    quality_issues = []

    for article in unique_articles:

        url = article.get("url", "")

        title = (article.get("title") or "").strip()
        content = (article.get("content") or "").strip()
        author = (article.get("author") or "").strip()
        published_at = article.get("published_at")
        image_url = (article.get("image_url") or "").strip()

        issues = []

        # TITLE
        if not title:
            title_empty += 1
            issues.append("title kosong")

        # CONTENT
        content_length = len(content)

        if not content:
            content_empty += 1
            issues.append("content kosong")

        if content_length < 200:
            content_under_200 += 1
            issues.append(
                f"content < 200 ({content_length} karakter)"
            )

        if content_length < 500:
            content_under_500 += 1

        # AUTHOR
        if not author:
            author_empty += 1
            issues.append("author kosong")

        # PUBLISHED DATE
        if not published_at:
            published_empty += 1
            issues.append("published_at kosong")

        # IMAGE
        if not image_url:
            image_empty += 1
            issues.append("image kosong")

        if issues:

            quality_issues.append({
                "url": url,
                "title": title,
                "content_length": content_length,
                "issues": issues,
            })

    print(
        "TOTAL ARTICLES       :",
        total_articles
    )

    print(
        "TITLE EMPTY          :",
        title_empty
    )

    print(
        "CONTENT EMPTY        :",
        content_empty
    )

    print(
        "AUTHOR EMPTY         :",
        author_empty
    )

    print(
        "PUBLISHED EMPTY      :",
        published_empty
    )

    print(
        "IMAGE EMPTY          :",
        image_empty
    )

    print(
        "CONTENT < 200        :",
        content_under_200
    )

    print(
        "CONTENT < 500        :",
        content_under_500
    )

    # QUALITY RATE
    quality_success = (
        total_articles - len(quality_issues)
    )

    quality_rate = (
        quality_success
        / total_articles
        * 100
        if total_articles
        else 0
    )

    print(
        "NO QUALITY ISSUE     :",
        quality_success
    )

    print(
        "QUALITY ISSUE        :",
        len(quality_issues)
    )

    print(
        "QUALITY RATE         :",
        round(quality_rate, 2),
        "%"
    )

    if quality_issues:

        print(
            "\nQUALITY ISSUE DETAILS"
        )

        for item in quality_issues[:20]:

            print(
                "\nURL   :",
                item["url"]
            )

            print(
                "TITLE :",
                item["title"]
            )

            print(
                "LENGTH:",
                item["content_length"]
            )

            print(
                "ISSUES:",
                ", ".join(item["issues"])
            )

    # =========================
    # SAMPLE CONTENT AUDIT
    # =========================

    print("\n[10] SAMPLE CONTENT AUDIT")

    sample_articles = unique_articles[:20]

    for index, article in enumerate(
        sample_articles,
        start=1
    ):

        print("\n" + "=" * 70)

        print(
            f"SAMPLE {index}/20"
        )

        print(
            "URL:",
            article.get("url", "")
        )

        print(
            "TITLE:",
            article.get("title", "")
        )

        print(
            "METHOD:",
            article.get(
                "extraction_method",
                ""
            )
        )

        content = (
            article.get("content") or ""
        ).strip()

        print(
            "CONTENT LENGTH:",
            len(content)
        )

        print("\nCONTENT AWAL:")

        print(
            content[:1000]
        )

        print("\nCONTENT AKHIR:")

        print(
            content[-1000:]
        )

    # =========================
    # ARTICLE FILTER AUDIT
    # =========================

    print("\n[11] ARTICLE FILTER AUDIT")

    article_sample = article_urls[:30]

    non_article_urls = [
        url
        for url in unique_urls
        if not pipeline.article_filter.is_article_url(url)
    ]

    non_article_sample = non_article_urls[:30]

    print(
        "ARTICLE CANDIDATE SAMPLE :",
        len(article_sample)
    )

    print(
        "NON-ARTICLE SAMPLE       :",
        len(non_article_sample)
    )

    print("\n--- ARTICLE CANDIDATE SAMPLE ---")

    for index, url in enumerate(
        article_sample,
        start=1
    ):
        print(
            f"{index:02d}. {url}"
        )

    print("\n--- NON-ARTICLE SAMPLE ---")

    for index, url in enumerate(
        non_article_sample,
        start=1
    ):
        print(
            f"{index:02d}. {url}"
        )

    print("\n" + "=" * 60)
    print("TAHAP 9 SELESAI")
    print("=" * 60)


if __name__ == "__main__":
    main()