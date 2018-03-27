#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from UI.MainUI import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UIThread()
    ex.showMaximized()
    sys.exit(app.exec_())
