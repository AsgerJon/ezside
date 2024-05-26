"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys
import os
import time
from typing import Callable

from icecream import ic

from ezside.windows import MainWindow, App

ic.configureOutput(includeContext=True, )


def tester00() -> int:
  """Main Tester Script"""
  stuff = [os, sys, ic, 'hello world']
  return 0


def tester01() -> int:
  """Main Tester Script"""
  return App(MainWindow, 'EZ', 'EZSide!').exec()


def main(callMeMaybe: Callable) -> None:
  """Main Tester Script"""
  tic = time.perf_counter_ns()
  print('Running python script located at: \n%s' % sys.argv[0])
  print('Started at: %s' % time.ctime())
  print(77 * '-')
  retCode = 0
  try:
    retCode = callMeMaybe()
  except BaseException as exception:
    print('Exception: %s' % exception)
    retCode = -1
    raise exception
  retCode = 0 if retCode is None else retCode
  print(77 * '-')
  print('Return Code: %s' % retCode)
  toc = time.perf_counter_ns() - tic
  print('Runtime: %.3E seconds' % (toc * 1e-09,))


if __name__ == '__main__':
  main(tester01)
