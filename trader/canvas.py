
import pandas as pd
import numpy as np
from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as MplNavigationToolbar
from matplotlib.figure import Figure

from .stock import Stock


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self._strategy = None
        self._trades = None
        self._stockValues = None

    def setFileData(self, stockValues):
        self._stockValues = stockValues
        self.updatePlot()

    def setStrategy(self, strategy):
        if self._strategy:
            self._strategy.changed.disconnect(self.updatePlot)
        self._strategy = strategy
        self._strategy.changed.connect(self.updatePlot)
        self.updatePlot()

    def updatePlot(self):
        self.axes.cla()

        if self._stockValues is None or self._strategy is None:
            return

        stock = Stock()

        result = self._strategy.run(self._stockValues, stock)
        self.axes.cla()

        N = len(self._stockValues)
        X_STEP = N / 7

        handles = []
        labels = []

        self.axes.set_xticks(np.arange(0, N, step=X_STEP))
        handle = self.axes.plot(
            self._stockValues['Date'],
            self._stockValues['Adj Close'],
            label='Date', alpha=.3
        )
        handles.append(handle[0])
        labels.append('Date')

        for axis in result['axes']:
            if axis.get('type', 'line') == 'line':
                label = axis.get('label', None)
                handle = self.axes.plot(
                    axis['data'],
                    label=label,
                    alpha=axis.get('alpha', .4)
                )[0]
                handles.append(handle)
                labels.append(label)

        self.axes.scatter(self._stockValues.index, result['buys'], label='Buy', marker='^', color='green')
        self.axes.scatter(self._stockValues.index, result['sells'], label='Sell', marker='v', color='red')
        self.axes.set_title('Strategy: %s' % self._strategy.NAME)
        self.axes.set_xlabel('%s - %s' % (self._stockValues['Date'][0], self._stockValues['Date'][N-1]))
        self.axes.set_ylabel('Price (USD)')
        self.axes.legend(
            loc='upper left',
            handles=handles,
        )

        self.axes.text(X_STEP * 6, 0, 'Balance: $%s' % stock.balance(), fontsize=12)
        self.draw()

