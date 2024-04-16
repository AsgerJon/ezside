"""Main Tester Script"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from icecream import ic
# import msgs.msg as msg

from ezside.app import MainWindow, App

for item in sys.path:
  print(item)


def tester00() -> None:
  """Main Tester Script"""
  stuff = [os, sys, ic, 'hello', 'world', MainWindow, ]
  [print(x) for x in stuff]


def tester01() -> None:
  """Main Tester Script"""
  app = App(MainWindow)
  # app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
  # window = MainWindow()
  # window.show()
  sys.exit(app.exec())


if __name__ == '__main__':
  tester01()
