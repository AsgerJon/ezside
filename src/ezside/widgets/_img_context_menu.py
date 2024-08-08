"""ImgContextMenu widget provides a subclass of QMenu creating a context
menu for the ImgEdit widget. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenu
from worktoy.desc import AttriBox, THIS

from ezside.app import EZAction


class ImgContextMenu(QMenu):
  """ImgContextMenu widget provides a subclass of QMenu creating a context
  menu for the ImgEdit widget. """

  selectColor = AttriBox[EZAction](THIS, 'Select Color')
  selectRadius = AttriBox[EZAction](THIS, 'Select Radius')

  def __init__(self, parent=None) -> None:
    """Initializes the context menu."""
    QMenu.__init__(self, parent, )
    self.addAction(self.selectColor, )
    self.addAction(self.selectRadius)
