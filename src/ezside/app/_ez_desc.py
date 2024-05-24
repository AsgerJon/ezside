"""EZDesc subclasses AbstractDescriptor from the AttriBox package. It
should be further subclassed to provide descriptors for classes in the
framework. Upon instantiation, it allows setting either a default value or
a settings id. This would allow multiple classes to share the same
settings. For example the same background QBrush instance. Please note, that
the settingsId is set at instantiation time and is optional. For this
reason, subclasses may provide a fallback value.

In summary:
  - EZDesc implements the descriptor protocol by subclasses
  AbstractDescriptor from the AttriBox package.
  - ContentClass is the nomenclature used when referring to the class
  whose instances are created and returned by the EZDesc subclasses.
  - OwnerClass is the nomenclature referring to the class with an
  attribute of the ContentClass, but provided for by the use of the EZDesc
  subclass.
  - ContentDesc is the nomenclature referring to the EZDesc subclass that
  provides the descriptor for the ContentClass.
  - The EZDesc itself provides an __init__ function whose first argument
  is the settingsId. Please note that the rest of the framework assumes this
  to always be the case. Subclasses deviating can expect UNDEFINED BEHAVIOR!
  - The object returned by the QSettings instance on the settingsId should
  be an instance of the ContentClass. If missing, subclasses should raise
  the MissingSettingsError rather than using their own fallback. The
  EZDesc itself provides this validation."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Callable, Never

from icecream import ic
from attribox import AbstractDescriptor
from vistutils.waitaminute import typeMsg

from ezside.app import AppDesc, Settings

ic.configureOutput(includeContext=True)


class EZDesc(AbstractDescriptor):
  """EZDesc subclasses AbstractDescriptor from the AttriBox package. It
  should be further subclassed to provide descriptors for classes in the
  framework. Upon instantiation, it allows setting either a default value or
  a settings id. This would allow multiple classes to share the same
  settings. For example the same background QBrush instance. """

  __on_create__ = None
  __settings_id__ = None
  __pos_args__ = None
  __key_args__ = None

  app = AppDesc()
  settings = Settings()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the EZDesc."""
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self.__pos_args__ = [*args, ]
    self.__key_args__ = {**kwargs, }

  def getArgs(self) -> list:
    """Getter-function for positional arguments given at instantiation."""
    return self.__pos_args__

  def getKwargs(self) -> dict:
    """Getter-function for keyword arguments given at instantiation."""
    return self.__key_args__

  def getContentClass(self) -> type:
    """Return the class that the descriptor provides. Subclasses should
     implement this method to define the type of the content class. """

  def create(self, instance: object, owner: type, **kwargs) -> Any:
    """Create the content class instance. Subclasses should implement this
    method to define how the contentInstance is created. Please note, that
    subclasses are expected to return the created object of the
    contentClass without assigning. """

  def _createHook(self, *args, **kwargs) -> None:
    """This method is invoked when ever the createContent method
    successfully instantiates the content class. It alerts the methods
    decorated with the @CREATE decorator. """

  def _getCreateHooked(self, **kwargs) -> list[Callable]:
    """Getter-function for the list of methods that are hooked to the
    'create' hook. """
    if self.__on_create__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__on_create__ = []
      return self._getCreateHooked(_recursion=True)
    if isinstance(self.__on_create__, list):
      for callMeMaybe in self.__on_create__:
        if not callable(callMeMaybe):
          e = typeMsg('callMeMaybe', callMeMaybe, Callable)
          raise TypeError(e)
      else:
        return self.__on_create__
    e = typeMsg('on_create', self.__on_create__, list)
    raise TypeError(e)

  def _getCreateHookedAppend(self, **kwargs) -> Callable:
    """Getter-function for the append function on the list of hooked
    methods."""
    return self._getCreateHooked().append

  def _hookCreate(self, callMeMaybe: Callable, **kwargs) -> Callable:
    """Hook a method to the 'create' hook. """
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
    if callMeMaybe in self._getCreateHooked():
      return callMeMaybe
    if kwargs.get('_recursion', False):
      raise RecursionError
    self._getCreateHookedAppend()(callMeMaybe)
    return self._hookCreate(callMeMaybe, _recursion=True)

  def CREATE(self, callMeMaybe: Callable) -> Callable:
    """Decorator for hooking a method to the 'create' hook. Methods hooked
    this way are returned without modifications. When an instance of the
    content class is created, decorated methods receive the instance for
    whom the object was created and the newly created object. This is to
    support the fact that the decorator is called while the owning class
    body is still running. What is received by the decorator is the not
    yet bounded to anything but is the function itself."""
    return self._hookCreate(callMeMaybe)

  def _alertCreateHooked(self, instance: object, content: object) -> None:
    """Alert all methods hooked to the 'create' hook. """
    for callMeMaybe in self._getCreateHooked():
      callMeMaybe(instance, object)

  def __instance_get__(self, instance: object, owner: type, **kwargs) -> Any:
    """The EZDesc implementation of the required instance getter should
    not be overridden by subclasses. """
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    content = getattr(instance, pvtName, None)
    if content is None:
      if kwargs.get('_recursion', False):
        print('%s' % owner.__name__)
        raise RecursionError
      content = self.create(instance, owner, id=self.__settings_id__)
      setattr(instance, pvtName, content)
      return self.__instance_get__(instance, owner, _recursion=True)
    if isinstance(content, self.getContentClass()):
      self._alertCreateHooked(instance, content)
      return content
    e = typeMsg('content', content, self.getContentClass())
    raise TypeError(e)

  def __set__(self, instance: object, value: object) -> None:
    """Subclasses are encouraged to implement the setter function to
    define relevant setting behaviour. If the setter is not implemented,
    the default implementation replaces the content instance with the
    received value without any validation.

    Example use case:
    Subclasses whose inner content is a QBrush or QPen for example, should
    when the value is an instance of QColor change the color of the
    content instance."""
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, value)

  def __delete__(self, instance: object) -> Never:
    """Subclasses can provide an implementation of the delete method. If
    not the default behaviour raises a TypeError."""
    return AbstractDescriptor.__delete__(self, instance)
