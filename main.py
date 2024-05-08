"""Main Tester Script"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.app import App


def tester01() -> int:
  """Main Tester Script"""
  return App().exec()


if __name__ == '__main__':
  tester01()
