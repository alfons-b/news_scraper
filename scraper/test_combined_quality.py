import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from django.db.models import Count
from news.models import Article


def main():

    articles = Article.objects.filter(
        extraction_method="COMBINED"
    )

    total = articles.count()

    print("=" * 70)
    print("COMBINED ARTICLES FINAL QUALITY AUDIT")
    print("=" * 70)

    print(f"\nTotal COMBINED articles : {total}")

    # ==========================================================
    # 1. FIELD COMPLETENESS
    # ==========================================================

    title_empty = articles.filter(
        title=""
    ).count()

    content_empty = articles.filter(
        content=""
    ).count()

    author_empty = articles.filter(
        author=""
    ).count()

    published_empty = articles.filter(
        published_at__isnull=True
    ).count()

    image_empty = articles.filter(
        image_url=""
    ).count()

    hash_empty = articles.filter(
        content_hash=""
    ).count()

    print("\n1. FIELD COMPLETENESS")
    print("-" * 70)

    print(f"Title kosong         : {title_empty}")
    print(f"Content kosong       : {content_empty}")
    print(f"Author kosong        : {author_empty}")
    print(f"Published kosong     : {published_empty}")
    print(f"Image URL kosong     : {image_empty}")
    print(f"Content hash kosong  : {hash_empty}")

    # ==========================================================
    # 2. CONTENT LENGTH
    # ==========================================================

    short_200 = 0
    short_500 = 0

    for article in articles:

        length = len((article.content or "").strip())

        if length < 200:
            short_200 += 1

        if length < 500:
            short_500 += 1

    print("\n2. CONTENT LENGTH")
    print("-" * 70)

    print(f"Content < 200 karakter : {short_200}")
    print(f"Content < 500 karakter : {short_500}")

    # ==========================================================
    # 3. CONTENT HASH DUPLICATION
    # ==========================================================

    duplicate_hash_groups = (
        articles
        .values("content_hash")
        .annotate(total=Count("id"))
        .filter(total__gt=1)
    )

    duplicate_groups = duplicate_hash_groups.count()

    duplicate_articles = sum(
        item["total"]
        for item in duplicate_hash_groups
    )

    print("\n3. CONTENT HASH DUPLICATION")
    print("-" * 70)

    print(f"Duplicate hash groups : {duplicate_groups}")
    print(f"Articles in duplicates: {duplicate_articles}")

    # ==========================================================
    # 4. URL DUPLICATION
    # ==========================================================

    duplicate_url_groups = (
        articles
        .values("url")
        .annotate(total=Count("id"))
        .filter(total__gt=1)
    )

    duplicate_urls = duplicate_url_groups.count()

    print("\n4. URL DUPLICATION")
    print("-" * 70)

    print(f"Duplicate URL groups : {duplicate_urls}")

    # ==========================================================
    # 5. PROVENANCE
    # ==========================================================

    non_combined = Article.objects.exclude(
        extraction_method="COMBINED"
    ).filter(
        id__in=articles.values("id")
    ).count()

    print("\n5. PROVENANCE")
    print("-" * 70)

    print(f"Non-COMBINED articles : {non_combined}")

    # ==========================================================
    # 6. SAMPLE ARTICLES
    # ==========================================================

    print("\n6. SAMPLE CONTENT")
    print("-" * 70)

    samples = articles.order_by("id")[:5]

    for article in samples:

        content = article.content or ""

        print(f"\nID      : {article.id}")
        print(f"Title   : {article.title}")
        print(f"Length  : {len(content)}")
        print(f"Method  : {article.extraction_method}")
        print(f"Content : {content[:500]}")

    # ==========================================================
    # FINAL STATUS
    # ==========================================================

    print("\n" + "=" * 70)
    print("FINAL STATUS")
    print("=" * 70)

    if total == 0:
        print("ERROR: Tidak ada artikel COMBINED.")
        return

    if (
        title_empty == 0
        and content_empty == 0
        and hash_empty == 0
        and duplicate_groups == 0
        and duplicate_urls == 0
        and non_combined == 0
    ):
        print("STRUKTUR DATA : BERHASIL")
    else:
        print("STRUKTUR DATA : PERLU DIPERIKSA")

    print("\nCatatan:")
    print("- Author kosong tidak otomatis berarti gagal.")
    print("- Published kosong tidak otomatis berarti gagal.")
    print("- Image kosong tidak otomatis berarti gagal.")
    print("- Content < 200/500 perlu dilihat konteksnya.")
    print("- Sample content harus diperiksa secara manual.")


if __name__ == "__main__":
    main()