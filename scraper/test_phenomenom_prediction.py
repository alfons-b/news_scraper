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

total = 0
ntt_count = 0
economic_count = 0
phenomenon_count = 0

for article in articles:
    total += 1

    text = f"{article.title} {article.content}"

    # Filter region
    is_ntt = region_filter.is_ntt_related(text)

    if not is_ntt:
        continue

    ntt_count += 1

    # Filter aktivitas ekonomi
    matched_keywords = economic_filter.get_matched_keywords(text)

    if not matched_keywords:
        continue

    economic_count += 1

    # Irisan kedua filter
    is_phenomenon = is_ntt and bool(matched_keywords)

    if is_phenomenon:
        phenomenon_count += 1


print("=" * 60)
print("HASIL PREDIKSI FENOMENA")
print("=" * 60)

print(f"TOTAL ARTIKEL       : {total}")
print(f"TERKAIT NTT         : {ntt_count}")
print(f"AKTIVITAS EKONOMI   : {economic_count}")
print(f"PREDIKSI FENOMENA   : {phenomenon_count}")