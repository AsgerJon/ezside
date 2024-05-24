"""The 'parseFilter' function parses name filter from positional and keyword
arguments for use in file dialogs."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


def _parseKwargs(*args, **kwargs) -> str:
  """The '_parseKwargs' function parses name filter from keyword
  arguments."""
  filterKeys = ['filter', 'filters', 'nameFilter', 'nameFilters']
  for key in filterKeys:
    if key in kwargs:
      val = kwargs[key]
      if isinstance(val, str):
        return val


def _parseArgs(*args, **kwargs) -> str:
  """The '_parseArgs' function parses name filter from positional
  arguments."""
  for arg in args:
    if isinstance(arg, str):
      return arg


def parseFilter(*args, **kwargs) -> str:
  """The 'parseFilter' function parses name filter from positional and
  keyword arguments for use in file dialogs."""
  parsers = [_parseKwargs, _parseArgs]
  for parser in parsers:
    nameFilter = parser(*args, **kwargs)
    if nameFilter:
      return nameFilter
