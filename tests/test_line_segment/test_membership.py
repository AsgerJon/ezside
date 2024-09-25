"""Runs membership tests for the LineSegment class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from ezside.tegning import LineSegment, Point


class TestLineSegment(TestCase):
  """Test the LineSegment class."""

  def setUp(self) -> None:
    """Readies the diagonal line segment for testing along with samples."""
    self.diagonal = LineSegment(Point(0, 0), Point(100, 100))
    self.samples = [Point(i, 100 - i) for i in range(101)]

  def test_trivial(self) -> None:
    """Test the trivial properties of the diagonal line segment."""
    for sample in self.samples:
      if (sample.x - sample.y) ** 2:
        self.assertNotIn(sample, self.diagonal)
      else:
        self.assertIn(sample, self.diagonal)
