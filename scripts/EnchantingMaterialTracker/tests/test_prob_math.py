"""
Unit tests for the probability helpers defined in the EMT probability module.

These tests cover the basic behaviour of the union probability and multi-draw
roll functions.  They intentionally use simple numeric cases so the expected
values can be computed by hand.  If these tests fail then the math helper
functions have likely regressed.
"""

import math
import unittest

from scripts.EnchantingMaterialTracker.emt.prob import clamp01, union_prob, p_roll


class TestProbMath(unittest.TestCase):
    """Unit tests for probability helper functions."""

    def test_clamp01_bounds(self):
        """clamp01 should clamp values outside of [0,1]."""
        self.assertEqual(clamp01(-0.5), 0.0)
        self.assertEqual(clamp01(0.0), 0.0)
        self.assertEqual(clamp01(0.3), 0.3)
        self.assertEqual(clamp01(1.0), 1.0)
        self.assertEqual(clamp01(1.5), 1.0)

    def test_union_prob(self):
        """union_prob should compute 1 minus the product of (1 - p_i)."""
        cases = [
            ([], 0.0),  # no events yields zero probability of union
            ([0.0], 0.0),
            ([1.0], 1.0),
            ([0.1, 0.2], 1 - (1 - 0.1) * (1 - 0.2)),
            ([0.1, 0.2, 0.3], 1 - (1 - 0.1) * (1 - 0.2) * (1 - 0.3)),
        ]
        for probs, expected in cases:
            with self.subTest(probs=probs):
                self.assertTrue(
                    math.isclose(
                        union_prob(probs), expected, rel_tol=1e-9, abs_tol=1e-9
                    )
                )

    def test_p_roll(self):
        """p_roll should implement the multi-draw formula base*(1-(1-q)**draws)."""
        cases = [
            (0.0, 0.5, 1, 0.0),            # zero base always yields zero
            (0.5, 0.0, 1, 0.0),            # zero q always yields zero
            (0.5, 1.0, 1, 0.5),            # full q yields base
            (0.5, 0.5, 1, 0.25),           # one draw, half q
            (0.1, 0.5, 1, 0.05),           # example from runbook
            (0.1, 0.5, 2, 0.1 * (1 - (1 - 0.5) ** 2)),
            (0.1, 0.5, 3, 0.1 * (1 - (1 - 0.5) ** 3)),
        ]
        for base, q, draws, expected in cases:
            with self.subTest(base=base, q=q, draws=draws):
                self.assertTrue(
                    math.isclose(
                        p_roll(base, q, draws), expected, rel_tol=1e-9, abs_tol=1e-9
                    )
                )


if __name__ == "__main__":
    unittest.main()