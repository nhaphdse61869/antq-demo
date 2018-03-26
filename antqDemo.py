#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from UI.MainUI import *
from UI.ContainerWindow import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = UIThread()
    # ex.showMaximized()
    ex = App()
    sys.exit(app.exec_())

