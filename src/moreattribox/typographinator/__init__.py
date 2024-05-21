"""Typographinator provides an abstraction for text. The base object in
the abstraction is the word. Besides representing words this abstraction
also represents numbers and punctuation. Thus, a paragraph of text can be
represented by an array of words. A Line is not part of any abstraction,
but represents an array of words that can be displayed without wrapping
under the present conditions. The underlying text remains the same whether
rendered as a page wide paragraph or in a column. Only in the very final
step in rendering will be the text be split into lines.

An array of words constitutes a Paragraph, which is the next abstraction
layer. Whereas words are separated by spaces, paragraphs are separated by
linebreaks. .
"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._word import Word
from ._paragraph import Paragraph
from ._chapter import Chapter
from ._memoir import Memoir
