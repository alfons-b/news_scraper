import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from news.models import Article
from scraper.filters.region import NTTRegionFilter
from scraper.filters.economic_activity import EconomicActivityFilter


region_filter = NTTRegionFilter()
economic_filter = EconomicActivityFilter()

articles = Article.objects.all()

ntt_articles = []

for article in articles:
    text = f"{article.title} {article.content}"

    if region_filter.is_ntt_related(text):
        ntt_articles.append(article)


economic_articles = []
non_economic_articles = []

for article in ntt_articles:
    text = f"{article.title} {article.content}"

    if economic_filter.is_economic_activity(text):
        economic_articles.append(article)
    else:
        non_economic_articles.append(article)


print("=" * 60)
print("TEST ECONOMIC ACTIVITY FILTER")
print("=" * 60)

print(f"TOTAL ARTIKEL          : {articles.count()}")
print(f"TERKAIT NTT            : {len(ntt_articles)}")
print(f"KANDIDAT AKTIVITAS EKONOMI : {len(economic_articles)}")
print(f"BUKAN KANDIDAT EKONOMI : {len(non_economic_articles)}")

if len(ntt_articles) > 0:
    print(
        f"ECONOMIC RATE          : "
        f"{len(economic_articles) / len(ntt_articles) * 100:.2f} %"
    )


print("\n" + "=" * 60)
print("SAMPEL KANDIDAT EKONOMI")
print("=" * 60)

for i, article in enumerate(economic_articles[:20], start=1):
    print(f"\n[{i}]")
    print("TITLE :", article.title)
    print("URL   :", article.url)


print("\n" + "=" * 60)
print("SAMPEL BUKAN KANDIDAT EKONOMI")
print("=" * 60)

for i, article in enumerate(non_economic_articles[:20], start=1):
    print(f"\n[{i}]")
    print("TITLE :", article.title)
    print("URL   :", article.url)