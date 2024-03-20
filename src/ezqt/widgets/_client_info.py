"""ClientInfo shows static information about the current client"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout
from attribox import AttriBox

from ezqt.core import Tight
from ezqt.widgets import BaseWidget, TextLabel


class ClientInfo(BaseWidget):
  """ClientInfo shows static information about the current client"""

  uri = AttriBox[TextLabel]('URI')
  robotId = AttriBox[TextLabel]('Robot ID')
  customerId = AttriBox[TextLabel]('Customer ID')
  baseLayout = AttriBox[QVBoxLayout]()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(128, 128)
    self.uri.initUi()
    self.uri.setSizePolicy(Tight, Tight)
    self.baseLayout.addWidget(self.uri)
    self.robotId.initUi()
    self.robotId.setSizePolicy(Tight, Tight)
    self.baseLayout.addWidget(self.robotId)
    self.customerId.initUi()
    self.customerId.setSizePolicy(Tight, Tight)
    self.baseLayout.addWidget(self.customerId)
    self.setLayout(self.baseLayout)
