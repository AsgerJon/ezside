"""BaseWidget provides a common base class for all widgets in the
application."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from icecream import ic

from ezside.widgets import _BaseWidgetPrivates

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class BaseWidget(_BaseWidgetPrivates):
  """BaseWidget provides a common base class for all widgets in the
  application."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the BaseWidget.
    Please note that BaseWidget will look for keyword arguments to set the
    styleId, at the following names:
      - 'styleId'
      - 'style'
      - 'id'
    The default styleId is 'normal'. """
    super().__init__(*args, **kwargs)

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
    """Getter-function for the dynamic fields. Subclasses should return
    key value pairs with the key of the following format:
    className/styleId/state/fieldName
    with className being the name of the class. By stating this explicitly,
    issues with conflicts between base classes and subclasses are avoided.
    For example, if widget class has a QPen instance for base state and
    another for hover state, the registerFields method should return the
    instance for base state, and this method should define for the hover
    state.
    basePen = QPen()
    hoverPen = QPen()
    Then the registerFields method should contain:
    'borderPen': basePen
    and this method should contain:
    'Button/normal/hover/borderPen': hoverPen
    This way, the hoverPen is only used when the widget is in the hover
    state. Fields not defined in this method fall backs to the value defined
    by registerFields. """

  @abstractmethod
  def detectState(self, ) -> str:
    """State-aware widgets should implement this method to define which
    state the widget is currently in. Please note that if this method
    returns an object that is not an instance of 'str' present in the
    static list of states, it will result in undefined behaviour. """

  def getStyle(self, name: str) -> Any:
    """This method looks up the named style using the AppSettings class.
    This means that it may be persistently changed during runtime. """
    return self._getNamedStyle(name)
