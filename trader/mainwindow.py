import pandas
import yfinance
from .pyqt import *
from .debug import *
from .strategy import SMAStrategy
from .canvas import MplCanvas, MplNavigationToolbar



class MainWindow(QMainWindow, Debug):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._filePath = None
        self._apiData = {
            'symbol': 'AAPL',
            'dateStart': QDate.currentDate().addDays(-365 * 4),
            'dateEnd': QDate.currentDate().addDays(-1),
        }

        w = QWidget()

        self.mainToolBar = QGroupBox('Data Source', self)
        self.mainToolBar.setFixedHeight(65)

        self.symbolLabel = QLabel('Symbol:')
        self.symbolEdit = QLineEdit(self._apiData['symbol'], self.mainToolBar)
        self.symbolEdit.setFixedWidth(75)
        self.symbolEdit.editingFinished.connect(self.onSymbol)
        self.dateStartLabel = QLabel('Start Date:')
        self.dateStartEdit = QDateEdit(self._apiData['dateStart'], self.mainToolBar)
        self.dateStartEdit.setDisplayFormat('yyyy-MM-dd')
        self.dateStartEdit.editingFinished.connect(self.onDateStart)
        self.dateEndLabel = QLabel('End Date:')
        self.dateEndEdit = QDateEdit(self._apiData['dateEnd'], self.mainToolBar)
        self.dateEndEdit.setDisplayFormat('yyyy-MM-dd')
        self.dateEndEdit.editingFinished.connect(self.onDateEnd)
        MainToolBarLayout = QHBoxLayout()
        MainToolBarLayout.addWidget(self.symbolLabel)
        MainToolBarLayout.addWidget(self.symbolEdit)
        MainToolBarLayout.addWidget(self.dateStartLabel)
        MainToolBarLayout.addWidget(self.dateStartEdit)
        MainToolBarLayout.addWidget(self.dateEndLabel)
        MainToolBarLayout.addWidget(self.dateEndEdit)
        MainToolBarLayout.addStretch(10)
        self.mainToolBar.setLayout(MainToolBarLayout)

        self._strategy = SMAStrategy(w)
        self._strategy.changed.connect(self.onStrategyChanged)
        self.canvas = MplCanvas(w, width=5, height=4, dpi=100)
        self.canvas.setStrategy(self._strategy)
        toolbar = MplNavigationToolbar(self.canvas, w)
        #
        LeftLayout = QVBoxLayout()
        LeftLayout.addWidget(self.mainToolBar)
        LeftLayout.addWidget(self._strategy)
        LeftLayout.addWidget(self.canvas)
        LeftLayout.addWidget(toolbar)
        LeftLayout.setSpacing(22)

        self.dataDir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        self.fileList = QListWidget(self)
        self.fileList.setFont(QFont('Courier'))
        self.fileList.setSortingEnabled(True)
        self.fileList.setFixedWidth(380)
        self.fileList.itemSelectionChanged.connect(self.onFileItemSelectionChanged)
        self.resultText = QTextEdit(self)
        self.resultText.setFont(QFont('Courier'))
        self.resultText.setLineWrapMode(QTextEdit.NoWrap)
        self.resultText.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        #
        RightLayout = QVBoxLayout()
        RightLayout.addWidget(self.fileList)
        RightLayout.addWidget(self.resultText)

        Layout = QHBoxLayout(w)
        Layout.addLayout(LeftLayout)
        Layout.addLayout(RightLayout)

        self.setCentralWidget(w)

        # Load Cache
        appDataDir = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
        cacheDataDir = self._cacheDataDir()
        if not os.path.isdir(cacheDataDir):
            QDir(appDataDir).mkpath(cacheDataDir)
        # self._fsWatcher = QFileSystemWatcher(self)
        # self._fsWatcher.addPath(cacheDataDir)
        # self._fsWatcher.directoryChanged.connect(self.onCacheDirChanged)

    def init(self):
        self._updateFileList()
        self.updateSearch()
        self.resize(1250, 800)

    def _cacheDataDir(self):
        appDataDir = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
        cacheDataDir = os.path.join(appDataDir, 'cache')
        return cacheDataDir

    def _updateFileList(self):
        self.fileList.clear()
        cacheDataDir = self._cacheDataDir()
        for fileInfo in QDir(cacheDataDir).entryInfoList():
            fileName = fileInfo.fileName()
            if fileName[0] == '.':
                continue
            filePath = fileInfo.absoluteFilePath()
            item = QListWidgetItem(fileName)
            item._filePath = filePath
            self.fileList.addItem(fileName)
            if self._filePath == item._filePath:
                item.setSelected(True)

    # def onCacheDirChanged(self):
    #     self.here()
    #     self._updateFileList()

    def updateSearch(self):
        cacheEntryPath = self._tickerCachePath(**self._apiData)
        # Load data
        if not os.path.isfile(cacheEntryPath):
            self.here("Downloading: %s, %s - %s" % (
                self._apiData['symbol'],
                self._apiData['dateStart'].toString('yyyy-MM-dd'),
                self._apiData['dateEnd'].toString('yyyy-MM-dd')
            ))
            stockPrices = yfinance.download(
                self._apiData['symbol'],
                start=self._apiData['dateStart'].toString('yyyy-MM-dd'),
                end=self._apiData['dateEnd'].toString('yyyy-MM-dd')
            )
            if len(stockPrices) > 0:
                # self.here('Caching: %s' % cacheEntryPath)
                stockPrices.to_csv(cacheEntryPath)
        self._updateFileList()
        # 'Date' column doesn't exist unless read from CSV for some reason
        if os.path.isfile(cacheEntryPath):
            # self.here('Reading: %s' % cacheEntryPath)
            self.runFile(cacheEntryPath)

    def _tickerCachePath(self, symbol, dateStart, dateEnd):
        fileName = "%s-%s-to-%s.csv" % (
            self._apiData['symbol'],
            self._apiData['dateStart'].toString('yyyy-MM-dd'),
            self._apiData['dateEnd'].toString('yyyy-MM-dd'),
        )
        filePath = os.path.join(self._cacheDataDir(), fileName)
        return filePath

    def onSymbol(self):
        symbol = self.symbolEdit.text()
        if symbol != self._apiData['symbol']:
            self._apiData['symbol'] = symbol.upper()
            if symbol.upper() != symbol:
                self.symbolEdit.setText(symbol.upper())
            self.updateSearch()

    def onDateStart(self):
        dateStart = self.dateStartEdit.date()
        if dateStart != self._apiData['dateStart']:
            self._apiData['dateStart'] = dateStart
            self.updateSearch()

    def onDateEnd(self):
        dateEnd = self.dateEndEdit.date()
        if dateEnd != self._apiData['dateEnd']:
            self._apiData['dateEnd'] = dateEnd
            self.updateSearch()

    def runFile(self, filePath):
        self._filePath = filePath
        stockValues = pandas.read_csv(filePath)
        stock = self.canvas.run(stockValues)

        result = """Strategy:\tBuy & Hold
Gain:\t%s%% ($%0.2f/share)

------------------------------------------

Strategy:\t%s
Gain:\t%s%% ($%0.2f/share)

%s
        """ % (
            stock.bah_percent_return(),
            stock.bah_gain(),
            self._strategy.NAME,
            stock.percent_return(),
            stock.gain(),
            stock.logString(),            
        )
        self.resultText.setText(result)
        
        # update file list
        cacheDataDir = self._cacheDataDir()
        for row in range(self.fileList.count()):
            item = self.fileList.item(row)
            itemFilePath = os.path.join(cacheDataDir, item.text())
            if itemFilePath == self._filePath and not item.isSelected():
                item.setSelected(True)
                break
        fileName = QFileInfo(filePath).fileName()
        self.setWindowTitle(fileName)

    def onFileItemSelectionChanged(self):
        items = self.fileList.selectedItems()
        if items:
            fileName = items[0].text()
            filePath = os.path.join(self._cacheDataDir(), fileName)
            if filePath != self._filePath:
                self.runFile(filePath)

    def onStrategyChanged(self):
        self.runFile(self._filePath)

        


