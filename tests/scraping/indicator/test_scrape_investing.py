import unittest
from unittest import mock

from example_reporting_web_services.scraping.indicator.scrape_investing import ScrapeInvesting


class ScrapeInvestingTestCase(unittest.TestCase):
    """Tests for ScrapeInvesting """

    def test_constructor_fill_fields(self):
        """ must fill all fields """
        scrape = ScrapeInvesting()
        self.assertIsNotNone(scrape)

    def test_parse_string(self):
        """ must return int of numeric characters, 0 if no numeric value"""
        scrape = ScrapeInvesting()
        self.assertEqual(0, scrape._parse_string_to_int(""))
        self.assertEqual(0, scrape._parse_string_to_int("abc aeazez&ç'_&'&)$'"))
        self.assertEqual(0, scrape._parse_string_to_int("0azepoazj0"))
        self.assertEqual(0, scrape._parse_string_to_int("0"))
        self.assertEqual(123, scrape._parse_string_to_int(" 123 azeçàu&éjz"))
        self.assertEqual(123, scrape._parse_string_to_int("aze1çàu2&é3jz"))

    def mocked_requests_post(*args, **kwargs):
        """ Mock request """

        if 'GetTechincalData' in args[0]:
            return MockResponse('ok', 200)

        return MockResponse('ko', 500)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_do_call_return_content(self, mock_post):
        """ must return response content """
        scrape = ScrapeInvesting()
        data_res = scrape._scrape_investing()
        self.assertEqual('ok', data_res)
        self.assertEqual(len(mock_post.call_args_list), 1)

    def mocked_requests_post_exception(*args, **kwargs):
        """ Mock request """
        return MockResponse('ko', 500)

    @mock.patch('requests.post', side_effect=mocked_requests_post_exception)
    def test_do_call_exception(self, mock_post):
        """ must return exception status != 200 """
        scrape = ScrapeInvesting()
        with self.assertRaises(ValueError) as context:
            scrape._scrape_investing()

        self.assertTrue('status code != 200' in str(context.exception))
        self.assertEqual(len(mock_post.call_args_list), 1)

    def test_parse_string_ok_no_details(self):
        """ must return trend with zero details """
        scrape = ScrapeInvesting()
        html = """
            <span id='techStudiesInnerWrap'><span class='uppercaseText'>my_summary</span></span>          
        """.replace("\n", "")
        trend = scrape._parse_investing(html)
        self.assertEqual("my_summary", trend.summary)
        self.assertEqual("investing.com", trend.from_site)
        self.assertEqual("https://www.investing.com/indices/investing.com-btc-usd-technical", trend.from_url)
        self.assertEqual([], trend.details)

    def test_parse_string_ko_detail_exception(self):
        """ must raise exception on detail """
        scrape = ScrapeInvesting()
        html = """
            <span id='techStudiesInnerWrap'><span class='uppercaseText'>my_summary</span>
                <span class='summaryTableLine'><span>name1:</span><span>value1</span>
                <span>abc0</span><span>def0</span></span></span>
        """.replace("\n", "")
        with self.assertRaises(ValueError) as context:
            scrape._parse_investing(html)
        self.assertTrue('no value in trend details' in str(context.exception))

    def test_parse_string_ok_with_detail(self):
        """ must return trend with details """
        scrape = ScrapeInvesting()
        html = """
            <span id='techStudiesInnerWrap'><span class='uppercaseText'>my_summary</span>
            
                <span class='summaryTableLine'><span>name1:</span><span>value1</span>
                <span>abc1</span><span>def2</span></span></span>
        """.replace("\n", "")
        trend_details = scrape._parse_investing(html).details
        self.assertEqual(1, len(trend_details))
        self.assertEqual('name1', trend_details[0].trend_name)
        self.assertEqual('value1', trend_details[0].trend_value)
        self.assertEqual(1, trend_details[0].trend_buy)
        self.assertEqual(2, trend_details[0].trend_sell)
        self.assertEqual(0, trend_details[0].trend_neutral)

    def mocked_requests_post_all(*args, **kwargs):
        """ Mock request """

        if 'GetTechincalData' in args[0]:
            html = """
                        <span id='techStudiesInnerWrap'><span class='uppercaseText'>my_summary_end</span></span>          
                    """.replace("\n", "")
            return MockResponse(html, 200)

        return MockResponse('ko', 500)

    @mock.patch('requests.post', side_effect=mocked_requests_post_all)
    def test_do_call_return_content_all(self, mock_post):
        """ must return response content """
        scrape = ScrapeInvesting()

        trend = scrape.scrape()
        self.assertEqual(len(mock_post.call_args_list), 1)
        self.assertEqual("my_summary_end", trend.summary)
        self.assertEqual([], trend.details)

class MockResponse:
    def __init__(self, content, status_code):
        self.text = content
        self.status_code = status_code