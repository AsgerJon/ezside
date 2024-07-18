"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.yolo import yolo

from ezside.app import App, MainWindow


def tester01() -> int:
  """Main Tester Script"""
  return App(MainWindow, ).exec()


if __name__ == '__main__':
  yolo(tester01)
