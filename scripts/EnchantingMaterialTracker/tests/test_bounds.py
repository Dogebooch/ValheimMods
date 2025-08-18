"""
Property tests ensuring that the probability functions never return values
outside the closed interval [0, 1].  These tests sample a range of
randomised inputs and assert that both `p_roll` and `union_prob` are
properly clamped.  If either function ever returns a negative number or a
value greater than one, the clamping logic has failed.
"""

import random
import unittest

from scripts.EnchantingMaterialTracker.emt.prob import clamp01, union_prob, p_roll


class TestBounds(unittest.TestCase):
    """Tests to ensure probabilities are bounded in [0,1]."""

    def test_clamp01_properties(self):
        """Randomised test to ensure clamp01 never exceeds bounds."""
        for _ in range(100):
            x = random.uniform(-10.0, 10.0)
            c = clamp01(x)
            self.assertGreaterEqual(c, 0.0)
            self.assertLessEqual(c, 1.0)

    def test_p_roll_bounds(self):
        """Randomised test to ensure p_roll is always between 0 and 1."""
        for _ in range(100):
            base = random.uniform(-1.0, 2.0)
            q = random.uniform(-1.0, 2.0)
            draws = random.randint(0, 5)
            p = p_roll(base, q, draws)
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 1.0)

    def test_union_prob_bounds(self):
        """Randomised test to ensure union_prob is always between 0 and 1."""
        for _ in range(100):
            n = random.randint(0, 5)
            ps = [random.uniform(-1.0, 2.0) for _ in range(n)]
            u = union_prob(ps)
            self.assertGreaterEqual(u, 0.0)
            self.assertLessEqual(u, 1.0)


if __name__ == "__main__":
    unittest.main()