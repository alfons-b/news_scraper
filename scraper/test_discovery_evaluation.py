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

    print("=" * 70)
    print("DISCOVERY METHOD EVALUATION")
    print("=" * 70)

    source = NewsSource.objects.get(name="Pos Kupang")

    # ==========================================================
    # AMBIL SEMUA URL DISCOVERY UNTUK SOURCE
    # ==========================================================

    discovered_urls = list(
        DiscoveredURL.objects
        .filter(source=source)
    )

    print("\nSOURCE")
    print("-" * 70)
    print("Source :", source.name)
    print("Total DiscoveredURL :", len(discovered_urls))

    # ==========================================================
    # KELOMPOKKAN URL BERDASARKAN DISCOVERY EVIDENCE
    # ==========================================================

    method_urls = {
        "RSS": set(),
        "SITEMAP": set(),
        "HTML": set(),
    }

    for discovered in discovered_urls:

        evidences = DiscoveryEvidence.objects.filter(
            discovered_url=discovered
        ).values_list(
            "discovery_method",
            flat=True
        )

        for method in evidences:

            if method in method_urls:
                method_urls[method].add(
                    discovered.url
                )

    # ==========================================================
    # JUMLAH PER METODE
    # ==========================================================

    print("\nURL PER DISCOVERY METHOD")
    print("-" * 70)

    for method, urls in method_urls.items():

        print(
            f"{method:<10}: {len(urls)}"
        )

    # ==========================================================
    # UNION
    # ==========================================================

    all_urls = set().union(
        *method_urls.values()
    )

    print("\nUNION")
    print("-" * 70)

    print(
        "Total unique URLs dari semua method :",
        len(all_urls)
    )

    # ==========================================================
    # HANYA SATU METHOD
    # ==========================================================

    only_one = {
        "RSS": [],
        "SITEMAP": [],
        "HTML": [],
    }

    for url in all_urls:

        methods = []

        for method, urls in method_urls.items():

            if url in urls:
                methods.append(method)

        if len(methods) == 1:
            only_one[methods[0]].append(url)

    print("\nURL YANG HANYA DITEMUKAN OLEH SATU METHOD")
    print("-" * 70)

    for method, urls in only_one.items():

        print(
            f"{method:<10}: {len(urls)}"
        )

    # ==========================================================
    # PASANGAN METHOD
    # ==========================================================

    rss = method_urls["RSS"]
    sitemap = method_urls["SITEMAP"]
    html = method_urls["HTML"]

    print("\nOVERLAP PASANGAN METHOD")
    print("-" * 70)

    print(
        "RSS ∩ Sitemap :",
        len(rss & sitemap)
    )

    print(
        "RSS ∩ HTML    :",
        len(rss & html)
    )

    print(
        "Sitemap ∩ HTML:",
        len(sitemap & html)
    )

    # ==========================================================
    # SEMUA METHOD
    # ==========================================================

    all_three = rss & sitemap & html

    print("\nOVERLAP SEMUA METHOD")
    print("-" * 70)

    print(
        "RSS ∩ Sitemap ∩ HTML :",
        len(all_three)
    )

    # ==========================================================
    # DISTRIBUSI JUMLAH EVIDENCE
    # ==========================================================

    counter = Counter()

    for url in all_urls:

        count = 0

        if url in rss:
            count += 1

        if url in sitemap:
            count += 1

        if url in html:
            count += 1

        counter[count] += 1

    print("\nDISTRIBUSI JUMLAH METHOD PER URL")
    print("-" * 70)

    for number in sorted(counter):

        print(
            f"Ditemukan oleh {number} method : "
            f"{counter[number]}"
        )

    # ==========================================================
    # PERSENTASE
    # ==========================================================

    print("\nPERSENTASE")
    print("-" * 70)

    total = len(all_urls)

    if total > 0:

        for number in sorted(counter):

            percentage = (
                counter[number] / total * 100
            )

            print(
                f"{number} method : "
                f"{percentage:.2f}%"
            )

    # ==========================================================
    # KESIMPULAN TEKNIS
    # ==========================================================

    print("\n" + "=" * 70)
    print("KESIMPULAN TEKNIS")
    print("=" * 70)

    print(
        "\nInterpretasi hasil harus didasarkan pada "
        "jumlah URL yang unik dan overlap antar-method."
    )

    print(
        "URL yang hanya ditemukan oleh satu method "
        "menunjukkan kontribusi unik method tersebut."
    )

    print(
        "URL yang ditemukan oleh beberapa method "
        "menunjukkan adanya overlap discovery."
    )

    print(
        "\nCatatan: hasil ini mengevaluasi discovery "
        "yang tersimpan di database, bukan coverage "
        "terhadap seluruh artikel yang tersedia di website."
    )


if __name__ == "__main__":
    main()