"""Probability utilities for Enchanting Material Tracker.

This module provides helper functions for combining independent drop events
and computing the probability that at least one target item appears in a
multi‑draw set.  All probabilities are clamped to the range [0, 1] to guard
against accidental overflows or negative values.
"""

from __future__ import annotations

from typing import Iterable, Sequence, Set


def clamp01(x: float) -> float:
    """Clamp a numeric value into the closed interval [0, 1].

    Values below zero return 0.0, values above one return 1.0.  This guard
    prevents arithmetic errors from yielding nonsensical probabilities.
    """
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def union_prob(ps: Iterable[float]) -> float:
    """Return the probability that at least one of the independent events occurs.

    Given a sequence of independent event probabilities ``ps``, this function
    computes ``1 − ∏(1 − p_i)``.  Each element is clamped to [0, 1] prior to
    computing the product.  The result is clamped as well.

    Parameters
    ----------
    ps:
        An iterable of probabilities for independent events.

    Returns
    -------
    float
        The probability that at least one of the events happens.
    """
    prod = 1.0
    for p in ps:
        prod *= (1.0 - clamp01(p))
    return clamp01(1.0 - prod)


def p_roll(base: float, q: float, draws: int) -> float:
    """Compute the probability of getting a target item from a multi‑draw roll.

    Many Valheim loot tables specify that a set of items is drawn ``draws`` times
    with a base chance ``base`` for the set to trigger.  Within the set the
    relative weights of each item define ``q``, the probability that a single draw
    yields one of the target items.  The chance of getting at least one target
    item from the roll is::

        base × (1 − (1 − q)**draws)

    Both ``base`` and ``q`` are clamped to [0, 1] and ``draws`` is coerced to a
    positive integer.

    Parameters
    ----------
    base:
        The base probability that the set is rolled at all.
    q:
        The chance that a single draw yields a target item.
    draws:
        The number of draws from the set.  Values less than one are treated as
        a single draw.

    Returns
    -------
    float
        The probability of at least one target item appearing from the roll.
    """
    base = clamp01(base)
    q = clamp01(q)
    n = 1 if draws < 1 else int(draws)
    return clamp01(base * (1.0 - (1.0 - q) ** n))


def compute_q_from_set(set_items: Sequence[object], target_names: Set[str]) -> float:
    """Compute ``q``, the chance a single draw yields a target, from weighted items.

    Valheim sets often contain a mixture of enchanting materials and other items.
    Each item may define a ``weight`` attribute (defaulting to 1.0) and a ``name``
    attribute.  This helper sums the weights of all items in ``set_items`` and the
    weights of the subset whose ``name`` is in ``target_names``.  The ratio of
    target weight to total weight yields ``q``.

    If the total weight is zero, the function returns 0.0.

    Parameters
    ----------
    set_items:
        An iterable of objects with optional ``weight`` and ``name`` attributes.
    target_names:
        The set of names for the items of interest.

    Returns
    -------
    float
        The probability that a single draw from the set yields a target item.
    """
    total = 0.0
    target = 0.0
    for it in set_items:
        w = float(getattr(it, "weight", 1.0) or 0.0)
        nm = getattr(it, "name", "")
        total += w
        if nm in target_names:
            target += w
    if total <= 0.0:
        return 0.0
    return clamp01(target / total)
