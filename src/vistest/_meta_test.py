"""MetaTest provides the metaclass for test classes. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.metas import AbstractMetaclass

Bases: tuple[type, ...]


class MetaTest(AbstractMetaclass):
  """MetaTest provides the metaclass for test classes. """
