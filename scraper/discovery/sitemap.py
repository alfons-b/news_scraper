import time
import requests
import xml.etree.ElementTree as ET

from .base import BaseDiscovery


class SitemapDiscovery(BaseDiscovery):
    """
    Discovery URL artikel melalui Sitemap XML.

    Mendukung:
    - Sitemap biasa
    - Sitemap index
    """

    def discover(self, source):

        if not source.sitemap_url:
            raise ValueError(
                f"Sitemap URL belum dikonfigurasi "
                f"untuk source: {source.name}"
            )

        return self._discover_sitemap(
            source.sitemap_url
        )

    def _discover_sitemap(self, sitemap_url):

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "application/xml, "
                "text/xml, "
                "*/*;q=0.8"
            ),
        }

        max_retries = 3

        for attempt in range(1, max_retries + 1):

            try:

                print(
                    f"Mengambil sitemap: {sitemap_url} "
                    f"(percobaan {attempt}/{max_retries})"
                )

                response = requests.get(
                    sitemap_url,
                    headers=headers,
                    timeout=60,
                    allow_redirects=True,
                )

                response.raise_for_status()

                break

            except requests.exceptions.Timeout:

                print(
                    f"Timeout saat mengambil sitemap "
                    f"(percobaan {attempt}/{max_retries})"
                )

                if attempt == max_retries:
                    raise

                time.sleep(2)

            except requests.exceptions.RequestException:

                if attempt == max_retries:
                    raise

                time.sleep(2)

        root = ET.fromstring(
            response.content
        )

        root_tag = self._remove_namespace(
            root.tag
        )

        urls = []

        if root_tag == "urlset":

            for element in root:

                if self._remove_namespace(
                    element.tag
                ) != "url":
                    continue

                for child in element:

                    if self._remove_namespace(
                        child.tag
                    ) == "loc":

                        if child.text:
                            urls.append(
                                child.text.strip()
                            )

        elif root_tag == "sitemapindex":

            child_sitemaps = []

            for element in root:

                if self._remove_namespace(
                    element.tag
                ) != "sitemap":
                    continue

                for child in element:

                    if self._remove_namespace(
                        child.tag
                    ) == "loc":

                        if child.text:
                            child_sitemaps.append(
                                child.text.strip()
                            )

            for child_sitemap in child_sitemaps:

                child_urls = self._discover_sitemap(
                    child_sitemap
                )

                urls.extend(
                    child_urls
                )

        else:

            raise ValueError(
                f"Format sitemap tidak dikenali: "
                f"{root_tag}"
            )

        return urls

    @staticmethod
    def _remove_namespace(tag):

        if "}" in tag:
            return tag.split("}", 1)[1]

        return tag