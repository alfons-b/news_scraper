import requests
import feedparser

from .base import BaseDiscovery


class RSSDiscovery(BaseDiscovery):
    """
    Discovery URL artikel melalui RSS Feed.
    """

    def discover(self, source):

        if not source.rss_url:
            raise ValueError(
                f"RSS URL belum dikonfigurasi untuk source: {source.name}"
            )

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            ),
            "Accept": (
                "application/rss+xml, "
                "application/xml, "
                "text/xml, "
                "text/html;q=0.9, "
                "*/*;q=0.8"
            ),
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        response = requests.get(
            source.rss_url,
            headers=headers,
            timeout=30,
            allow_redirects=True,
        )

        response.raise_for_status()

        feed = feedparser.parse(response.content)

        urls = []

        for entry in feed.entries:

            url = entry.get("link")

            if url:
                urls.append(url)

        return urls