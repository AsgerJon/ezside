"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from worktoy.keenum import auto, KeeNum
from worktoy.yolo import yolo

from ezside.app import App, MainWindow
from main_tester_class01 import ComplexNumber


def tester01() -> int:
  """Main Tester Script"""
  app = App(sys.argv)
  app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
  window = MainWindow()
  window.show()
  return app.exec()


def tester02() -> int:
  """Testing AttriClass/AttriBox issue"""

  z = ComplexNumber()
  print(z)
  print(z.realPart)
  print(type(z.realPart))


if __name__ == '__main__':
  yolo(tester02)
