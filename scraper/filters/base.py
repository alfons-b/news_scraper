from abc import ABC, abstractmethod


class BaseArticleFilter(ABC):
    """
    Interface dasar untuk filter URL artikel.
    """

    @abstractmethod
    def is_article_url(self, url):
        """
        Mengembalikan True jika URL dianggap sebagai artikel.
        """
        raise NotImplementedError