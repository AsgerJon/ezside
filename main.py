"""Main Tester Script"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys
import time
from typing import Callable

from PySide6.QtCore import Qt
from pyperclip import copy

from ezside.app.menus import FileMenu
from ezside.app import App
from ezside.core import AlignFlag, AlignLeft, SolidFill
from morevistutils import ModInt


def tester01() -> int:
  """Main Tester Script"""
  return App(_reset=True).exec()


def tester02() -> int:
  """Main Tester Script"""
  print(FileMenu)
  lmao = ModInt(5, 9)
  print(lmao)
  yolo = lmao + 1
  print(yolo)
  return 0


def tester03() -> int:
  """Main Tester Script"""
  for item in dir(int):
    print(item, type(getattr(int, item)).__name__)

  return 0


def tester05() -> int:
  """YOLO"""
  lmao = [
    'SolidFill', 'BlankFill', 'SolidLine', 'DashLine', 'DotLine', 'DashDot',
    'BlankLine', 'FlatCap', 'SquareCap', 'RoundCap', 'MiterJoin',
    'BevelJoin',
    'RoundJoin', 'SvgMiterJoin', 'Normal', 'Bold', 'DemiBold', 'WrapMode',
    'NoWrap', 'WordWrap', 'AlignFlag', 'AlignLeft', 'AlignRight',
    'AlignHCenter', 'AlignVCenter', 'AlignCenter', 'Center', 'AlignTop',
    'AlignBottom', 'Expand', 'Tight', 'Fixed', 'TimerType', 'Precise',
    'Coarse', 'VeryCoarse', 'SHIFT', 'CTRL', 'ALT', 'META', 'LeftClick',
    'RightClick', 'MiddleClick', 'NoClick', 'BackClick', 'ForwardClick',
    'VERTICAL', 'HORIZONTAL', 'alignDict', 'Prefer', 'Weight', 'Cap',
    'MixCase', 'SmallCaps', 'Upper', 'Lower']
  lines = []
  for item in lmao:
    lines.append("""'%s': %s,""" % (item, item))
  lol = '{\n%s\n}' % '\n'.join(lines)
  copy(lol)
  return 0


def tester06() -> int:
  """CUNT"""
  print(type(AlignFlag))
  print(type(AlignFlag).__bases__)
  print(type(SolidFill))
  print(type(Qt.BrushStyle))
  print(type(AlignLeft))
  print(isinstance(SolidFill, int))
  print(isinstance(AlignLeft, int))


def main(callMeMaybe: Callable) -> None:
  """Main Tester Script"""
  tic = time.time()
  print('Running python script located at: \n%s' % sys.argv[0])
  print('Started at: %s' % time.ctime())
  print(77 * '-')
  retCode = 0
  try:
    retCode = callMeMaybe()
  except Exception as exception:
    print('Exception: %s' % exception)
    raise exception
  retCode = 0 if retCode is None else retCode
  print(77 * '-')
  print('Return Code: %s' % retCode)
  print('Runtime: %.3f seconds' % (time.time() - tic))


if __name__ == '__main__':
  main(tester01)
