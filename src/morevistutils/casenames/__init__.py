"""The 'casenames' module provides functionality for managing names
consisting of multiple words abstracted from the case. Instances can be
created from different cases and more words may be added to an existing
instance. The class provides conversion back to any of the supported
cases. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_case import AbstractCase
from ._camel_case import CamelCase
from ._kebab_case import KebabCase
from ._name import Name
from ._pascal_case import PascalCase
from ._sentence_case import SentenceCase
from ._snake_case import SnakeCase
from ._title_case import TitleCase

if __name__ != '__main__':
  Name.addCase(CamelCase)
  Name.addCase(SnakeCase)
  Name.addCase(PascalCase)
  Name.addCase(KebabCase)
  Name.addCase(SentenceCase)
  Name.addCase(TitleCase)

__all__ = ['AbstractCase', 'CamelCase', 'SnakeCase', 'PascalCase',
           'KebabCase', 'SentenceCase', 'TitleCase', 'Name']
