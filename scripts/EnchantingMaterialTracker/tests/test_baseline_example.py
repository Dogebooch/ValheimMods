"""
Integration-style test for a simple two-roll baseline scenario.

This test reproduces the calculation described in the runbook for the
"NovusMats" example consisting of two item types – RunestoneMagic and
ShardMagic – both with equal weight.  The first roll has a base chance of
10%% and one draw; the second roll has a base chance of 5%% and two draws.

According to the runbook, when the weight of the target material within
each set is 0.5, the expected combined probability of receiving a
RunestoneMagic item is 0.0875.  This value comes from summing the
individual roll probabilities rather than applying a union calculation.

The test therefore asserts that the sum of the per‑roll probabilities
matches 0.0875.  It also checks that the union probability computed by
union_prob is slightly lower (approx 0.085625), highlighting the small
difference between the two approaches.
"""

import math
import unittest

from scripts.EnchantingMaterialTracker.emt.prob import union_prob, p_roll


class TestBaselineExample(unittest.TestCase):
    """Validate the baseline example from the runbook."""

    def test_novus_mats_example_sum_vs_union(self):
        base1, base2 = 0.10, 0.05
        q = 0.5
        draws1, draws2 = 1, 2

        # Compute per‑roll probabilities
        p1 = p_roll(base1, q, draws1)
        p2 = p_roll(base2, q, draws2)

        # Expected via summation (runbook uses additive method)
        expected_sum = 0.10 * 0.5 + 0.05 * (1 - (1 - 0.5) ** 2)
        self.assertTrue(math.isclose(p1 + p2, expected_sum, rel_tol=1e-9))
        self.assertTrue(math.isclose(expected_sum, 0.0875, rel_tol=1e-4))

        # Compute union probability
        union = union_prob([p1, p2])
        # Union should be slightly lower than the sum
        self.assertLess(union, p1 + p2)
        self.assertTrue(math.isclose(union, 0.085625, rel_tol=1e-4))


if __name__ == "__main__":
    unittest.main()