import unittest

from example_reporting_web_services.scraping.indicator.trend_indicator import TrendIndicator
from example_reporting_web_services.scraping.indicator.trend_indicator_detail import TrendIndicatorDetail


class TrendIndicatorTestCase(unittest.TestCase):
    """Tests for TrendIndicator """

    def test_constructor_fill_fields(self):
        """ must fill all fields """
        indicator = TrendIndicator("summary", "from_site", "from_url")
        self.assertEqual("summary", indicator.summary)
        self.assertEqual("from_site", indicator.from_site)
        self.assertEqual("from_url", indicator.from_url)
        self.assertEqual([], indicator.details)

    def test_trend_to_json_no_details(self):
        """ must convert trend object to json format"""
        result_json = TrendIndicator("summary", "from_site", "from_url").to_json()
        expected = '{"summary": "summary", "from_site": "from_site", "from_url": "from_url", "details": []}'
        self.assertEqual(expected, result_json)

    def test_trend_to_json_with_details(self):
        """ must convert trend object to json format"""
        indicator = TrendIndicator("summary", "from_site", "from_url")
        indicator.details.append(TrendIndicatorDetail("trend_name", "trend_value", 0, 1, 2))
        result_json = indicator.to_json()
        # multiple lines without additional spaces or \n
        expected = ''.join(['{"summary": "summary", "from_site": "from_site", "from_url": "from_url",',
                            ' "details": [{"trend_name": "trend_name", "trend_value": "trend_value",',
                            ' "trend_buy": 0, "trend_sell": 1, "trend_neutral": 2}]}'])
        self.assertEqual(expected, result_json)
