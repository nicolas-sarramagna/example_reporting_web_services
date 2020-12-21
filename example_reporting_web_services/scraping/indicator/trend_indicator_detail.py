class TrendIndicatorDetail:
    """
        Technical indicator trend with details
    """

    def __init__(self, trend_name: str, trend_value: str, trend_buy: int = 0, trend_sell: int = 0,
                 trend_neutral: int = 0):
        """

        :param trend_name:
        :param trend_value:
        :param trend_buy:
        :param trend_sell:
        :param trend_neutral:
        """
        self.trend_name = trend_name
        self.trend_value = trend_value
        self.trend_buy = trend_buy
        self.trend_sell = trend_sell
        self.trend_neutral = trend_neutral

    def __str__(self):
        return self.trend_name + ' ' + self.trend_value + ' sell(' + str(self.trend_sell) + \
               ') neutral (' + str(self.trend_neutral) + ') buy (' + str(self.trend_buy) + ')'
