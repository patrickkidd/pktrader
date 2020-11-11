from .debug import Debug


class Stock(Debug):

    def __init__(self):
        self._balance = 0
        self._last_buy = None

    def buy(self, price):
        # self.here("BUY  @ $%s" % round(price, 2))
        self._last_buy = price
        if self._last_buy is None:
            self._balance = 0

    def sell(self, price):
        if self._last_buy is not None:
            self._balance += round(price - self._last_buy, 2)
            # self.here("SELL @ $%s, Balance: $%s" % (round(price, 2), self._balance))

    def balance(self):
        return round(self._balance, 2)

