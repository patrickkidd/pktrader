import sys, os.path
import pandas as pd
import numpy as np
from datetime import datetime

from .pyqt import *
from .mainwindow import MainWindow




def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.fileList.item(0).setSelected(True)
    app.exec()


if __name__ == '__main__':
    main()
