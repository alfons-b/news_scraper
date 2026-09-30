import os

import django

# ============================================================
# DJANGO SETUP
# ============================================================

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()


# ============================================================
# IMPORT
# ============================================================

from news.models import Article

# ============================================================
# QUALITY TEST
# ============================================================

def main():

    print("=" * 70)
    print("QUALITY VALIDATION - ARTICLE DATABASE")
    print("=" * 70)

    # --------------------------------------------------------
    # AMBIL DATA
    # --------------------------------------------------------

    articles = Article.objects.filter(
        source__name="Pos Kupang"
    )

    total = articles.count()

    print("\nTOTAL")
    print("-" * 70)
    print(f"Total Articles : {total}")

    if total == 0:
        print("\nERROR: Tidak ada artikel Pos Kupang.")
        return

    # --------------------------------------------------------
    # FIELD COMPLETENESS
    # --------------------------------------------------------

    empty_title = articles.filter(
        title=""
    ).count()

    empty_content = articles.filter(
        content=""
    ).count()

    empty_author = articles.filter(
        author=""
    ).count()

    empty_published = articles.filter(
        published_at__isnull=True
    ).count()

    empty_image = articles.filter(
        image_url=""
    ).count()

    empty_hash = articles.filter(
        content_hash=""
    ).count()

    print("\nFIELD COMPLETENESS")
    print("-" * 70)

    print(f"Title kosong          : {empty_title}")
    print(f"Content kosong        : {empty_content}")
    print(f"Author kosong         : {empty_author}")
    print(f"Published kosong      : {empty_published}")
    print(f"Image URL kosong      : {empty_image}")
    print(f"Content hash kosong   : {empty_hash}")

    # --------------------------------------------------------
    # CONTENT LENGTH
    # --------------------------------------------------------

    short_content = 0

    for article in articles.only(
        "id",
        "content"
    ):
        content = article.content or ""

        if len(content.strip()) < 200:
            short_content += 1

    print("\nCONTENT LENGTH")
    print("-" * 70)

    print(
        f"Content < 200 karakter : "
        f"{short_content}"
    )

    # --------------------------------------------------------
    # SHORT CONTENT DETAIL
    # --------------------------------------------------------

    print("\nSHORT CONTENT DETAIL")
    print("-" * 70)

    for article in articles.only(
        "id",
        "url",
        "title",
        "content",
        "extraction_method"
    ):

        content = article.content or ""

        if len(content.strip()) < 200:

            print(f"ID      : {article.id}")
            print(f"Title   : {article.title}")
            print(f"URL     : {article.url}")
            print(
                f"Length  : "
                f"{len(content.strip())} karakter"
            )
            print(
                f"Method  : "
                f"{article.extraction_method or 'EMPTY'}"
            )
            print(f"Content : {content}")
            print("-" * 70)

    # --------------------------------------------------------
    # DUPLICATE HASH
    # --------------------------------------------------------

    hashes = {}

    for article in articles.only(
        "id",
        "content_hash"
    ):

        content_hash = (
            article.content_hash or ""
        )

        if not content_hash:
            continue

        hashes.setdefault(
            content_hash,
            []
        ).append(article.id)

    duplicate_groups = [
        ids
        for ids in hashes.values()
        if len(ids) > 1
    ]

    duplicate_articles = sum(
        len(ids) - 1
        for ids in duplicate_groups
    )

    print("\nCONTENT HASH")
    print("-" * 70)

    print(
        f"Unique hash groups      : "
        f"{len(hashes)}"
    )

    print(
        f"Duplicate hash groups   : "
        f"{len(duplicate_groups)}"
    )

    print(
        f"Duplicate articles      : "
        f"{duplicate_articles}"
    )

    # --------------------------------------------------------
    # EXTRACTION METHOD
    # --------------------------------------------------------

    extraction_methods = {}

    for article in articles.only(
        "extraction_method"
    ):

        method = (
            article.extraction_method
            or "EMPTY"
        )

        extraction_methods[method] = (
            extraction_methods.get(method, 0)
            + 1
        )

    print("\nEXTRACTION METHOD")
    print("-" * 70)

    for method, count in sorted(
        extraction_methods.items()
    ):
        print(
            f"{method:<20}: {count}"
        )

    # --------------------------------------------------------
    # QUALITY SUMMARY
    # --------------------------------------------------------

    quality_checks = {
        "Semua title terisi":
            empty_title == 0,

        "Semua content terisi":
            empty_content == 0,

        "Semua content >= 200 karakter":
            short_content == 0,

        "Semua content memiliki hash":
            empty_hash == 0,

        "Tidak ada duplicate content":
            duplicate_articles == 0,
    }

    print("\n" + "=" * 70)
    print("QUALITY CHECK")
    print("=" * 70)

    for name, result in quality_checks.items():
        print(
            f"{name:<40}: {result}"
        )

    all_valid = all(
        quality_checks.values()
    )

    print("\n" + "=" * 70)

    if all_valid:
        print("STATUS : QUALITY CHECK BERHASIL")
    else:
        print("STATUS : ADA DATA YANG PERLU DIPERIKSA")

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()