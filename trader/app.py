import sys, os.path
import pandas as pd
import numpy as np
from datetime import datetime

from .pyqt import *
from .mainwindow import MainWindow



def main():

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) # before app creation
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.init()
    app.exec()


if __name__ == '__main__':
    main()
