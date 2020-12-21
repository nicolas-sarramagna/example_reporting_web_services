import asyncio

from example_reporting_web_services.scraping.chart.scrape_investtech import ScrapeInvesttech
from example_reporting_web_services.scraping.indicator.scrape_investing import ScrapeInvesting
from example_reporting_web_services.scraping.indicator.scrape_tradingview import ScrapeTradingView

if __name__ == '__main__':

    scrape = ScrapeTradingView()
    loop = asyncio.get_event_loop()
    trend = loop.run_until_complete(scrape.scrape())
    print("TradingView")
    print(trend.summary)
    for detail in trend.details:
        print(detail)

    scrape = ScrapeInvesting()
    trend = scrape.scrape()
    print("Investing")
    print(trend.summary)
    for detail in trend.details:
        print(detail)

    scrape_charts = ScrapeInvesttech()
    b_img_graph = scrape_charts.scrape_graph()
    b_img_rsi = scrape_charts.scrape_rsi()
