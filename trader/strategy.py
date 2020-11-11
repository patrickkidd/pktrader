import numpy
from .pyqt import *
from .debug import Debug



# DataFrame.plot(
#     x=None, y=None, kind='line', ax=None, subplots=False,
#     sharex=None, sharey=False, layout=None, figsize=None,
#     use_index=True, title=None, grid=None, legend=True, style=None,
#     logx=False, logy=False, loglog=False, xticks=None, yticks=None,
#     xlim=None, ylim=None, rot=None, fontsize=None, colormap=None,
#     table=False, yerr=None, xerr=None, secondary_y=False, 
#     sort_columns=False, **kwargs
# )


class Strategy(QWidget, Debug):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(45)

    def run(self, stockValues, stock):
        pass


class SMAStrategy(Strategy):

    changed = pyqtSignal()

    NAME = 'Simple Moving Average'

    def __init__(self, parent=None):
        super().__init__(parent)

        self._shortWindow = 30
        self._longWindow = 100

        Layout = QHBoxLayout()
        self.shortLabel = QLabel('Short Window:', self)
        self.shortLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.shortEdit = QLineEdit(self)
        self.shortEdit.setText(str(self._shortWindow))
        self.shortEdit.setInputMask('000')
        self.shortEdit.setMaxLength(3)
        self.shortEdit.setMaximumWidth(35)
        self.shortEdit.editingFinished.connect(self.onShortWindowChanged)
        self.longLabel = QLabel('Long Window:', self)
        self.longLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.longEdit = QLineEdit(self)
        self.longEdit.setText(str(self._longWindow))
        self.longEdit.setInputMask('000')
        self.longEdit.setMaxLength(3)
        self.longEdit.setMaximumWidth(35)
        self.longEdit.editingFinished.connect(self.onLongWindowChanged)
        Layout.addWidget(self.shortLabel)
        Layout.addWidget(self.shortEdit)
        Layout.addWidget(self.longLabel)
        Layout.addWidget(self.longEdit)
        Layout.addSpacing(10)
        self.setLayout(Layout)

    def run(self, _stockValues, stock):
        stockValues = _stockValues['Adj Close']

        buys = []
        sells = []
        flag = -1

        shortValues = stockValues.rolling(window=self._shortWindow).mean()
        longValues = stockValues.rolling(window=self._longWindow).mean()

        for i in range(len(stockValues)):
            if shortValues[i] > longValues[i]:
                if flag != 1:
                    buys.append(stockValues[i])
                    sells.append(numpy.nan)
                    flag = 1
                    stock.buy(stockValues[i])
                else:
                    buys.append(numpy.nan)
                    sells.append(numpy.nan)
            elif shortValues[i] < longValues[i]:
                if flag != 0:
                    buys.append(numpy.nan)
                    sells.append(stockValues[i])
                    flag = 0
                    stock.sell(stockValues[i])
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

