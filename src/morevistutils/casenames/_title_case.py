"""
A class for managing names in the title case format.
Title Case capitalizes the first letter of every word.
"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
from morevistutils.casenames import AbstractCase


class TitleCase(AbstractCase):
  """
  A class for managing names in the title case format.
  Title Case capitalizes the first letter of every word.
  """

  @classmethod
  def joinWords(cls, *words: str) -> str:
    """
    Join the words together using the rules of the title case.
    """
    return ' '.join(word.capitalize() for word in words)

  @classmethod
  def resolveName(cls, name: str) -> list[str]:
    """
    Assuming the name is in title case, this method returns a list of words
    with the first letter of each word capitalized.
    """
    return name.split()
