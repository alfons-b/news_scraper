import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from django.db import transaction
from news.models import Article


def main():

    articles = Article.objects.filter(
        extraction_method=""
    ).exclude(
        url__icontains="example.com"
    )

    total = articles.count()

    print("=" * 70)
    print("SET LEGACY EXTRACTION METHOD")
    print("=" * 70)

    print(f"Target articles : {total}")

    if total == 0:
        print("\nTidak ada artikel yang perlu diubah.")
        return

    with transaction.atomic():

        updated = articles.update(
            extraction_method="LEGACY"
        )

    print(f"Updated         : {updated}")

    print("\nSTATUS")
    print("-" * 70)

    if updated == total:
        print(
            "BERHASIL: seluruh artikel EMPTY "
            "telah ditandai sebagai LEGACY."
        )
    else:
        print(
            "PERHATIAN: jumlah updated tidak sesuai "
            "dengan jumlah target."
        )


if __name__ == "__main__":
    main()