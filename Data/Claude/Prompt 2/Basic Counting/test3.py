"""
Unit tests for two "count distinct common elements" functions.

ASSUMPTIONS (the description did not specify these, so they are made explicit
and are easy to change in the three config lines below):

  A1. Module name is `basic_counting`.
  A2. The nested-loop function is `find_common(list1, list2)`.
  A3. The set-based function is `find_common_efficient(list1, list2)`.
  A4. Both take two lists of ints and return an int: the number of DISTINCT
      values that appear in both lists (duplicates never inflate the count).
  A5. Neither function should mutate its inputs (a reasonable expectation
      for a pure counting function, not stated explicitly).
  A6. Behavior for invalid inputs (None, non-iterables, non-integer elements)
      is NOT specified. I do not assert a particular exception. I only assert
      that the two implementations behave consistently with each other.
  A7. The random list generator is not tested directly (its name and
      signature are unknown). Instead, randomized lists drawn from a range
      based on list size (assumed here to be 0..size) are used to
      cross-check both functions against an independent oracle.
"""

import random

import pytest

# ---- configuration (edit if the real names differ) -------------------------
from basic_counting import find_common, find_common_efficient  # A1-A3

IMPLEMENTATIONS = [find_common, find_common_efficient]
IDS = ["nested_loops", "sets"]


def oracle(a, b):
    """Independent reference for the stated behavior: distinct shared values."""
    return len(set(a) & set(b))


@pytest.fixture(params=IMPLEMENTATIONS, ids=IDS)
def count_common(request):
    return request.param


# ---- normal inputs ---------------------------------------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([1, 2, 3, 4], [3, 4, 5, 6], 2),
        ([1, 2, 3], [2, 3, 4], 2),
        ([10, 20, 30, 40, 50], [50, 40, 99], 2),
        ([5, 1, 9, 3], [9, 5], 2),
        ([7], [7], 1),
        ([1, 2, 3, 4, 5], [5], 1),
    ],
)
def test_normal_inputs(count_common, a, b, expected):
    assert count_common(a, b) == expected


def test_returns_int(count_common):
    result = count_common([1, 2, 3], [2, 3, 4])
    assert isinstance(result, int)
    assert not isinstance(result, bool)


# ---- empty lists -----------------------------------------------------------
@pytest.mark.parametrize(
    "a, b",
    [
        ([], []),
        ([], [1, 2, 3]),
        ([1, 2, 3], []),
        ([], [0]),
        ([-1], []),
    ],
)
def test_empty_lists_give_zero(count_common, a, b):
    assert count_common(a, b) == 0


# ---- no common elements ----------------------------------------------------
@pytest.mark.parametrize(
    "a, b",
    [
        ([1, 2, 3], [4, 5, 6]),
        ([1, 3, 5], [2, 4, 6]),
        ([0], [1]),
        ([-1, -2], [1, 2]),          # same magnitude, different sign
        ([100], [-100]),
        ([1, 2, 3], [10, 20, 30]),
    ],
)
def test_no_common_elements(count_common, a, b):
    assert count_common(a, b) == 0


# ---- all elements in common ------------------------------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([1, 2, 3], [1, 2, 3], 3),
        ([1, 2, 3], [3, 2, 1], 3),                  # different order
        ([4], [4], 1),
        (list(range(100)), list(range(100)), 100),
        (list(range(100)), list(range(99, -1, -1)), 100),
    ],
)
def test_all_elements_common(count_common, a, b, expected):
    assert count_common(a, b) == expected


def test_one_list_is_subset_of_other(count_common):
    big = list(range(50))
    small = [3, 17, 49]
    assert count_common(big, small) == 3
    assert count_common(small, big) == 3


# ---- partial overlap -------------------------------------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([1, 2, 3, 4, 5], [4, 5, 6, 7, 8], 2),
        ([1, 2, 3, 4, 5], [1, 9, 8, 7, 6], 1),       # overlap at first element
        ([1, 2, 3, 4, 5], [9, 8, 7, 6, 5], 1),       # overlap at last element
        ([1, 2, 3, 4, 5], [9, 3, 8], 1),             # overlap in the middle
        (list(range(0, 20)), list(range(10, 30)), 10),
    ],
)
def test_partial_overlap(count_common, a, b, expected):
    assert count_common(a, b) == expected


