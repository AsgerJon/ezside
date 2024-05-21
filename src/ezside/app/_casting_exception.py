"""CastingException provides a custom exception class to be raised when a
failed attempt at casting a string to a given type. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class CastingException(Exception):
  """CastingException provides a custom exception class to be raised when a
  failed attempt at casting a string to a given type. """

  def __init__(self, exc: Exception, cls: type, value: str) -> None:
    e = """When attempting to cast the string: '%s' to an instance of 
    type: '%s', the following error occurred: '%s'!"""
    Exception.__init__(self, e % (value, cls, str(exc)))
