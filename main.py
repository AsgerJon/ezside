"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from worktoy.keenum import auto, KeeNum
from worktoy.yolo import yolo

from ezside.app import App, MainWindow


def tester01() -> int:
  """Main Tester Script"""
  app = App(sys.argv)
  app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
  window = MainWindow()
  window.show()
  return app.exec()


class Cunt(KeeNum):
  FUCK = auto()
  YOU = auto()


def tester02() -> int:
  """CUNT"""
  lmao = {Cunt.FUCK: 69, Cunt.YOU: 420}
  for (key, val) in lmao.items():
    print("""%s: %s""" % (key, val))

  return 0


if __name__ == '__main__':
  yolo(tester02)
