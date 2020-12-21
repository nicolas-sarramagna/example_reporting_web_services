import unittest
from unittest import mock

from example_reporting_web_services.scraping.chart.scrape_investtech import ScrapeInvesttech


class ScrapeInvesttechTestCase(unittest.TestCase):
    """Tests for ScrapeInvesttech """

    def test_constructor_fill_fields(self):
        """ must fill all fields """
        scrape = ScrapeInvesttech()
        self.assertIsNotNone(scrape)

    def mocked_requests_get(*args, **kwargs):
        """ Mock request """

        class MockResponse:
            def __init__(self, content, status_code):
                self.content = content
                self.status_code = status_code

        if args[0] == 'urlOK':
            return MockResponse(b'00', 200)
        elif 'indicators' in args[0]:
            return MockResponse(b'01', 200)
        elif 'rsi' in args[0]:
            return MockResponse(b'010', 200)

        return MockResponse(b'01', 500)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_do_call_return_content(self, mock_get):
        """ must return response content """
        scrape = ScrapeInvesttech()
        data_res = scrape._scrape_get_simple("urlOK")
        self.assertEqual(b'00', data_res)
        self.assertEqual(len(mock_get.call_args_list), 1)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_do_call_exception(self, mock_get):
        """ must return exception status != 200 """
        scrape = ScrapeInvesttech()
        with self.assertRaises(ValueError) as context:
            scrape._scrape_get_simple("urlException")

        self.assertTrue('status code != 200' in str(context.exception))
        self.assertEqual(len(mock_get.call_args_list), 1)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_scrape_graph(self, mock_get):
        """ must return chart content """
        scrape = ScrapeInvesttech()
        data_res = scrape.scrape_graph()
        self.assertEqual(b'01', data_res)
        self.assertEqual(len(mock_get.call_args_list), 1)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_scrape_rsi(self, mock_get):
        """ must return rsi content """
        scrape = ScrapeInvesttech()
        data_res = scrape.scrape_rsi()
        self.assertEqual(b'010', data_res)
        self.assertEqual(len(mock_get.call_args_list), 1)


if __name__ == '__main__':
    unittest.main()
