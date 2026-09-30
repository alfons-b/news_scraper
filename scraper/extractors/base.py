from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """
    Interface dasar untuk seluruh extractor artikel.
    """

    @abstractmethod
    def extract(self, html, url=None):
        """
        Mengekstrak data artikel dari HTML.

        Parameters:
            html: HTML mentah halaman artikel
            url: URL artikel

        Returns:
            dict berisi hasil ekstraksi
        """
        raise NotImplementedError