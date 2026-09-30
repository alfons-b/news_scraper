import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from scraper.extractors.merger import ExtractionMerger


def main():

    merger = ExtractionMerger()

    jsonld_result = {
        "url": "https://example.com/article",
        "canonical_url": "https://example.com/article",
        "title": "Judul Artikel",
        "author": "Penulis",
        "published_at": None,
        "content": "",
        "summary": "Ringkasan",
        "image_url": "https://example.com/image.jpg",
        "category": "",
    }

    conventional_result = {
        "url": "https://example.com/article",
        "canonical_url": "",
        "title": "",
        "author": "",
        "published_at": None,
        "content": "Ini adalah isi artikel hasil conventional extraction.",
        "summary": "",
        "image_url": "",
        "category": "",
    }

    result = merger.merge(
        jsonld_result,
        conventional_result
    )

    print("=" * 70)
    print("MERGER VALIDATION")
    print("=" * 70)

    print(f"Title            : {result.get('title')}")
    print(f"Author           : {result.get('author')}")
    print(f"Content          : {result.get('content')}")
    print(f"Image URL        : {result.get('image_url')}")
    print(
        f"Extraction Method: "
        f"{result.get('extraction_method')}"
    )

    print("=" * 70)

    assert result.get("title") == "Judul Artikel"
    assert result.get("author") == "Penulis"
    assert result.get("content") == (
        "Ini adalah isi artikel hasil conventional extraction."
    )
    assert result.get("image_url") == (
        "https://example.com/image.jpg"
    )
    assert result.get("extraction_method") == "COMBINED"

    print("STATUS : BERHASIL")


if __name__ == "__main__":
    main()