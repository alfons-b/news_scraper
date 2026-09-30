import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from news.models import Article


def main():

    articles = Article.objects.filter(
        extraction_method=""
    ).exclude(
        url__icontains="example.com"
    )

    total = articles.count()

    title_empty = 0
    content_empty = 0
    hash_empty = 0
    author_empty = 0
    published_empty = 0
    image_empty = 0
    short_content = 0

    for article in articles:

        if not (article.title or "").strip():
            title_empty += 1

        if not (article.content or "").strip():
            content_empty += 1

        if not (article.content_hash or "").strip():
            hash_empty += 1

        if not (article.author or "").strip():
            author_empty += 1

        if article.published_at is None:
            published_empty += 1

        if not (article.image_url or "").strip():
            image_empty += 1

        if len((article.content or "").strip()) < 200:
            short_content += 1

    print("=" * 70)
    print("EMPTY ARTICLES QUALITY CHECK")
    print("=" * 70)

    print(f"Total EMPTY             : {total}")

    print("\nFIELD CHECK")
    print("-" * 70)

    print(f"Title kosong            : {title_empty}")
    print(f"Content kosong          : {content_empty}")
    print(f"Content hash kosong     : {hash_empty}")
    print(f"Author kosong           : {author_empty}")
    print(f"Published kosong        : {published_empty}")
    print(f"Image URL kosong        : {image_empty}")

    print("\nCONTENT LENGTH")
    print("-" * 70)

    print(f"Content < 200 karakter : {short_content}")

    print("\nINTERPRETASI")
    print("-" * 70)

    if content_empty == 0:
        print("✓ Semua EMPTY memiliki content")

    if hash_empty == 0:
        print("✓ Semua EMPTY memiliki content_hash")

    if title_empty == 0:
        print("✓ Semua EMPTY memiliki title")

    print("\nSTATUS")
    print("-" * 70)

    if (
        content_empty == 0
        and hash_empty == 0
        and title_empty == 0
    ):
        print(
            "DATA EMPTY TERLIHAT VALID. "
            "Masalah utama kemungkinan hanya provenance metadata."
        )
    else:
        print(
            "ADA DATA EMPTY YANG PERLU DIINVESTIGASI."
        )


if __name__ == "__main__":
    main()