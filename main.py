"""Main Tester Script"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from icecream import ic

from ezside.app import MainWindow, App
from ezside.style import RGB
from tester_class_01 import Point


def tester00() -> None:
  """Main Tester Script"""
  stuff = [os, sys, ic, 'hello', 'world', MainWindow, ]
  [print(x) for x in stuff]


def tester01() -> None:
  """Main Tester Script"""
  app = App(MainWindow)
  sys.exit(app.exec())


def tester02() -> None:
  """Main Tester Script"""
  lime = RGB(144, 255, 0)
  print(lime)


if __name__ == '__main__':
  tester01()
