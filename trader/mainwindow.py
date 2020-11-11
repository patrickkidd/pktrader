
import pandas
from .pyqt import *
from .debug import *
from .strategy import SMAStrategy
from .canvas import MplCanvas, MplNavigationToolbar
from .stock import Stock


class MainWindow(QMainWindow, Debug):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._filePath = None

        self._strategy = SMAStrategy(self)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.setStrategy(self._strategy)
        toolbar = MplNavigationToolbar(self.canvas, self)
        PltLayout = QVBoxLayout()
        PltLayout.addWidget(self._strategy)
        PltLayout.addWidget(self.canvas)
        PltLayout.addWidget(toolbar)

        self.dataDir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        self.fileList = QListWidget(self)
        self.fileList.setFixedWidth(300)
        for fileInfo in QDir(self.dataDir).entryInfoList():
            fileName = fileInfo.fileName()
            if fileName[0] == '.':
                continue
            self.fileList.addItem(fileName)
        self.fileList.itemSelectionChanged.connect(self.onFileItemSelectionChanged)

        centralWidget = QWidget(self)
        Layout = QHBoxLayout(centralWidget)
        Layout.addLayout(PltLayout)
        Layout.addWidget(self.fileList)

        self.setCentralWidget(centralWidget)
        self.resize(1250, 800)

    def openFile(self, filePath):
        self._filePath = filePath
        self._fileName = QFileInfo(filePath).fileName()
        stockValues = pandas.read_csv(filePath)
        self.canvas.setFileData(stockValues)

    def onFileItemSelectionChanged(self):
        item = self.fileList.selectedItems()[0]
        fileName = item.text()
        filePath = os.path.join(self.dataDir, fileName)
        self.openFile(filePath)

        


