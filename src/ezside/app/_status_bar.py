"""StatusBar subclasses QStatusBar providing the custom status bar. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QStatusBar, QLabel, QWidget

from worktoy.desc import AttriBox, THIS


class StatusBar(QStatusBar):
  """StatusBar subclasses QStatusBar providing the custom status bar. """

  permanentWidget = AttriBox[QLabel]('breh', THIS)

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QWidget):
        QStatusBar.__init__(self, arg)
        break
    else:
      QStatusBar.__init__(self)

  def initUi(self, ) -> None:
    self.addPermanentWidget(self.permanentWidget)
    self.showMessage('Ready')
