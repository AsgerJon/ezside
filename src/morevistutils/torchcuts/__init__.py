"""The 'torchcuts' module provides names for functions and types that are
defined in both numpy and torch. For data types, lower case names denote
numpy version and upper case the torch version. For functions, the most
common functions the torch versions have special names, and the numpy
versions receive no special treatment."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import numpy
import torch

Oh = torch.zeros
J = torch.ones
I = torch.eye
T = torch.transpose
D = torch.diag
R = torch.rand
Rn = torch.randn

F32 = torch.float32
F64 = torch.float64
C64 = torch.complex64
C128 = torch.complex128
I64 = torch.int64
I32 = torch.int32
I16 = torch.int16
I8 = torch.int8
U64 = torch.uint64
U32 = torch.uint32
U16 = torch.uint16
U8 = torch.uint8

f32 = numpy.float32
f64 = numpy.float64
c64 = numpy.complex64
c128 = numpy.complex128
i64 = numpy.int64
i32 = numpy.int32
i16 = numpy.int16
i8 = numpy.int8
u64 = numpy.uint64
u32 = numpy.uint32
u16 = numpy.uint16

__all__ = ['Oh', 'J', 'I', 'T', 'D', 'R', 'Rn', 'F32', 'F64', 'C64', 'C128',
           'I64', 'I32', 'I16', 'I8', 'U64', 'U32', 'U16', 'U8', 'f32',
           'f64', 'c64', 'c128', 'i64', 'i32', 'i16', 'i8', 'u64', 'u32',
           'u16']
