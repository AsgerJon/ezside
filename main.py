"""Main Tester Script"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from PySide6.QtWidgets import QMainWindow, QApplication
from icecream import ic


def tester00() -> None:
  """Main Tester Script"""
  stuff = [os, sys, ic, 'hello', 'world']
  [print(x) for x in stuff]


def tester01() -> None:
  """Main Tester Script"""
  app = QApplication(sys.argv)
  window = QMainWindow()
  window.show()
  app.exec()


if __name__ == '__main__':
  tester00()
