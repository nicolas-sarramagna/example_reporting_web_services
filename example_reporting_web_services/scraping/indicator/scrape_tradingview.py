from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession

from example_reporting_web_services.scraping.indicator.trend_indicator import TrendIndicator
from example_reporting_web_services.scraping.indicator.trend_indicator_detail import TrendIndicatorDetail


class ScrapeTradingView:
    """
        scrape https://www.tradingview.com/symbols/BTCUSD/technicals/
    """

    def __init__(self):
        """scrape technical indicator for Bitcoin vs USD """

    async def scrape(self) -> TrendIndicator:
        """
        do scrape of Bitcoin vs USD indicators
        :return: trend object
        """
        content_tradingview = await self._scrape_tradingview()
        trend_tradingview = self._parse_tradingview(content_tradingview)
        return trend_tradingview

    async def _scrape_tradingview(self) -> str:
        """
        scrape investing.com of technical indicators for Bitcoin vs USD
        use asynchronous api because of async calls of javascript in the tradingview.com page
        :return: content
        """
        url = "https://www.tradingview.com/symbols/BTCUSD/technicals"

        response = await AsyncHTMLSession().get(url)
        await response.html.arender(timeout=30)

        if 200 != response.status_code:
            raise ValueError('Scrape of ' + url + ' status code != 200 :' + str(response.status_code))
        return response.html.raw_html

    def _parse_tradingview(self, content: str) -> TrendIndicator:
        """
        Parse the scraping and create the Trend result
        :param content: result of scraping from _scrape method
        :return: Trend object
        """
        soup = BeautifulSoup(content, "html.parser")

        trends = []

        # same html level for summary and the details -> need to check by value
        for element in soup.select('div[class*=speedometerWrapper]'):

            # by name, summary is in
            for trend in element.select('[class*=speedometerTitle]'):
                trend_name = trend.get_text()
                trend_value = element.select_one('[class*=speedometerSignal]').get_text()
                trend_sell, trend_neutral, trend_buy = 0, 0, 0

                # get sell, neutral and buy number, summary too but not used
                for trend_number in element.select('span[class*=counterNumber]'):

                    all_class = ''.join(trend_number.attrs['class'])
                    number = int(trend_number.get_text())

                    if 'sellColor' in all_class:
                        trend_sell = number
                    elif 'neutralColor' in all_class:
                        trend_neutral = number
                    elif 'buyColor' in all_class:
                        trend_buy = number
                    else:
                        raise ValueError('no match found in -' + all_class + '-')

                # check trend values
                self._check_trend_values(trend_name.lower(), trend_sell, trend_neutral, trend_buy)

                trend_detail = TrendIndicatorDetail(trend_name, trend_value, trend_buy, trend_sell, trend_neutral)
                trends.append(trend_detail)

        # get summary index for summary value
        index = self._find_index_summary(trends)

        summary = trends[index].trend_value
        from_url = "https://www.tradingview.com/symbols/BTCUSD/technicals"
        trend = TrendIndicator(summary, from_site="tradingview.com", from_url=from_url)
        # remove summary detail from trends
        trends.pop(index)
        # add the other details
        trend.details.extend(trends)

        return trend

    def _find_index_summary(self, trends: [TrendIndicatorDetail]) -> int:
        """
            find summary index from trends, raise ValueError if trend with name 'summary' not found
        :param trends:  all trends build from the html content, summary is in
        :return: index of summary in trends list
        """
        index = 0
        while index < len(trends):
            if trends[index].trend_name.lower() == 'summary':
                break
            index += 1

        if index >= len(trends):
            raise ValueError('trend summary not found in trends')

        return index

    def _check_trend_values(self, trend_name: str, trend_sell: int, trend_neutral: int, trend_buy: int) -> None:
        """
        Check if sum of trend values are equal of 11 for trend_name 'oscillators' and 17 for 'moving averages'
        :param trend_name: check for 'oscillators' and 'moving averages'
        :param trend_sell: number of indicators sell
        :param trend_neutral: number of indicators neutral
        :param trend_buy: number of indicators buy
        :return: raise ValueError if check is False
        """
        trend_name_l = trend_name.lower()
        sum_trend_values = trend_sell + trend_neutral + trend_buy
        if trend_name_l == 'oscillators' and 11 != sum_trend_values:
            raise ValueError('missing trend indicators for oscillators,' +
                             ' must sum of trend values == 11 and not : ' + str(sum_trend_values))
        elif trend_name_l == 'moving averages' and 17 != sum_trend_values:
            raise ValueError('missing trend indicators for moving averages,' +
                             ' must sum of trend values == 17 and not : ' + str(sum_trend_values))
