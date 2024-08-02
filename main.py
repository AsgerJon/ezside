"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from worktoy.keenum import auto, KeeNum
from worktoy.yolo import yolo

from ezside.app import App
from main_tester_class02 import MainWindow


def tester01() -> int:
  """Main Tester Script"""
  app = App(sys.argv)
  app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
  window = MainWindow()
  window.show()
  return app.exec()


if __name__ == '__main__':
  yolo(tester01)
