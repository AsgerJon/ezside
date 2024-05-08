"""BaseWidget provides a common base class for all widgets in the
application."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from PySide6.QtGui import QPaintEvent, QPainter, QColor, QPen
from icecream import ic

from ezside.core import SolidLine, emptyBrush
from ezside.widgets import _BaseWidgetPrivates

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class BaseWidget(_BaseWidgetPrivates):
  """BaseWidget provides a common base class for all widgets in the
  application."""

  @abstractmethod
  def initUi(self, ) -> None:
    """Initializes the user interface for the widget. This is where
    subclasses should organize nested widgets and layouts. Standalone
    widgets may return an empty reimplementation. """

  @abstractmethod
  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the widget. Subclasses
    with nested widgets and internal signal and slot logic, should
    implement this method to organize these. This method is invoked only
    after initUi, so the reimplementation may rely on widgets instantiated
    during initUi to be available. All external signals and slots, must be
    ready before this method returns. If not needed, implement an empty
    method."""

  @classmethod
  @abstractmethod
  def registerFields(cls) -> dict[str, Any]:
    """Subclasses are required to implement this method to provide
    centrally managed settings. The method should return a dictionary
    mapping setting names to fallback values. An empty dictionary may be
    returned if no settings are required.

    This method is expected to be available to class decorators. This
    means that the class creation tries to invoke '__set_name__' on all
    descriptors before class decorators receive the finished class. This
    allows for fields to be provided by descriptor classes the implement
    __set_name__.

    In contrast to 'registerStates', 'registerDynamicFields' and to this
    method there is no registerStyleIds method. Instead, styleIds should
    be defined at instantiation time. This allows the field values to be
    editable during runtime and even to be persistent across sessions
    thanks to the AppSettings class which is a subclass of QSettings. """

  @classmethod
  @abstractmethod
  def registerStates(cls, ) -> list[str]:
    """State-aware widgets are expected to implement this method to return
    a list of the states supported by this class. Subclass implementation
    must return a list of at least one state. The suggested name for this
    state is 'defaultState'.

    The second half of the docstring for 'registerFields' applies to this
    method as well. """

  @classmethod
  @abstractmethod
  def registerDynamicFields(cls, ) -> dict[str, Any]:
    """Subclasses may implement this method to define dynamic values at
    fields that depend on the current state and style id. """

  @abstractmethod
  def detectState(self, ) -> str:
    """State-aware widgets should implement this method to define which
    state the widget is currently in. Please note that if this method
    returns an object that is not an instance of 'str' present in the
    static list of states, it will result in undefined behaviour. """

  def paintEvent(self, event: QPaintEvent) -> None:
    """The paintEvent method paints the widget."""
    if self.__debug_flag__ is None:
      return
    painter = QPainter()
    painter.begin(self)
    viewRect = painter.viewport()
    pen = QPen()
    pen.setStyle(SolidLine)
    pen.setWidth(1)
    pen.setColor(QColor(0, 0, 0, ))
    painter.setPen(pen)
    painter.setBrush(emptyBrush())
    painter.drawRoundedRect(viewRect, 4, 4)
    painter.end()
