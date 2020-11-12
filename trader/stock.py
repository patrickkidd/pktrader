from .debug import Debug


class Stock(Debug):

    def __init__(self):
        self._gain = 0
        self._first_buy = None
        self._last_buy = None
        self._last_sell = None
        self._trades = []

    def buy(self, date, price):
        # self.here("BUY  @ $%s" % round(price, 2))
        self._trades.append(('BUY', date, round(price, 2), self.gain()))
        self._last_buy = price
        if self._first_buy is None:
            self._first_buy = price
        if self._last_buy is None:
            self._gain = 0

    def sell(self, date, price):
        if self._last_buy is not None:
            self._gain += round(price - self._last_buy, 2)
            self._last_sell = price
            self._trades.append(('SELL', date, round(price, 2), self.gain()))

    def first_buy(self):
        return round(self._first_buy, 2)

    def last_sell(self):
        return round(self._last_sell, 2)

    def bah_gain(self):
        return round(self._last_sell - self._first_buy, 2)

    def bah_percent_return(self):
        if self._last_sell is not None:
            return int((self._last_sell / self._first_buy) * 100) - 100

    def gain(self):
        return round(self._gain, 2)

    def percent_return(self):
        if self._last_sell is not None:
            ret = self._gain / self._first_buy
            return int(ret * 100)

    def logString(self):
        s = ''
        for trade in self._trades:
            if s:
                s += '\n'            
            s += "%s\t%s  $%0.2f\tBalance: $%0.2f" % trade
        return s

