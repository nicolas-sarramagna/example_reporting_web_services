import unittest

from example_reporting_web_services.scraping.indicator.trend_indicator_detail import TrendIndicatorDetail


class TrendIndicatorDetailTestCase(unittest.TestCase):
    """Tests for TrendIndicatorDetail """

    def test_constructor_fill_fields(self):
        """ must fill all fields """
        indicator = TrendIndicatorDetail("trend_name", "trend_value", 2, 1, 0)
        self.assertEqual("trend_name", indicator.trend_name)
        self.assertEqual("trend_value", indicator.trend_value)
        self.assertEqual(2, indicator.trend_buy)
        self.assertEqual(0, indicator.trend_neutral)
        self.assertEqual(1, indicator.trend_sell)

    def test_constructor_check_optional_fields(self):
        """ must put defautl values in fields not present in parameter """
        indicator = TrendIndicatorDetail("trend_name", "trend_value")
        self.assertEqual("trend_name", indicator.trend_name)
        self.assertEqual("trend_value", indicator.trend_value)
        self.assertEqual(0, indicator.trend_buy)
        self.assertEqual(0, indicator.trend_neutral)
        self.assertEqual(0, indicator.trend_sell)

    def test_str_representation(self):
        """ must have a defined str display """
        indicator = TrendIndicatorDetail("trend_name", "trend_value", 0, 1, 2)
        str_representation = indicator.__str__()
        str_expected = "trend_name trend_value sell(1) neutral (2) buy (0)"
        self.assertEqual(str_expected, str_representation)


if __name__ == '__main__':
    unittest.main()
