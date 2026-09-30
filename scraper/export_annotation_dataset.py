import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from news.models import Article
from scraper.filters.region import NTTRegionFilter
from scraper.filters.economic_activity import EconomicActivityFilter

region_filter = NTTRegionFilter()
economic_filter = EconomicActivityFilter()

articles = Article.objects.all()
articles = Article.objects.all()

articles = Article.objects.all()

for article in articles:
    text = f"{article.title} {article.content}"

    is_ntt = region_filter.is_ntt_related(text)

    if not is_ntt:
        continue

    matched_keywords = economic_filter.get_matched_keywords(text)

    if not matched_keywords:
        continue

    print(article.id)
    print(article.title)
    print(matched_keywords)
    print("-" * 80)