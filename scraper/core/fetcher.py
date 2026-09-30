import requests


class HTMLFetcher:
    """
    Mengambil HTML dari sebuah URL artikel.

    Tanggung jawab:
    - melakukan HTTP request
    - menangani redirect
    - mengembalikan HTML
    - tidak melakukan parsing atau extraction
    """

    def __init__(self, timeout=30):
        self.timeout = timeout

        self.headers = {
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

    def fetch(self, url):

        response = requests.get(
            url,
            headers=self.headers,
            timeout=self.timeout,
            allow_redirects=True,
        )

        response.raise_for_status()

        return response.text