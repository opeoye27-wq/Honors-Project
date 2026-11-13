"""
Unit tests for the "count distinct common elements" functions.

ASSUMPTIONS (the description leaves these open; adjust the constants below if wrong):

A1. The functions live in a module named `basic_counting` and are called
    `find_common(list1, list2)` (nested loops) and
    `find_common_efficient(list1, list2)` (Python sets). Change MODULE_NAME,
    NESTED_FUNC_NAME and SET_FUNC_NAME below if the real names differ.
A2. Each function takes two lists of integers as arguments and RETURNS an int
    (it does not print the result or read module-level globals).
A3. "Common elements" means DISTINCT values present in both lists. A value
    that is duplicated within one or both lists is counted once.
A4. The functions must not modify their input lists.
A5. Invalid inputs (None, non-iterables) are assumed to raise TypeError. The
    description does not specify this, so those tests are isolated and marked.
A6. Both functions are expected to give identical results for every input.
A7. The random list generator is out of scope: the request covers only the
    counting functions.
"""

import importlib
import random

import pytest

# --------------------------------------------------------------------------
# Configuration (see A1)
# --------------------------------------------------------------------------
MODULE_NAME = "basic_counting"
NESTED_FUNC_NAME = "find_common"
SET_FUNC_NAME = "find_common_efficient"

_module = importlib.import_module(MODULE_NAME)
find_common = getattr(_module, NESTED_FUNC_NAME)
find_common_efficient = getattr(_module, SET_FUNC_NAME)

IMPLEMENTATIONS = [
    pytest.param(find_common, id="nested_loops"),
    pytest.param(find_common_efficient, id="sets"),
]


@pytest.fixture(params=IMPLEMENTATIONS)
def count_common(request):
    """Runs each test against both implementations."""
    return request.param


def reference_count(a, b):
    """Independent oracle derived from the stated behavior (A3)."""
    return len(set(a) & set(b))


# --------------------------------------------------------------------------
# Normal inputs
# --------------------------------------------------------------------------
class TestNormalInputs:
    def test_simple_partial_overlap(self, count_common):
        assert count_common([1, 2, 3, 4], [3, 4, 5, 6]) == 2

    def test_single_common_element(self, count_common):
        assert count_common([1, 2, 3], [3, 7, 8]) == 1

    def test_unsorted_inputs(self, count_common):
        assert count_common([9, 1, 5, 3], [3, 9, 2, 8]) == 2

    def test_different_lengths_first_longer(self, count_common):
        assert count_common([1, 2, 3, 4, 5, 6, 7], [2, 4]) == 2

    def test_different_lengths_second_longer(self, count_common):
        assert count_common([2, 4], [1, 2, 3, 4, 5, 6, 7]) == 2

    def test_returns_int(self, count_common):
        result = count_common([1, 2], [2, 3])
        assert isinstance(result, int)
        assert not isinstance(result, bool)


# --------------------------------------------------------------------------
# Empty lists
# --------------------------------------------------------------------------
class TestEmptyLists:
    def test_both_empty(self, count_common):
        assert count_common([], []) == 0

    def test_first_empty(self, count_common):
        assert count_common([], [1, 2, 3]) == 0

    def test_second_empty(self, count_common):
        assert count_common([1, 2, 3], []) == 0


# --------------------------------------------------------------------------
# No common elements
# --------------------------------------------------------------------------
class TestNoCommonElements:
    def test_disjoint_lists(self, count_common):
        assert count_common([1, 2, 3], [4, 5, 6]) == 0

    def test_disjoint_interleaved(self, count_common):
        assert count_common([1, 3, 5, 7], [2, 4, 6, 8]) == 0

    def test_disjoint_with_negatives_and_positives(self, count_common):
        assert count_common([-3, -2, -1], [1, 2, 3]) == 0

    def test_values_differing_only_by_sign(self, count_common):
        # 5 and -5 are different values
        assert count_common([5, 10], [-5, -10]) == 0


