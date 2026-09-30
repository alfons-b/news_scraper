import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from news.models import Article
from scraper.extractors.jsonld import JSONLDExtractor
from scraper.extractors.conventional import ConventionalExtractor
from scraper.extractors.merger import ExtractionMerger


def main():

    article = Article.objects.get(id=3)

    print("=" * 70)
    print("OLD ARTICLE VS CURRENT EXTRACTION")
    print("=" * 70)

    print("\nDATA LAMA")
    print("-" * 70)
    print("ID              :", article.id)
    print("Title           :", article.title)
    print("URL             :", article.url)
    print("Content length  :", len(article.content or ""))
    print("Raw HTML length :", len(article.raw_html or ""))
    print("Method lama     :", repr(article.extraction_method))

    if not article.raw_html:
        print("\nRAW HTML TIDAK TERSEDIA")
        print("Perbandingan tidak dapat dilakukan.")
        return

    html = article.raw_html

    jsonld = JSONLDExtractor()
    conventional = ConventionalExtractor()
    merger = ExtractionMerger()

    jsonld_result = jsonld.extract(html, article.url)
    conventional_result = conventional.extract(html, article.url)

    merged_result = merger.merge(
        jsonld_result,
        conventional_result
    )

    print("\nHASIL JSON-LD SEKARANG")
    print("-" * 70)

    if jsonld_result:
        print("Title          :", jsonld_result.get("title"))
        print("Author         :", jsonld_result.get("author"))
        print("Published      :", jsonld_result.get("published_at"))
        print("Content length :", len(jsonld_result.get("content", "") or ""))
    else:
        print("JSON-LD        : GAGAL")

    print("\nHASIL CONVENTIONAL SEKARANG")
    print("-" * 70)

    if conventional_result:
        conventional_content = conventional_result.get("content", "")

        print("Content length :", len(conventional_content or ""))
        print("Content awal   :", conventional_content[:300])
    else:
        print("CONVENTIONAL   : GAGAL")

    print("\nHASIL MERGER SEKARANG")
    print("-" * 70)

    if merged_result:
        new_content = merged_result.get("content", "")

        print("Title          :", merged_result.get("title"))
        print("Author         :", merged_result.get("author"))
        print("Published      :", merged_result.get("published_at"))
        print("Content length :", len(new_content or ""))
        print("Method baru    :", merged_result.get("extraction_method"))

        print("\nCONTENT LAMA vs BARU")
        print("-" * 70)

        old_content = article.content or ""

        print("Panjang lama :", len(old_content))
        print("Panjang baru :", len(new_content))

        print(
            "Isi sama persis :",
            old_content.strip() == new_content.strip()
        )

        print("\nCONTENT LAMA - 300 KARAKTER PERTAMA")
        print("-" * 70)
        print(old_content[:300])

        print("\nCONTENT BARU - 300 KARAKTER PERTAMA")
        print("-" * 70)
        print(new_content[:300])

    else:
        print("MERGER : GAGAL")


if __name__ == "__main__":
    main()