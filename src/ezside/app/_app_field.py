"""AppField provides a descriptor pointing to the running application and
validates that it an instance of 'App'. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, TYPE_CHECKING, Union, Self

from PySide6.QtCore import QObject, QCoreApplication
from PySide6.QtWidgets import QApplication
from worktoy.base import BaseObject
from worktoy.text import typeMsg

if TYPE_CHECKING:
  from ezside.app import App


class AppField(BaseObject):
  """AppField provides a descriptor pointing to the running application and
  validates that it an instance of 'App'. """

  @staticmethod
  def _validateApp(app: QCoreApplication) -> None:
    """Validates that the running application is an instance of 'App'. """
    if not isinstance(app, QCoreApplication):
      e = typeMsg('app', app, QCoreApplication)
      raise TypeError(e)
    if getattr(app, '__ezside_app__', None) is None:
      e = """The running application is not an instance of 'App'!"""
      raise RuntimeError(e)

  def __get__(self, instance: QObject, owner: QObject) -> Union[App, Self]:
    """Getter-function for the AppField."""
    if instance is None:
      return self
    app = QApplication.instance()
    self._validateApp(app)
    return app

  def __set__(self, *_) -> Never:
    """Setter-function for the AppField."""
    e = """The 'AppField' is read-only!"""
    raise TypeError(e)

  def __delete__(self, *_) -> Never:
    """Deleter-function for the AppField."""
    e = """The 'AppField' is read-only!"""
    raise TypeError(e)

  def __set_name__(self, owner: QObject, name: str) -> None:
    """Sets the name of the descriptor. """
    if name != 'app':
      e = """The 'AppField' must be named 'app'!"""
      raise AttributeError(e)

  def __init__(self, *args, **kwargs) -> None:
    pass
