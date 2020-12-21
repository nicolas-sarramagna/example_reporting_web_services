import requests


class ScrapeInvesttech:
    """ scrape https://www.investtech.com/main/market.php?CompanyID=99400001&product=5 """

    def __init__(self):
        """scraping of two charts : global trend chart + rsi chart """

    def scrape_graph(self) -> bytes:
        """
        :return: response content of the trend chart
        """
        url_img_graph = "https://www.investtech.com/main/img.php?CompanyID=99400001&chartId=5&indicators=80,81,82,83,84,85,87,88,86&w=862&h=378"
        resp_img_graph = self._scrape_get_simple(url_img_graph)
        return resp_img_graph

    def scrape_rsi(self) -> bytes:
        """
        :return: response content of the rsi (relative strength index) chart
        """
        url_img_rsi = "https://www.investtech.com/main/img.php?CompanyID=99400001&chartId=5&type=rsi&w=862&h=78"
        resp_img_rsi = self._scrape_get_simple(url_img_rsi)
        return resp_img_rsi

    def _scrape_get_simple(self, url: str) -> bytes:
        """
        common function to scrape chart
        :param url: url of the image
        :return:response content
        """

        response = requests.get(url, timeout=30)

        if 200 != response.status_code:
            raise ValueError('Scrape of ' + url + ' status code != 200 :' + str(response.status_code))
        return response.content
