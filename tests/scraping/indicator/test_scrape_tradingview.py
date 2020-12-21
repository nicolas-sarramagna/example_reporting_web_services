import asyncio
import unittest
from unittest import mock
from unittest.mock import patch

from example_reporting_web_services.scraping.indicator.scrape_tradingview import ScrapeTradingView
from example_reporting_web_services.scraping.indicator.trend_indicator import TrendIndicator
from example_reporting_web_services.scraping.indicator.trend_indicator_detail import TrendIndicatorDetail


class ScrapeTradingViewTestCase(unittest.TestCase):
    """Tests for ScrapeTradingView """

    def test_constructor_fill_fields(self):
        """ must fill all fields """
        scrape = ScrapeTradingView()
        self.assertIsNotNone(scrape)

    async def mocked_requests_get(*args, **kwargs):
        """ Mock request """

        if 'tradingview' in args[0]:
            return MockResponse(200)

        return MockResponse(500)

    @mock.patch('requests.sessions.Session.get', side_effect=mocked_requests_get)
    def test_do_call_return_content(self, mock_get):
        """ must return response content """
        scrape = ScrapeTradingView()
        loop = asyncio.get_event_loop()
        data_res = loop.run_until_complete(scrape._scrape_tradingview())

        self.assertEqual('html', data_res)
        self.assertEqual(len(mock_get.call_args_list), 1)

    async def mocked_requests_get_exception(*args, **kwargs):
        """ Mock request """
        return MockResponse(500)

    @mock.patch('requests.sessions.Session.get', side_effect=mocked_requests_get_exception)
    def test_call_exception(self, mock_get):
        """ must return exception status != 200 """
        scrape = ScrapeTradingView()
        with self.assertRaises(ValueError) as context:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(scrape._scrape_tradingview())

        self.assertTrue('status code != 200' in str(context.exception))
        self.assertEqual(len(mock_get.call_args_list), 1)

    @mock.patch('requests.sessions.Session.get', side_effect=mocked_requests_get)
    def test_scrape_general(self, mock_get):
        """ must call internal methods """

        with patch.object(ScrapeTradingView, '_parse_tradingview') as mock_method:
            scrape = ScrapeTradingView()
            mock_method.return_value = TrendIndicator("summary", "site", "url")
            loop = asyncio.get_event_loop()
            trend = loop.run_until_complete(scrape.scrape())

            mock_method.assert_called_once_with('html')
            self.assertEqual(len(mock_get.call_args_list), 1)
            self.assertEqual("summary", trend.summary)
            self.assertEqual("site", trend.from_site)
            self.assertEqual("url", trend.from_url)

    def test_check_trend_values(self):
        """
        raise ValueError if sum of trend values != 11 when trend_name 'oscillators' and != 17 when 'moving averages'
        """
        scrape = ScrapeTradingView()
        self.assertIsNone(scrape._check_trend_values("OscillatORS", 1, 2, 8))
        self.assertIsNone(scrape._check_trend_values("moVING AveRages", 1, 2, 14))
        with self.assertRaises(ValueError) as context:
            self.assertIsNone(scrape._check_trend_values("oscillators", 1, 2, 0))
            self.assertTrue('oscillators' in str(context.exception))
        with self.assertRaises(ValueError) as context:
            self.assertIsNone(scrape._check_trend_values("moving averages", 1, 2, 3))
            self.assertTrue('averages' in str(context.exception))

    def test_find_index_summary(self):
        """
            must return index of a trend with 'summury' name from list of TrendIndicators
            return ValueError otherwise
        """
        scrape = ScrapeTradingView()

        trends = []

        # test no data
        with self.assertRaises(ValueError) as context:
            self.assertIsNone(scrape._find_index_summary(trends))
            self.assertTrue('summary not found' in str(context.exception))

        # test no summary
        for i in range(1, 4):
            trends.append(TrendIndicatorDetail("summary" + str(i), "1"))
        with self.assertRaises(ValueError) as context:
            self.assertIsNone(scrape._find_index_summary(trends))
            self.assertTrue('summary not found' in str(context.exception))

        # test with summary
        trends.insert(2, TrendIndicatorDetail("summary", "0"))
        self.assertEqual(2, scrape._find_index_summary(trends))

        # test one element with summary
        trends2 = [trends[2]]
        del trends
        self.assertEqual(0, scrape._find_index_summary(trends2))

        # test multiple element, summary in first
        for i in range(1, 4):
            trends2.append(TrendIndicatorDetail("summary" + str(i), "1"))
        self.assertEqual(0, scrape._find_index_summary(trends2))
        # test multiple element, summary in end
        del trends2[0]
        trends2.append(TrendIndicatorDetail("summary", "0"))
        self.assertEqual(len(trends2) - 1, scrape._find_index_summary(trends2))

    def test_parse_tradingview_no_details(self):
        """
        must build a trend object from html
        """
        html = """<div class='speedometerWrapper'><span class='speedometerTitle'>summary</span>
                    <span class='speedometerSignal'>myvalue</span>
               
                          <span class='counterNumber sellColor'>0</span>
                          <span class='counterNumber neutralColor'>1</span>
                          <span class='counterNumber buyColor'>2</span>
                      
              </div>
        """.replace('\n', '')
        scrape = ScrapeTradingView()
        trend = scrape._parse_tradingview(html)
        self.assertEqual('myvalue', trend.summary)
        self.assertEqual([], trend.details)

    def test_parse_tradingview_with_details(self):
        """
        must build a trend object from html with details
        """
        html = """<div class='speedometerWrapper'><span class='speedometerTitle'>summary</span>
                    <span class='speedometerSignal'>myvalue</span>
                         <span class='counterNumber sellColor'>0</span>
                          <span class='counterNumber neutralColor'>1</span>
                          <span class='counterNumber buyColor'>2</span>
              </div><div class='speedometerWrapper'>
                    <span class='speedometerTitle'>moving averages</span>
                    <span class='speedometerSignal'>myvalue2</span>
                          <span class='counterNumber sellColor'>3</span>
                          <span class='counterNumber neutralColor'>4</span>
                          <span class='counterNumber buyColor'>10</span>
              </div>
        """.replace('\n', '')
        scrape = ScrapeTradingView()
        trend = scrape._parse_tradingview(html)
        self.assertEqual('myvalue', trend.summary)
        self.assertEqual(1, len(trend.details))
        detail = trend.details[0]
        self.assertEqual('moving averages', detail.trend_name)
        self.assertEqual('myvalue2', detail.trend_value)
        self.assertEqual(3, detail.trend_sell)
        self.assertEqual(4, detail.trend_neutral)
        self.assertEqual(10, detail.trend_buy)

    def test_parse_tradingview_raise_exception(self):
        """
        must raise a ValueError, details on trend values not found
        """
        html = """<div class='speedometerWrapper'><span class='speedometerTitle'>summary</span>
                    <span class='speedometerSignal'>myvalue</span>
                         <span class='counterNumber selColor'>0</span>
                          <span class='counterNumber netralColor'>1</span>
                          <span class='counterNumber buColor'>2</span>
              </div>
        """.replace('\n', '')
        scrape = ScrapeTradingView()
        with self.assertRaises(ValueError) as context:
            self.assertIsNone(scrape._parse_tradingview(html))
            self.assertTrue('no match found in' in str(context.exception))


class HTML:
    def __init__(self):
        self.raw_html = 'html'

    async def arender(self, timeout: 0):
        """ mock method """
        pass


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code
        self.html = HTML()
