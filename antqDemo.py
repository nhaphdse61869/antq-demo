#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from UI.MainUI import UIThread

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UIThread()
    sys.exit(app.exec_())
