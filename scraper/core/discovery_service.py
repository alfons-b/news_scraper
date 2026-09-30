from news.models import (
    DiscoveredURL,
    DiscoveryEvidence,
)


def save_discovered_urls(
    source,
    discovery_method,
    urls,
):
    """
    Menyimpan hasil discovery yang sudah diperoleh
    ke DiscoveredURL dan DiscoveryEvidence.
    """

    created_count = 0
    existing_count = 0

    for url in urls:

        discovered_url, created = (
            DiscoveredURL.objects.get_or_create(
                source=source,
                url=url,
                defaults={
                    "discovery_method": discovery_method,
                    "processed": False,
                },
            )
        )

        if created:

            created_count += 1

        else:

            existing_count += 1

        # Simpan bukti bahwa URL ditemukan
        # melalui metode tertentu.

        DiscoveryEvidence.objects.get_or_create(
            discovered_url=discovered_url,
            discovery_method=discovery_method,
        )

    return {
        "method": discovery_method,
        "total_found": len(urls),
        "created": created_count,
        "existing": existing_count,
    }