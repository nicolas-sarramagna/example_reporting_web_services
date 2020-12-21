import configparser
import io
from distutils.util import strtobool
from os import path

import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse, JSONResponse

from example_reporting_web_services.base_logger import logger
from example_reporting_web_services.scraping.chart.scrape_investtech import ScrapeInvesttech
from example_reporting_web_services.scraping.indicator.scrape_investing import ScrapeInvesting
from example_reporting_web_services.scraping.indicator.scrape_tradingview import ScrapeTradingView

app = FastAPI()


@app.exception_handler(Exception)
async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(exc, exc_info=True)
    return JSONResponse(str(exc), status_code=500)


@app.get('/api/v1/trend/indicator/investing')
def trend_indicator_from_investing():
    """
        scrape Bitcoin-USD technical indicators from https://www.investing.com/indices/investing.com-btc-usd-technical
    :return: TrendIndicator object in json format
    """
    scrape = ScrapeInvesting()
    trend = scrape.scrape()
    trend_json = trend.to_json()
    logger.debug(trend_json)
    return trend_json


@app.get('/api/v1/trend/indicator/tradingview')
async def trend_indicator_from_tradingview():
    """
        scrape Bitcoin-USD technical indicators from https://www.tradingview.com/symbols/BTCUSD/technicals/
    :return: TrendIndicator object in json format
    """
    scrape = ScrapeTradingView()
    trend = await scrape.scrape()
    trend_json = trend.to_json()
    logger.debug(trend_json)
    return trend_json


@app.get('/api/v1/trend/chart/investtech/graph')
def trend_chart_graph_from_investtech():
    """
        scrape Bitcoin-USD global chart from https://www.investtech.com/main/market.php?CompanyID=99400001&product=5
    :return: png image
    """
    scrape_charts = ScrapeInvesttech()
    b_img_graph = scrape_charts.scrape_graph()
    logger.debug('graph.png')
    return _send_img(b_img_graph, 'graph.png')


@app.get('/api/v1/trend/chart/investtech/rsi')
def trend_chart_rsi_from_investtech():
    """
        scrape Bitcoin-USD rsi chart from https://www.investtech.com/main/market.php?CompanyID=99400001&product=5
    :return: png image
    """
    scrape_charts = ScrapeInvesttech()
    b_img_rsi = scrape_charts.scrape_rsi()
    logger.debug('rsi.png')
    return _send_img(b_img_rsi, 'rsi.png')


def _send_img(binary_image: bytes, filename_png: str):
    """
    private method to send image
    :param binary_image: bytes content of the image
    :param filename_png: filename of the file
    :return:
    """
    response = StreamingResponse(io.BytesIO(binary_image), media_type="image/png")
    response.headers["Content-Disposition"] = "filename=" + filename_png
    return response


if __name__ == "__main__":
    # 0 . Load config file
    config = configparser.ConfigParser()
    config_file_path = path.join(path.dirname(path.abspath(__file__)), "config/config.cfg")
    config.read(config_file_path)

    server_host = config.get("AppSection", "server_host")
    server_port = int(config.get("AppSection", "server_port"))
    server_reload = bool(strtobool(config.get("AppSection", "server_reload")))
    server_debug = bool(strtobool(config.get("AppSection", "server_debug")))
    log_level = config.get("AppSection", "server_log_level")

    logger.info("Read config file DONE")

    uvicorn.run("app_ws:app", log_level=log_level, reload=server_reload, debug=server_debug,
                host=server_host, port=server_port)
