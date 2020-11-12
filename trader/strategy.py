import numpy
from .pyqt import *
from .debug import Debug


class Strategy(QGroupBox, Debug):

    NAME = 'NULL Strategy'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.NAME)
        self.setFixedHeight(65)

    def run(self, stockValues, stock):
        pass


class SMAStrategy(Strategy):

    changed = pyqtSignal()

    NAME = 'Simple Moving Average'

    def __init__(self, parent=None):
        super().__init__(parent)

        self._shortWindow = 30
        self._longWindow = 100

        self.shortLabel = QLabel('Short Window:', self)

        self.shortEdit = QLineEdit(self)
        self.shortEdit.setText(str(self._shortWindow))
        self.shortEdit.setInputMask('000')
        self.shortEdit.setMaxLength(3)
        self.shortEdit.setMaximumWidth(45)
        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.shortEdit.setSizePolicy(policy)
        self.shortEdit.editingFinished.connect(self.onShortWindowChanged)

        self.longLabel = QLabel('Long Window:', self)

        self.longEdit = QLineEdit(self)
        self.longEdit.setText(str(self._longWindow))
        self.longEdit.setInputMask('000')
        self.longEdit.setMaxLength(3)
        self.longEdit.setMaximumWidth(45)
        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        policy.setHeightForWidth(self.longEdit.sizePolicy().hasHeightForWidth())
        self.longEdit.setSizePolicy(policy)
        self.longEdit.editingFinished.connect(self.onLongWindowChanged)

        Layout = QHBoxLayout()
        Layout.addWidget(self.shortLabel)
        Layout.addWidget(self.shortEdit)
        Layout.addWidget(self.longLabel)
        Layout.addWidget(self.longEdit)
        Layout.addStretch(10)
        self.setLayout(Layout)

    def run(self, _stockValues, stock):
        stockValues = _stockValues['Adj Close']

        buys = []
        sells = []
        holding = False

        shortValues = stockValues.rolling(window=self._shortWindow).mean()
        longValues = stockValues.rolling(window=self._longWindow).mean()

        for i in range(len(stockValues)):
            if shortValues[i] > longValues[i]:
                if not holding:
                    buys.append(stockValues[i])
                    sells.append(numpy.nan)
                    holding = True
                    stock.buy(_stockValues['Date'][i], stockValues[i])
                else:
                    buys.append(numpy.nan)
                    sells.append(numpy.nan)
            elif shortValues[i] < longValues[i]:
                if holding:
                    buys.append(numpy.nan)
                    sells.append(stockValues[i])
                    holding = False
                    stock.sell(_stockValues['Date'][i], stockValues[i])
                else:
                    buys.append(numpy.nan)
                    sells.append(numpy.nan)
            else:
                buys.append(numpy.nan)
                sells.append(numpy.nan)

        return {
            'axes': (
                {
                    'data': shortValues,
                    'type': 'line',
                    'label': '%i Day Window' % self._shortWindow
                },
                {
                    'data': longValues,
                    'type': 'line',
                    'label': '%i Day Window' % self._longWindow
                }
            ),
            'buys': buys,
            'sells': sells
        }

    def onShortWindowChanged(self):
        x = int(self.shortEdit.text())
        if x != self._shortWindow:
            self._shortWindow = x
            self.changed.emit()

    def onLongWindowChanged(self):
        x = int(self.longEdit.text())
        if x != self._longWindow:
            self._longWindow = x
            self.changed.emit()

