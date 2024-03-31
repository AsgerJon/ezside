"""Main Tester Script"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from icecream import ic
# import msgs.msg as msg

from ezside.windows import MainWindow, TestWindow

for item in sys.path:
  print(item)


def tester00() -> None:
  """Main Tester Script"""
  stuff = [os, sys, ic, 'hello', 'world', TestWindow, MainWindow, ]
  [print(x) for x in stuff]


def tester01() -> None:
  """Main Tester Script"""
  app = QApplication(sys.argv)
  app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())


def tester02() -> None:
  """Main Tester Script"""
  here = os.path.dirname(__file__)
  iconPath = os.path.join(here, 'windows', 'menus', 'icons', 'icons')
  iconList = []
  for icon in os.listdir(iconPath):
    iconList.append(icon)
  iconStrings = '\n'.join(iconList)
  iconFile = os.path.join(here, 'icons.txt')
  with open(iconFile, 'w') as f:
    f.write(iconStrings)


def tester03() -> None:
  """Main Tester Script"""
  here = os.path.dirname(__file__)
  iconPath = os.path.join(here, 'windows', 'menus', 'icons', 'icons')
  iconList = []
  for icon in os.listdir(iconPath):
    iconList.append(icon)
  iconStrings = '\n'.join(iconList)
  iconFile = os.path.join(here, 'icons.txt')
  with open(iconFile, 'w') as f:
    f.write(iconStrings)


if __name__ == '__main__':
  tester01()
