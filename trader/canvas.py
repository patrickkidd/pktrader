
import pandas as pd
import numpy as np
from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as MplNavigationToolbar
from matplotlib.figure import Figure

from .debug import Debug
from .stock import Stock


class MplCanvas(FigureCanvasQTAgg, Debug):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self._strategy = None
        self._trades = None
        self._stockValues = None

    def setStrategy(self, strategy):
        if self._strategy:
            self._strategy.changed.disconnect(self.updatePlot)
        self._strategy = strategy
        self._strategy.changed.connect(self.run)

    def run(self, stockValues=None):
        if stockValues is None:
            return
        self.axes.cla()

        self._stockValues = stockValues

        if self._stockValues is None or len(self._stockValues) == 0 or self._strategy is None:
            return

        stock = Stock()

        result = self._strategy.run(self._stockValues, stock)
        self.axes.cla()

        N = len(self._stockValues)
        X_STEP = N / 7

        handles = []

        self.axes.set_xticks(np.arange(0, N, step=X_STEP))
        handle = self.axes.plot(
            self._stockValues['Date'],
            self._stockValues['Adj Close'],
            label='Adj Close', alpha=.3
        )
        handles.append(handle[0])

        for axis in result['axes']:
            if axis.get('type', 'line') == 'line':
                label = axis.get('label', None)
                handle = self.axes.plot(
                    axis['data'],
                    label=label,
                    alpha=axis.get('alpha', .4)
                )[0]
                handles.append(handle)

        self.axes.scatter(self._stockValues.index, result['buys'], label='Buy', marker='^', color='green')
        self.axes.scatter(self._stockValues.index, result['sells'], label='Sell', marker='v', color='red')
        self.axes.set_title('Strategy: %s' % self._strategy.NAME)
        # self.axes.set_xlabel('%s - %s' % (self._stockValues['Date'][0], self._stockValues['Date'][N-1]))
        self.axes.set_ylabel('Price (USD)')
        self.axes.legend(
            loc='upper left',
            handles=handles,
        )
        self.draw()

        return stock

