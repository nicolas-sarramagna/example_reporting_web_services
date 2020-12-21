import requests
import re
from bs4 import BeautifulSoup
from requests import Response

from example_reporting_web_services.scraping.indicator.trend_indicator_detail import TrendIndicatorDetail
from example_reporting_web_services.scraping.indicator.trend_indicator import TrendIndicator


class ScrapeInvesting:
    """ scrape https://www.investing.com/indices/investing.com-btc-usd-technical """

    def __init__(self):
        """scrape technical indicator for Bitcoin vs USD """

    def scrape(self) -> TrendIndicator:
        """
        do scrape of Bitcoin vs USD indicators
        :return: trend object
        """
        content_investing = self._scrape_investing()
        trend_investing = self._parse_investing(content_investing)
        return trend_investing

    def _scrape_investing(self) -> str:
        """
        scrape investing.com of technical indicators for Bitcoin vs USD
        :return: str
        """
        url = "https://www.investing.com/instruments/Service/GetTechincalData"
        params = {"pairID": "1057391", "period": "86400", "viewType": "normal"}

        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Host": "www.investing.com",
                   "Origin": "https://www.investing.com",
                   "Referer": "https://www.investing.com/indices/investing.com-btc-usd-technical",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
                   "X-Requested-With": "XMLHttpRequest"}

        response = requests.post(url, data=params, headers=headers, timeout=30)

        if 200 != response.status_code:
            raise ValueError('Scrape of ' + url + ' status code != 200 :' + str(response.status_code))
        return response.text

    def _parse_investing(self, content: str) -> TrendIndicator:
        """
        Parse the scraping and create the Trend result
        :param content: result of scraping from _scrape method
        :return: Trend object
        """
        soup = BeautifulSoup(content, "html.parser")

        summary = soup.find(id="techStudiesInnerWrap").find(class_="uppercaseText").string
        trend = TrendIndicator(summary, from_site="investing.com",
                               from_url="https://www.investing.com/indices/investing.com-btc-usd-technical")

        for summary in soup.find(id="techStudiesInnerWrap").find_all(class_="summaryTableLine"):
            tech_trends = summary.find_all('span')
            trend_name = tech_trends[0].get_text().replace(":", "")
            trend_value = tech_trends[1].get_text()
            trend_buy = self._parse_string_to_int(tech_trends[2].get_text())
            trend_sell = self._parse_string_to_int(tech_trends[3].get_text())
            if 0 == (trend_buy + trend_sell):
                raise ValueError("no value in trend details")
            trend_detail = TrendIndicatorDetail(trend_name, trend_value, trend_buy, trend_sell)
            trend.details.append(trend_detail)

        return trend

    def _parse_string_to_int(self, s: str) -> int:
        """
        keep only numeric characters and convert to int
        :param s: string value to parse
        :return: 0 if s has no numeric character
        """
        return int(re.sub("[^0-9.]", "", "0" + s))
