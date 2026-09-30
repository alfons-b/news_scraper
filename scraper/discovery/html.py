import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from .base import BaseDiscovery


class HTMLDiscovery(BaseDiscovery):
    """
    Discovery URL melalui link <a> pada halaman HTML.

    Tujuan:
    - Mengambil seluruh link dari halaman sumber
    - Mengubah relative URL menjadi absolute URL
    - Memfilter URL agar tetap berada pada domain sumber
    """

    def discover(self, source):

        if not source.domain:
            raise ValueError(
                f"Domain belum dikonfigurasi "
                f"untuk source: {source.name}"
            )

        domain = source.domain.strip()

        if not domain.startswith(
            ("http://", "https://")
        ):
            url = f"https://{domain}"
        else:
            url = domain

        url = url.rstrip("/")

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "text/html, "
                "application/xhtml+xml, "
                "application/xml;q=0.9, "
                "*/*;q=0.8"
            ),
            "Accept-Language": (
                "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
            ),
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=60,
            allow_redirects=True,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        urls = set()

        base_url = response.url

        for link in soup.find_all(
            "a",
            href=True
        ):

            href = link.get("href")

            if not href:
                continue

            href = href.strip()

            absolute_url = urljoin(
                base_url,
                href
            )

            parsed = urlparse(
                absolute_url
            )

            # Hanya HTTP/HTTPS
            if parsed.scheme not in (
                "http",
                "https",
            ):
                continue

            # Hanya domain source
            source_domain = urlparse(
                url
            ).netloc

            if parsed.netloc != source_domain:
                continue

            # Hilangkan fragment
            clean_url = absolute_url.split(
                "#",
                1
            )[0]

            urls.add(clean_url)

        return list(urls)