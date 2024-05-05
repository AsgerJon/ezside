"""BaseWidget provides a common base class for all widgets in the
application."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Optional

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QWidget
from attribox import AttriBox
from vistutils.waitaminute import typeMsg

from ezside import BaseWindow
from ezside.app import App
from ezside.core import parseParent
from ezside.widgets import _AttriWidget
from morevistutils.metadec import WhoDat


@WhoDat()
class BaseWidget(_AttriWidget):
  """BaseWidget provides a common base class for all widgets in the
  application."""

  styleId = AttriBox[str]('base')

  @staticmethod
  def _parseStyleId(**kwargs) -> Optional[str]:
    """Parses the styleId from the keyword arguments."""
    for key in ['styleId', 'style', 'id', '__fb']:
      if key in kwargs:
        styleId = kwargs[key]
        if isinstance(styleId, str):
          return styleId
        e = typeMsg('styleId', styleId, str)
        raise TypeError(e)

  def __init__(self: BaseWidget, *args, **kwargs) -> None:
    """Subclasses that wish to allow __init__ to set the value of the
    'styleId' and other subclass specific primitive attributes, must apply
    these before invoking the parent __init__ method. This is because
    the __init__ automatically triggers the rest of the 'init' methods.
    Please note that BaseWidget will look for keyword arguments to set the
    styleId, at the following names:
      - 'styleId'
      - 'style'
      - 'id'
    defaulting to 'base' if none are found. """
    parent = parseParent(args)
    if parent is None:
      QWidget.__init__(self)
    else:
      QWidget.__init__(self, parent)
    self.styleId = self._parseStyleId(**kwargs, __fb='base')
    self.initStyle()
    self._universalInit()
    self.initUi()
    self.initSignalSlot()

  def getStyleFallbacks(self, ) -> dict[str, Any]:
    """Getter-function for style fallbacks. Subclasses are not required to
    reimplement this method, but only styles specified in the schema returned
    by this method can be centrally managed."""

  def getStyleSchema(self, ) -> dict[str, type]:
    """Getter-function for the style types. This method is auto generated
    from the getStyleFallbacks method. Subclasses reimplementing this
    method should leave the parent functionality intact. """
    out = {}
    for key, val in self.getStyleFallbacks().items():
      if key in out:
        e = """Duplicate key: '%s' in style fallbacks.""" % key
        raise KeyError(e)
      out[key] = type(val)
    return out

  def initStyle(self, ) -> None:
    """Initializes the style for the widget. Optional for subclasses to
    implement. """

  def _universalInit(self) -> None:
    """This method applies to all widgets. Subclasses are not permitted to
    reimplement. This prohibition will be enforced in a future update."""
    self.setMinimumSize(32, 32)

  @abstractmethod
  def initUi(self, ) -> None:
    """Initializes the user interface for the widget. Required for subclasses
    to implement. """

  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the widget. Optional for
    subclasses to implement."""

  @staticmethod
  def getApp() -> QCoreApplication:
    """Returns the application."""
    app = QCoreApplication.instance()
    if getattr(app, '__main_app__', None) is not None:
      return app
    e = """Expected application instance to have set the '__main_app__'
    attribute."""
    raise TypeError(e)

  @staticmethod
  def getMain() -> BaseWindow:
    """Getter-function for the owning main window"""
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      assert isinstance(app, App)
    return app.getMain()
