import json


class TrendIndicator:
    """
        Representation of the result of the scraping of indicators
    """

    def __init__(self, summary: str, from_site: str, from_url: str):
        """
        global trend + List of TrendIndicatorDetail indicators
        :param summary: global trend value
        :param from_site: site indication
        :param from_url: url indication
        """
        self.summary = summary
        self.from_site = from_site
        self.from_url = from_url
        self.details = []

    def to_json(self) -> str:
        """
        convert trend to json
        :return: string json representation of the instance
        """
        return json.dumps(self, default=lambda x: x.__dict__)
