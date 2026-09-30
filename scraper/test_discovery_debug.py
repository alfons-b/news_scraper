import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from collections import Counter
from news.models import NewsSource, DiscoveredURL, DiscoveryEvidence


def main():

    source = NewsSource.objects.get(name="Pos Kupang")

    print("=" * 70)
    print("DISCOVERY DATABASE DEBUG")
    print("=" * 70)

    # ==========================================================
    # 1. CEK discovery_method DI DiscoveredURL
    # ==========================================================

    discovered_urls = DiscoveredURL.objects.filter(
        source=source
    )

    counter = Counter(
        discovered_urls.values_list(
            "discovery_method",
            flat=True
        )
    )

    print("\n1. DiscoveredURL.discovery_method")
    print("-" * 70)

    print("Total :", discovered_urls.count())

    for method, count in counter.items():
        print(
            f"{method:<10}: {count}"
        )

    # ==========================================================
    # 2. CEK DiscoveryEvidence
    # ==========================================================

    evidences = DiscoveryEvidence.objects.filter(
        discovered_url__source=source
    )

    evidence_counter = Counter(
        evidences.values_list(
            "discovery_method",
            flat=True
        )
    )

    print("\n2. DiscoveryEvidence.discovery_method")
    print("-" * 70)

    print("Total evidence :", evidences.count())

    for method, count in evidence_counter.items():
        print(
            f"{method:<10}: {count}"
        )

    # ==========================================================
    # 3. CONTOH DATA
    # ==========================================================

    print("\n3. SAMPLE DiscoveredURL")
    print("-" * 70)

    for item in discovered_urls[:10]:

        print(
            f"\nID     : {item.id}"
        )

        print(
            f"Method : {item.discovery_method}"
        )

        print(
            f"URL    : {item.url}"
        )

        item_evidence = list(
            DiscoveryEvidence.objects
            .filter(discovered_url=item)
            .values_list(
                "discovery_method",
                flat=True
            )
        )

        print(
            f"Evidence : {item_evidence}"
        )

    # ==========================================================
    # 4. SAMPLING PER METHOD
    # ==========================================================

    print("\n4. SAMPLE URL PER DiscoveredURL METHOD")
    print("-" * 70)

    methods = (
        discovered_urls
        .values_list("discovery_method", flat=True)
        .distinct()
    )

    for method in methods:

        print(f"\n--- {method} ---")

        samples = (
            discovered_urls
            .filter(discovery_method=method)[:5]
        )

        for item in samples:
            print(item.url)

    print("\n" + "=" * 70)
    print("DEBUG SELESAI")
    print("=" * 70)


if __name__ == "__main__":
    main()