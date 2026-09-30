from scraper.filters.region import NTTRegionFilter
from scraper.filters.economic_activity import EconomicActivityFilter


class PhenomenonFilter:

    def __init__(self):
        self.region_filter = NTTRegionFilter()
        self.economic_filter = EconomicActivityFilter()

    def predict(self, text):

        if not text:
            return {
                "ntt_related": False,
                "economic_activity": False,
                "matched_economic_keywords": [],
                "phenomenon_prediction": False,
            }

        ntt_related = (
            self.region_filter.is_ntt_related(text)
        )

        matched_keywords = (
            self.economic_filter.get_matched_keywords(text)
        )

        economic_activity = bool(
            matched_keywords
        )

        phenomenon_prediction = (
            ntt_related and economic_activity
        )

        return {
            "ntt_related": ntt_related,
            "economic_activity": economic_activity,
            "matched_economic_keywords": matched_keywords,
            "phenomenon_prediction": phenomenon_prediction,
        }