"""The MissingSettingsError class is raised when the 'AppSettings' class
fails to recognize a settings key. Please note that the QSettings class
does not raise any such error, simply returning None. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class MissingSettingsError(Exception):
  """The MissingSettingsError class is raised when the 'AppSettings' class
  fails to recognize a settings key. Please note that the QSettings class
  does not raise any such error, simply returning None. """

  def __init__(self, key: str, ) -> None:
    e = """Unable to recognize given key: %s!""" % key
    Exception.__init__(self, e)
