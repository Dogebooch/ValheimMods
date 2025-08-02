"""Monte‑Carlo validation of the drop‑rate equation.

The script simulates item drops using the probability formula described in the
project documentation and compares the empirical drop rate against the expected
value. A simple 99% confidence interval is printed to illustrate accuracy.
"""

from __future__ import annotations

import math
import random


def drop_rate(ci: float, m_global: float = 1.0, m_world: float = 1.0,
              m_stars: float = 1.0, rho: float = 0.0, m_extras: float = 1.0) -> float:
    """Return effective drop probability per kill/open event."""
    return (ci / 100) * m_global * m_world * m_stars * (1 - rho) * m_extras


def simulate(p: float, trials: int = 100_000) -> tuple[float, float, float]:
    """Simulate Bernoulli trials and return (mean, low, high) for 99% CI."""
    hits = sum(random.random() < p for _ in range(trials))
    mean = hits / trials
    # Normal approximation 99% CI
    z = 2.576
    margin = z * math.sqrt(mean * (1 - mean) / trials)
    return mean, mean - margin, mean + margin


def main() -> None:
    params = dict(ci=25, m_global=1.0, m_world=1.0, m_stars=1.0, rho=0.1, m_extras=1.0)
    expected = drop_rate(**params)
    observed, low, high = simulate(expected)
    print(f"Expected drop rate: {expected:.5f}")
    print(f"Simulated drop rate: {observed:.5f}")
    print(f"99% CI: [{low:.5f}, {high:.5f}]")
    if low <= expected <= high:
        print("Result: within confidence interval")
    else:
        print("Result: outside confidence interval")


if __name__ == "__main__":
    main()
