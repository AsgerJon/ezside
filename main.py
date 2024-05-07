"""Main Tester Script"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from random import randint
import sys
import time
from types import FunctionType
from typing import Callable

from icecream import ic
from vistutils.text import stringList

from ezside.app import MainWindow, App
from ezside.app.menus import MainMenuBar
from morevistutils.casenames import Name, \
  CamelCase, \
  SnakeCase, \
  TitleCase, \
  SmartMap
from morevistutils.casenames import PascalCase, SentenceCase
from tester_class_02 import SomeClass, AnotherClass

lmaoPrint = print


def yolo(*items) -> str:
  for item in items:
    if isinstance(item, type):
      lmaoPrint(item.__qualname__)
    elif isinstance(item, FunctionType):
      lmaoPrint(item.__name__)
    else:
      lmaoPrint(item, end=' ')
  lmaoPrint()


print = yolo


def tester00() -> None:
  """Main Tester Script"""
  stuff = [os, sys, ic, 'hello', 'world', MainWindow, ]
  [print(x) for x in stuff]


def tester01() -> int:
  """Main Tester Script"""
  return App().exec()


def tester02() -> None:
  """Main Tester Script"""


def tester03() -> None:
  """Main Tester Script"""
  someObj = SomeClass()
  anotherObj = AnotherClass()
  print(anotherObj.urMom)
  print(object.__getattribute__(anotherObj, 'urMom'))


def tester04() -> None:
  """LMAO"""

  red, green, blue = 144, 255, 0
  colNum = red * 2 ** 16 + green * 2 ** 8 + blue

  print(colNum)


def tester05() -> None:
  """YOLO"""
  name = Name()
  print(name)
  for word in stringList("""top, left, corner"""):
    name.append(word)
  print(name)
  print(name @ CamelCase)
  print(name @ SnakeCase)

  print(77 * '-')
  name = Name(CamelCase)
  print(name)
  for word in stringList("""top, left, corner"""):
    name.append(word)
  print(name)
  for NameCase in [SnakeCase, PascalCase, TitleCase, SentenceCase]:
    print(NameCase)
    print(name @ NameCase)


def tester06() -> None:
  """YOLO"""
  lmao = SmartMap()
  yolo = {**globals()}
  for (key, val) in yolo.items():
    if isinstance(val, dict):
      lmao[key] = SmartMap(**val)
    else:
      lmao[key] = val

  for (key, val) in lmao.items():
    print(key, val)


F = lambda x: F(str(sum([int(c) for c in str(x)]))) if int(x) > 9 else int(x)


def tester07() -> None:
  """LMAO"""


def main(callMeMaybe: Callable) -> None:
  """Main Tester Script"""
  tic = time.time()
  print('Running python script located at: \n%s' % sys.argv[0])
  print('Started at: %s' % time.ctime())
  print(77 * '-')
  retCode = callMeMaybe()
  print(77 * '-')
  print('Return Code: %s' % retCode)
  print('Runtime: %.3f seconds' % (time.time() - tic))


if __name__ == '__main__':
  main(tester01)
