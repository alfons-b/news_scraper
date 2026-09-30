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

    print("=" * 70)
    print("EXTRACTION METHOD FINAL VALIDATION")
    print("=" * 70)

    total = Article.objects.count()

    print(f"\nTotal articles : {total}")

    print("\nEXTRACTION METHOD")
    print("-" * 70)

    results = (
        Article.objects
        .values("extraction_method")
        .annotate(total=Count("id"))
        .order_by("extraction_method")
    )

    for item in results:

        method = item["extraction_method"]

        if not method:
            method = "EMPTY"

        print(f"{method:<20}: {item['total']}")

    print("\nEXPECTED")
    print("-" * 70)
    print("COMBINED : 237")
    print("LEGACY   : 240")
    print("TEST     : 1")
    print("EMPTY    : 0")

    combined = Article.objects.filter(
        extraction_method="COMBINED"
    ).count()

    legacy = Article.objects.filter(
        extraction_method="LEGACY"
    ).count()

    test = Article.objects.filter(
        extraction_method="TEST"
    ).count()

    empty = Article.objects.filter(
        extraction_method=""
    ).count()

    print("\nVALIDATION")
    print("-" * 70)

    print("COMBINED benar :", combined == 237)
    print("LEGACY benar   :", legacy == 240)
    print("TEST benar     :", test == 1)
    print("EMPTY = 0      :", empty == 0)

    if (
        combined == 237
        and legacy == 240
        and test == 1
        and empty == 0
    ):
        print("\nSTATUS : BERHASIL")
    else:
        print("\nSTATUS : PERLU DIPERIKSA")


if __name__ == "__main__":
    main()