# -*- coding:utf-8 -*-
from _lib import *
from interface.index import *

if __name__ == '__main__':
    App = QtWidgets.QApplication(argv)
    MainObject = MainWindow()
    MainObject.show()
    exit(App.exec())
