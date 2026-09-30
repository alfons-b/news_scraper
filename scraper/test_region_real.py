import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from news.models import Article
from scraper.filters.region import NTTRegionFilter


filter_ntt = NTTRegionFilter()

articles = Article.objects.all()

total = articles.count()
ntt_articles = []
non_ntt_articles = []

for article in articles:

    text = f"{article.title} {article.content}"

    if filter_ntt.is_ntt_related(text):
        ntt_articles.append(article)
    else:
        non_ntt_articles.append(article)


print("=" * 60)
print("TEST REGION FILTER - DATA NYATA")
print("=" * 60)

print(f"TOTAL ARTIKEL : {total}")
print(f"TERKAIT NTT   : {len(ntt_articles)}")
print(f"TIDAK NTT     : {len(non_ntt_articles)}")

if total > 0:
    print(
        f"NTT RATE      : "
        f"{len(ntt_articles) / total * 100:.2f} %"
    )

print("\n" + "=" * 60)
print("SAMPEL ARTIKEL TERKAIT NTT")
print("=" * 60)

for i, article in enumerate(ntt_articles[:20], start=1):
    print(f"\n[{i}]")
    print("TITLE :", article.title)
    print("URL   :", article.url)

print("\n" + "=" * 60)
print("SAMPEL ARTIKEL TIDAK TERKAIT NTT")
print("=" * 60)

for i, article in enumerate(non_ntt_articles[:20], start=1):
    print(f"\n[{i}]")
    print("TITLE :", article.title)
    print("URL   :", article.url)