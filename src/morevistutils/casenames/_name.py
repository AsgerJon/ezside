"""Name is the central class in the casenames module providing the
abstraction from snake case, camel case or a custom case defined as a
subclass of AbstractCase."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, Type, Any

from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from morevistutils.casenames import AbstractCase


class Name:
  """A class for managing names consisting of multiple words abstracted from
  the case. Instances can be created from different cases and more words may
  be added to an existing instance. The class provides conversion back to any
  of the supported cases. """

  __inner_words__ = None
  __iter_contents__ = None
  __name_cases__ = None
  __instance_case__ = None

  @classmethod
  def getNameCases(cls, ) -> list[Type[AbstractCase]]:
    """Return a list of the name cases supported by the Name class."""
    if cls.__name_cases__ is None:
      cls.__name_cases__ = []
    else:
      for nameCase in cls.__name_cases__:
        if not issubclass(nameCase, AbstractCase):
          e = """Found item in list of name cases that is not a subclass 
          of AbstractCase. Item: '%s'""" % nameCase
          raise TypeError(monoSpace(e))
    return cls.__name_cases__

  @classmethod
  def addCase(cls, nameCase: type) -> None:
    """Adds a name case to the list of name cases."""
    if isinstance(nameCase, type):
      if issubclass(nameCase, AbstractCase):
        return cls.getNameCases().append(nameCase)
      e = """The given type: '%s' is not a subclass of AbstractCase!"""
      raise TypeError(monoSpace(e % nameCase.__name__))
    e = typeMsg('nameCase', nameCase, type)
    raise TypeError(e)

  @classmethod
  def resolveCase(cls, name: str, **kwargs) -> type:
    """Resolve the case of the name and return an instance of the case."""
    for Case in cls.getNameCases():
      if not isinstance(Case, type):
        e = typeMsg('Case', Case, type)
        raise TypeError(e)
      if issubclass(Case, AbstractCase):
        if Case.recognizeName(name):
          return Case
      else:
        e = """The given type: '%s' is not a subclass of AbstractCase!"""
        raise TypeError(monoSpace(e % Case.__name__))
    if kwargs.get('strict', True):
      e = """Could not resolve the case of the name: '%s'""" % name
      raise ValueError(monoSpace(e))

  @classmethod
  def lookUp(cls, data: dict, key: str) -> Any:
    """Uses the different cases to search the given dictionary for the key"""
    if key in data:
      return data[key]
    words = cls(key)._getInnerWords()
    for NameCase in cls.getNameCases():
      name = NameCase.joinWords(*words, )
      if name in data:
        return data[name]
    return dict.__getitem__(data, key)  # Raises default KeyError

  def __init__(self, *args, **kwargs) -> None:
    self.__inner_words__ = None
    self.__iter_contents__ = None
    self.__name_cases__ = None
    for arg in args:
      if isinstance(arg, str):
        for NameCase in self.getNameCases():
          if NameCase.joinWords(*NameCase.resolveName(arg)) == arg:
            if len(NameCase.resolveName(arg)) > 1:
              for word in NameCase.resolveName(arg):
                self._appendInnerWord(word)
              break
        else:
          self._appendInnerWord(arg)

  def _getInnerWords(self, ) -> list[str]:
    """Return the inner words of the name."""
    if self.__inner_words__ is None:
      self.__inner_words__ = []
    else:
      for word in self.__inner_words__:
        if not isinstance(word, str):
          e = typeMsg('word', word, str)
          raise TypeError(e)
    if not all(self.__inner_words__):
      words = self.__inner_words__
      self.__inner_words__ = []
      for word in words:
        if word:
          self.__inner_words__.append(word)
    return self.__inner_words__

  def _appendInnerWord(self, word: str) -> None:
    """Append a word to the inner words."""
    if self.__inner_words__ is None:
      self.__inner_words__ = []
    self.__inner_words__.append(word)

  def append(self, word: str) -> None:
    """Append a word to the name."""
    self._appendInnerWord(word)

  def __iter__(self, ) -> Self:
    """Implementation of iteration"""
    self.__iter_contents__ = self._getInnerWords()
    return self

  def __next__(self, ) -> str:
    """Implementation of iteration"""
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __contains__(self, word: str) -> bool:
    """Check if the name contains a word."""
    for innerWord in self._getInnerWords():
      if innerWord == word.lower():
        return True
    else:
      return False

  def __len__(self, ) -> int:
    """Return the number of words in the name."""
    return len(self._getInnerWords())

  def __matmul__(self, other: type) -> str:
    """Syntactic sugar for setting the instance case."""
    if isinstance(other, type):
      if issubclass(other, AbstractCase):
        return other.joinWords(*self._getInnerWords())

  def __getitem__(self, index: int) -> str:
    """Return the word at the given index."""
    return self._getInnerWords()[index]

  def __setitem__(self, index: int, value: str) -> None:
    """Set the word at the given index."""
    self._getInnerWords()[index] = value

  def __delitem__(self, index: int) -> None:
    """Delete the word at the given index."""
    self._getInnerWords().pop(index)

  def __str__(self, ) -> str:
    """The string representation is determined by the case of the name."""
    out = '(%s)' % ', '.join(self._getInnerWords())
    if out.startswith('(,'):
      for word in self._getInnerWords():
        print('|%s|' % word)
      raise ValueError
    return out

  def __repr__(self, ) -> str:
    """Representation of code instantiating the Name instance to its
    present state."""
    return 'Name(%s)' % ', '.join(self._getInnerWords())

  def currentHash(self) -> int:
    """Returns the hash of the current state of the name. Please note,
    that this is not the same as the hash of this name instance."""
    return hash(self.__str__())

  def __eq__(self, other: Any) -> bool:
    """Check if the name is equal to the other object."""
    if isinstance(other, Name):
      for (this, that) in zip(self._getInnerWords(), other._getInnerWords()):
        if this != that:
          return False
      return True
    if isinstance(other, str):
      return self == Name(other)
    return NotImplemented
