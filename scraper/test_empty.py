import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from news.models import Article


def main():

    empty_articles = Article.objects.filter(
        extraction_method=""
    ).exclude(
        url__icontains="example.com"
    )

    print("=" * 70)
    print("EMPTY EXTRACTION METHOD ANALYSIS")
    print("=" * 70)

    print(
        f"Total EMPTY articles : "
        f"{empty_articles.count()}"
    )

    print("\n10 SAMPLE EMPTY ARTICLES")
    print("-" * 70)

    for article in empty_articles.order_by("id")[:10]:

        print(f"ID    : {article.id}")
        print(f"Title : {article.title}")
        print(f"URL   : {article.url}")
        print(
            f"Content length : "
            f"{len(article.content or '')}"
        )
        print("-" * 70)


if __name__ == "__main__":
    main()