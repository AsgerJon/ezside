"""SizeRule provides a KeeNum class for resize policies. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QSizePolicy
from worktoy.desc import Field
from worktoy.keenum import KeeNum, auto, KeeNumObject

from typing import Self, TYPE_CHECKING

from worktoy.text import joinWords, monoSpace, typeMsg

if TYPE_CHECKING:
  Self = KeeNumObject


class SizeRule(KeeNum):
  """SizeRule provides a KeeNum class for resize policies. """

  base = Field()
  horizontal = Field()
  vertical = Field()
  h = Field()
  v = Field()
  qt = Field()

  EXPAND = auto()
  PREFER = auto()
  FIXED = auto()
  CONTRACT = auto()

  EXPAND_PREFER = auto()
  EXPAND_FIXED = auto()
  EXPAND_CONTRACT = auto()

  PREFER_EXPAND = auto()
  PREFER_FIXED = auto()
  PREFER_CONTRACT = auto()

  FIXED_EXPAND = auto()
  FIXED_PREFER = auto()
  FIXED_CONTRACT = auto()

  CONTRACT_EXPAND = auto()
  CONTRACT_PREFER = auto()
  CONTRACT_FIXED = auto()

  @classmethod
  def getBaseRules(cls) -> list[Self]:
    """getBaseRules returns the base rules for the SizeRule class. """
    return [cls.EXPAND, cls.PREFER, cls.FIXED, cls.CONTRACT]

  @classmethod
  def _getNamedBase(cls, name: str) -> Self:
    """Returns the base rule having the given name"""
    for rule in cls.getBaseRules():
      if rule.name.lower() == name.lower():
        return rule
    e = """No base rule with the name '%s' was found!""" % name
    raise ValueError(e)

  @classmethod
  def _getCombination(cls, *args) -> Self:
    """Returns the combination rule having the given names"""
    if not args:
      e = """No arguments were given!"""
      raise ValueError(e)
    if all([isinstance(arg, cls) for arg in args]):
      return cls._getCombination(*[arg.name for arg in args], )
    for arg in args:
      if not isinstance(arg, str):
        e = typeMsg('ruleName', arg, str)
        raise TypeError(e)
    if len(args) == 1:
      if '_' not in args[0]:
        return cls._getNamedBase(args[0])
      for rule in cls:
        if rule.name.lower() == args[0].lower():
          return rule
    if len(args) == 2:
      hRule = cls._getNamedBase(args[0])
      vRule = cls._getNamedBase(args[1])
      ruleName = '%s_%s' % (hRule.name, vRule.name)
      return cls._getCombination(ruleName)
    e = """'%s._getCombination' expects one or two positional arguments, 
    but received %d arguments: """
    argStr = joinWords(*[str(arg) for arg in args], )
    raise ValueError(monoSpace(e % (cls.__name__, len(args), argStr)))

  @base.GET
  def isBase(self) -> bool:
    """isBase returns True if the rule is a base rule. """
    return True if self in self.getBaseRules() else False

  @horizontal.GET
  @h.GET
  def _getHorizontal(self) -> Self:
    """Getter-function for the horizontal component"""
    if self in self.getBaseRules():
      return self
    return self._getNamedBase(self.name.split('_')[0])

  @horizontal.SET
  @h.SET
  def _setHorizontal(self, value: Self) -> Self:
    """Setter-function for the horizontal component"""
    return self._getCombination(value, self.vertical)

  @vertical.GET
  @v.GET
  def _getVertical(self) -> Self:
    """Getter-function for the vertical component"""
    if self in self.getBaseRules():
      return self
    return self._getNamedBase(self.name.split('_')[1])

  def _getBaseQt(self) -> QSizePolicy.Policy:
    """Returns the Qt version of the base rule"""
    if self not in self.getBaseRules():
      e = """'%s._getBaseQt' supports only base rules!"""
      raise ValueError(monoSpace(e % self.__class__.__name__))
    if 'expand' in self.name.lower():
      return QSizePolicy.Policy.MinimumExpanding
    if 'prefer' in self.name.lower():
      return QSizePolicy.Policy.Preferred
    if 'fixed' in self.name.lower():
      return QSizePolicy.Policy.Fixed
    if 'contract' in self.name.lower():
      return QSizePolicy.Policy.Maximum

  @qt.GET
  def _getQt(self) -> QSizePolicy:
    """Returns the Qt version of the flag"""
    h = self.__class__._getBaseQt(self.horizontal)
    v = self.__class__._getBaseQt(self.vertical)
    p = QSizePolicy()
    p.setHorizontalPolicy(h)
    p.setVerticalPolicy(v)
    return p

  def __add__(self, other: object) -> SizeRule:
    if not isinstance(other, SizeRule):
      return NotImplemented
    if self is other:
      return self
    return self._getCombination(self, other)
