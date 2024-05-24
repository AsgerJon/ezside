"""TestNamespace provides the namespace for the MetaTest metaclass. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.metas import BaseNamespace


class TestNamespace(BaseNamespace):
  """TestNamespace provides the namespace for the MetaTest metaclass. """

  def compile(self) -> dict:
    """Compiles the contents to a dictionary mapping. """
    out = {}
    for (key, val) in dict.items(self):
      out |= {key: val}
    return out