# --------------------------------------------------------------------------
# All elements in common
# --------------------------------------------------------------------------
class TestAllElementsInCommon:
    def test_identical_lists(self, count_common):
        assert count_common([1, 2, 3, 4], [1, 2, 3, 4]) == 4

    def test_same_elements_different_order(self, count_common):
        assert count_common([1, 2, 3, 4], [4, 3, 2, 1]) == 4

    def test_same_list_object_passed_twice(self, count_common):
        data = [7, 8, 9]
        assert count_common(data, data) == 3

    def test_subset_first_in_second(self, count_common):
        assert count_common([2, 3], [1, 2, 3, 4]) == 2

    def test_subset_second_in_first(self, count_common):
        assert count_common([1, 2, 3, 4], [2, 3]) == 2


# --------------------------------------------------------------------------
# Partial overlap
# --------------------------------------------------------------------------
class TestPartialOverlap:
    def test_overlap_at_start(self, count_common):
        assert count_common([1, 2, 3], [1, 2, 9]) == 2

    def test_overlap_at_end(self, count_common):
        assert count_common([7, 8, 9], [0, 8, 9]) == 2

    def test_overlap_in_middle(self, count_common):
        assert count_common([1, 5, 9], [2, 5, 8]) == 1

    def test_half_overlap(self, count_common):
        assert count_common(list(range(0, 10)), list(range(5, 15))) == 5


# --------------------------------------------------------------------------
# Duplicates (A3: count distinct common values only)
# --------------------------------------------------------------------------
class TestDuplicates:
    def test_duplicates_in_first_list_only(self, count_common):
        assert count_common([1, 1, 1, 2], [1, 3]) == 1

    def test_duplicates_in_second_list_only(self, count_common):
        assert count_common([1, 3], [1, 1, 1, 2]) == 1

    def test_duplicates_in_both_lists_counted_once(self, count_common):
        assert count_common([2, 2, 2], [2, 2]) == 1

    def test_multiple_distinct_values_with_duplicates(self, count_common):
        assert count_common([1, 1, 2, 2, 3], [2, 2, 3, 3, 4]) == 2

    def test_all_same_value_in_both(self, count_common):
        assert count_common([5] * 100, [5] * 50) == 1

    def test_duplicates_without_common_values(self, count_common):
        assert count_common([1, 1, 2, 2], [3, 3, 4, 4]) == 0

    def test_duplicate_count_does_not_multiply(self, count_common):
        # Pair-counting (3 x 4 = 12) would be a bug under distinct semantics.
        assert count_common([9, 9, 9], [9, 9, 9, 9]) == 1

    def test_result_never_exceeds_distinct_sizes(self, count_common):
        a = [1, 1, 2, 2, 3, 3]
        b = [1, 2, 3, 3, 3, 3, 3]
        result = count_common(a, b)
        assert result == 3
        assert result <= len(set(a))
        assert result <= len(set(b))


# --------------------------------------------------------------------------
# Negative integers and zero
# --------------------------------------------------------------------------
class TestNegativesAndZero:
    def test_negative_common(self, count_common):
        assert count_common([-1, -2, -3], [-3, -4, -5]) == 1

    def test_all_negative_identical(self, count_common):
        assert count_common([-5, -4, -3], [-3, -4, -5]) == 3

    def test_zero_common(self, count_common):
        assert count_common([0, 1, 2], [0, 5, 6]) == 1

    def test_zero_only_in_one_list(self, count_common):
        assert count_common([0, 1, 2], [1, 2, 3]) == 2

    def test_zero_only_lists(self, count_common):
        assert count_common([0, 0, 0], [0]) == 1

    def test_mixed_sign_overlap(self, count_common):
        assert count_common([-2, -1, 0, 1, 2], [-1, 0, 1, 3]) == 3

    def test_negative_zero_equivalent_to_zero(self, count_common):
        # For ints, -0 == 0.
        assert count_common([-0], [0]) == 1


