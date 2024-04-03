"""The defaults module organizes the defaults into a class used in
development that names each setting and value. In production the class
gets instantiated with the defaults and values from a defaults file. This
file will then be updated by the user. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._settings import Settings
