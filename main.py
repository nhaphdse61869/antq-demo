#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ui.app import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = UIThread()
    # ex.showMaximized()
    ex = App()
    sys.exit(app.exec_())