# --------------------------------------------------------------------------
# Boundary cases
# --------------------------------------------------------------------------
class TestBoundaryCases:
    def test_single_element_lists_equal(self, count_common):
        assert count_common([1], [1]) == 1

    def test_single_element_lists_different(self, count_common):
        assert count_common([1], [2]) == 0

    def test_single_vs_empty(self, count_common):
        assert count_common([1], []) == 0
        assert count_common([], [1]) == 0

    def test_common_only_first_elements(self, count_common):
        assert count_common([1, 2, 3], [1, 8, 9]) == 1

    def test_common_only_last_elements(self, count_common):
        assert count_common([1, 2, 3], [7, 8, 3]) == 1

    def test_large_integers(self, count_common):
        big = 10**18
        assert count_common([big, big + 1], [big + 1, big + 2]) == 1

    def test_very_large_negative_integers(self, count_common):
        small = -(10**18)
        assert count_common([small, small - 1], [small, small + 1]) == 1

    def test_adjacent_values_not_confused(self, count_common):
        assert count_common([1, 3, 5], [2, 4, 6]) == 0

    def test_range_boundary_values_from_list_size(self, count_common):
        # Values drawn from a range based on list size n, e.g. 0..n or 1..n.
        # Assumed boundaries: the minimum and maximum values must be matched.
        n = 10
        assert count_common([0, n], [0, n]) == 2
        assert count_common([0, n], [1, n - 1]) == 0

    def test_large_identical_lists(self, count_common):
        data = list(range(2000))
        assert count_common(data, data) == 2000

    def test_large_disjoint_lists(self, count_common):
        assert count_common(list(range(1000)), list(range(1000, 2000))) == 0

    def test_large_lists_with_many_duplicates(self, count_common):
        a = [i % 10 for i in range(3000)]
        b = [i % 20 for i in range(3000)]
        assert count_common(a, b) == 10


# --------------------------------------------------------------------------
# Properties (A3, A4, A6)
# --------------------------------------------------------------------------
class TestProperties:
    def test_symmetry(self, count_common):
        a = [1, 2, 2, 3, 10, -4]
        b = [2, 3, 3, 7, -4, -4]
        assert count_common(a, b) == count_common(b, a)

    def test_inputs_not_modified(self, count_common):
        a = [3, 1, 2, 2, 5]
        b = [5, 5, 2, 9]
        a_copy, b_copy = list(a), list(b)
        count_common(a, b)
        assert a == a_copy
        assert b == b_copy

    def test_repeated_calls_give_same_result(self, count_common):
        a, b = [1, 2, 3, 3], [3, 4, 1]
        assert count_common(a, b) == count_common(a, b) == 2

    def test_result_is_non_negative(self, count_common):
        assert count_common([1, 2], [3, 4]) >= 0

    def test_result_bounded_by_shorter_list(self, count_common):
        a, b = [1, 2, 3, 4, 5, 6], [2, 3]
        assert count_common(a, b) <= min(len(a), len(b))

    def test_both_implementations_agree_on_fixed_cases(self):
        cases = [
            ([], []),
            ([1], [1]),
            ([1, 1, 2], [2, 2, 3]),
            ([-1, 0, 1], [0, 1, 2]),
            ([5, 5, 5], [5]),
            (list(range(50)), list(range(25, 75))),
        ]
        for a, b in cases:
            assert find_common(a, b) == find_common_efficient(a, b), (a, b)

    @pytest.mark.parametrize("seed", range(25))
    def test_randomized_against_reference(self, count_common, seed):
        """Random lists drawn from a size-dependent range, checked against
        an independent oracle (distinct intersection size)."""
        rng = random.Random(seed)
        size = rng.randint(0, 60)
        high = max(size, 1)
        a = [rng.randint(0, high) for _ in range(size)]
        b = [rng.randint(0, high) for _ in range(size)]
        assert count_common(a, b) == reference_count(a, b)

    @pytest.mark.parametrize("seed", range(10))
    def test_randomized_with_negatives_against_reference(self, count_common, seed):
        rng = random.Random(1000 + seed)
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 80))]
        b = [rng.randint(-20, 20) for _ in range(rng.randint(0, 80))]
        assert count_common(a, b) == reference_count(a, b)


# --------------------------------------------------------------------------
# Invalid inputs (A5, behavior not specified in the description)
# --------------------------------------------------------------------------
class TestInvalidInputs:
    @pytest.mark.parametrize("bad", [None, 5, 3.14])
    def test_non_iterable_first_argument_raises(self, count_common, bad):
        with pytest.raises(TypeError):
            count_common(bad, [1, 2, 3])

    @pytest.mark.parametrize("bad", [None, 5, 3.14])
    def test_non_iterable_second_argument_raises(self, count_common, bad):
        with pytest.raises(TypeError):
            count_common([1, 2, 3], bad)

    def test_missing_arguments_raise(self, count_common):
        with pytest.raises(TypeError):
            count_common([1, 2, 3])
        with pytest.raises(TypeError):
            count_common()