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

    eligible = 0
    not_eligible = 0

    print("=" * 70)
    print("LEGACY DRY RUN")
    print("=" * 70)

    print(f"Total EMPTY : {total}")

    for article in articles:

        has_title = bool((article.title or "").strip())
        has_content = bool((article.content or "").strip())
        has_hash = bool((article.content_hash or "").strip())

        if has_title and has_content and has_hash:
            eligible += 1
        else:
            not_eligible += 1

    print("\nHASIL")
    print("-" * 70)

    print(f"Akan menjadi LEGACY : {eligible}")
    print(f"Tidak memenuhi syarat : {not_eligible}")

    print("\nSYARAT")
    print("-" * 70)
    print("✓ extraction_method masih kosong")
    print("✓ title tidak kosong")
    print("✓ content tidak kosong")
    print("✓ content_hash tidak kosong")

    print("\nSTATUS")
    print("-" * 70)

    if eligible == total and not_eligible == 0:
        print(
            "DRY RUN AMAN: seluruh EMPTY memenuhi "
            "syarat untuk ditandai sebagai LEGACY."
        )
    else:
        print(
            "ADA DATA YANG TIDAK MEMENUHI SYARAT. "
            "Jangan lakukan update massal."
        )


if __name__ == "__main__":
    main()