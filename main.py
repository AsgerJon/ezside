"""Main Tester Script"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from icecream import ic

from ezside.app import MainWindow, App


def tester00() -> None:
  """Main Tester Script"""
  stuff = [os, sys, ic, 'hello', 'world', MainWindow, ]
  [print(x) for x in stuff]


def tester01() -> None:
  """Main Tester Script"""
  app = App(MainWindow)
  sys.exit(app.exec())


if __name__ == '__main__':
  tester01()