# ---- negative integers and zero --------------------------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([-1, -2, -3], [-3, -4, -5], 1),
        ([-5, -4, -3], [-5, -4, -3], 3),
        ([-1, 0, 1], [0], 1),
        ([0], [0], 1),
        ([0, 1, 2], [3, 4, 5], 0),
        ([-1, 0, 1], [-1, 0, 1], 3),
        ([-10, 10], [10, -10], 2),
        ([-1, -2, -3], [1, 2, 3], 0),
        ([0, -0], [0], 1),                           # -0 == 0 for ints
    ],
)
def test_negative_numbers_and_zero(count_common, a, b, expected):
    assert count_common(a, b) == expected


# ---- boundary cases --------------------------------------------------------
def test_single_element_lists_match(count_common):
    assert count_common([0], [0]) == 1
    assert count_common([-7], [-7]) == 1


def test_single_element_lists_differ(count_common):
    assert count_common([0], [1]) == 0
    assert count_common([-7], [7]) == 0


def test_single_element_vs_long_list(count_common):
    assert count_common([500], list(range(1000))) == 1
    assert count_common([1000], list(range(1000))) == 0   # just outside range
    assert count_common([-1], list(range(1000))) == 0     # just below range


def test_overlap_only_at_range_edges(count_common):
    a = list(range(0, 10))        # 0..9
    b = list(range(9, 20))        # 9..19
    assert count_common(a, b) == 1        # only 9
    c = list(range(10, 20))       # 10..19
    assert count_common(a, c) == 0        # adjacent but disjoint


def test_very_large_and_very_small_integers(count_common):
    big = 2**63
    small = -(2**63)
    assert count_common([big, small, 1], [big, small, 2]) == 2
    assert count_common([big], [big + 1]) == 0
    assert count_common([10**100], [10**100]) == 1


def test_large_lists(count_common):
    a = list(range(2000))
    b = list(range(1000, 3000))
    assert count_common(a, b) == 1000


# ---- duplicates (distinct counting) ----------------------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([1, 1, 1], [1], 1),
        ([1], [1, 1, 1], 1),
        ([1, 1, 1], [1, 1], 1),                       # dupes on both sides
        ([1, 1, 2, 2], [1, 2], 2),
        ([1, 1, 2], [1, 2, 2], 2),
        ([1, 1, 1, 1], [2, 2, 2, 2], 0),              # dupes but no overlap
        ([0, 0, 0], [0, 0], 1),
        ([-3, -3, -3], [-3], 1),
        ([1, 2, 3, 3, 3], [3, 3, 4], 1),
        ([5, 5, 6, 6, 7, 7], [5, 6, 7, 5, 6, 7], 3),
    ],
)
def test_duplicates_counted_once(count_common, a, b, expected):
    assert count_common(a, b) == expected


def test_duplicate_multiplicity_does_not_inflate_count(count_common):
    # If duplicates were wrongly multiplied, this would be 3*4 = 12 or 3 or 4.
    assert count_common([9, 9, 9], [9, 9, 9, 9]) == 1


def test_count_never_exceeds_distinct_size_of_either_list(count_common):
    a = [1, 1, 2, 2, 3, 3]
    b = [1, 2, 3, 4, 5, 6, 7]
    result = count_common(a, b)
    assert result == 3
    assert result <= len(set(a))
    assert result <= len(set(b))


# ---- algebraic properties --------------------------------------------------
@pytest.mark.parametrize(
    "a, b",
    [
        ([1, 2, 3], [2, 3, 4]),
        ([1, 1, 2], [2, 2, 3]),
        ([], [1]),
        ([-1, 0, 1], [1, 2, -1]),
    ],
)
def test_symmetry(count_common, a, b):
    assert count_common(a, b) == count_common(b, a)


