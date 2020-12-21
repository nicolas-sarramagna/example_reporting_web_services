import unittest
import asyncio
from unittest.mock import patch, Mock
from starlette.responses import StreamingResponse
from example_reporting_web_services.app_ws import trend_indicator_from_investing, trend_indicator_from_tradingview
from example_reporting_web_services.app_ws import trend_chart_graph_from_investtech, trend_chart_rsi_from_investtech
from example_reporting_web_services.app_ws import _send_img


class AppTestCase(unittest.TestCase):
    """Tests for App Web Service """

    @patch('example_reporting_web_services.scraping.indicator.scrape_investing.ScrapeInvesting.scrape')
    def test_api_indicator_investing(self, mock_scrape):
        mock_scrape.return_value = Mock()
        mock_scrape.return_value.to_json.return_value = {'ok'}
        result = trend_indicator_from_investing()

        self.assertEqual({'ok'}, result)

    async def mocked_async_scrape(*args, **kwargs):
        """ Mock scrape """

        class MockResponse:
            def to_json(self):
                return {'ok'}

        return MockResponse()

    @patch('example_reporting_web_services.scraping.indicator.scrape_tradingview.ScrapeTradingView.scrape',
           side_effect=mocked_async_scrape)
    def test_api_indicator_tradingview(self, mock_scrape):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(trend_indicator_from_tradingview())
        self.assertEqual({'ok'}, result)
        self.assertEqual(len(mock_scrape.call_args_list), 1)

    @patch('example_reporting_web_services.scraping.chart.scrape_investtech.ScrapeInvesttech.scrape_graph')
    def test_api_chart_graph(self, mock_scrape):
        mock_scrape.return_value = b'123'

        result = trend_chart_graph_from_investtech()
        self.assertIsInstance(result, StreamingResponse)

    @patch('example_reporting_web_services.scraping.chart.scrape_investtech.ScrapeInvesttech.scrape_rsi')
    def test_api_chart_rsi(self, mock_scrape):
        mock_scrape.return_value = b'123'

        result = trend_chart_rsi_from_investtech()
        self.assertIsInstance(result, StreamingResponse)

    def test_send_img(self):
        """
        must return a StreamingResponse
        """
        response = _send_img(b'123', 'my_filename.png')
        response_header_values = response.headers.values()
        self.assertTrue("image/png" in response_header_values)
        self.assertTrue("filename=my_filename.png" in response_header_values)