def test_order_independence(count_common):
    a = [1, 2, 3, 4, 5]
    b = [4, 5, 6, 7]
    expected = count_common(a, b)
    assert count_common(list(reversed(a)), b) == expected
    assert count_common(a, list(reversed(b))) == expected
    shuffled = a[:]
    random.Random(0).shuffle(shuffled)
    assert count_common(shuffled, b) == expected


def test_self_comparison_equals_distinct_count(count_common):
    a = [1, 1, 2, 3, 3, 3, -4, 0, 0]
    assert count_common(a, a) == len(set(a))
    assert count_common(a, list(a)) == len(set(a))


# ---- purity (A5) -----------------------------------------------------------
def test_inputs_not_mutated(count_common):
    a = [3, 1, 2, 2, 1]
    b = [2, 4, 4, 3]
    a_copy, b_copy = a[:], b[:]
    count_common(a, b)
    assert a == a_copy
    assert b == b_copy


def test_same_list_object_passed_twice(count_common):
    a = [1, 2, 2, 3]
    assert count_common(a, a) == 3
    assert a == [1, 2, 2, 3]


def test_repeated_calls_give_same_result(count_common):
    a, b = [1, 2, 3, 3], [3, 4, 1]
    assert count_common(a, b) == count_common(a, b) == 2


# ---- agreement between the two approaches ----------------------------------
@pytest.mark.parametrize(
    "a, b",
    [
        ([], []),
        ([1, 2, 3], [3, 4, 5]),
        ([1, 1, 1], [1]),
        ([-5, 0, 5], [5, 0, -5]),
        (list(range(200)), list(range(100, 300))),
    ],
)
def test_nested_and_set_implementations_agree(a, b):
    assert find_common(a, b) == find_common_efficient(a, b)


# ---- randomized cross-check against the oracle (A7) ------------------------
@pytest.mark.parametrize("size", [0, 1, 2, 5, 10, 50, 100])
@pytest.mark.parametrize("seed", [0, 1, 2, 3, 4])
def test_random_lists_match_oracle(count_common, size, seed):
    rng = random.Random(seed * 1000 + size)
    # Values drawn from a range based on the list size; collisions/duplicates
    # are likely, which exercises the distinct-counting requirement.
    upper = max(size, 1)
    a = [rng.randint(0, upper) for _ in range(size)]
    b = [rng.randint(0, upper) for _ in range(size)]
    assert count_common(a, b) == oracle(a, b)


@pytest.mark.parametrize("seed", range(10))
def test_random_lists_with_negatives_match_oracle(count_common, seed):
    rng = random.Random(seed)
    a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 60))]
    b = [rng.randint(-20, 20) for _ in range(rng.randint(0, 60))]
    assert count_common(a, b) == oracle(a, b)


# ---- invalid / unspecified inputs (A6) -------------------------------------
def _outcome(func, a, b):
    """Return ('ok', value) or ('err', exception_type)."""
    try:
        return ("ok", func(a, b))
    except Exception as exc:  # noqa: BLE001
        return ("err", type(exc))


@pytest.mark.parametrize(
    "a, b",
    [
        (None, [1, 2, 3]),
        ([1, 2, 3], None),
        (None, None),
        (5, [1, 2, 3]),
        ([1, 2, 3], 5),
    ],
)
def test_invalid_inputs_behave_consistently_across_implementations(a, b):
    """Spec doesn't say what happens here; at minimum both approaches should
    agree (both raise the same exception type, or both return the same value).
    A failure signals an inconsistency worth clarifying in the spec."""
    assert _outcome(find_common, a, b) == _outcome(find_common_efficient, a, b)


@pytest.mark.parametrize(
    "a, b",
    [
        ([1, 2, 3], [1.0, 2.0, 3.0]),
        (["1", "2"], [1, 2]),
        ([True, False], [1, 0]),
    ],
)
def test_non_int_or_mixed_type_elements_behave_consistently(a, b):
    """Unspecified (A6). Python treats 1 == 1.0 == True, so the two approaches
    may legitimately differ only if one is implemented unusually; assert
    agreement rather than a specific value."""
    assert _outcome(find_common, a, b) == _outcome(find_common_efficient, a, b)
