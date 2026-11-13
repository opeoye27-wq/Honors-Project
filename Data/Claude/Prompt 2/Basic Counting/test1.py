"""
Unit tests for the "count common elements" functions.

ASSUMPTIONS (the description does not specify these, so they are made explicit):

1. Function names: the description says there are two functions (a nested-loop
   approach and a set-based approach) but does not name them. This file assumes
   `find_common(list1, list2)` and `find_common_efficient(list1, list2)`,
   importable from a module named `basic_counting`. Change the import and the
   IMPLEMENTATIONS list below if the real names differ.
2. Return value: each function returns an int, the number of DISTINCT values
   present in both lists (not the values themselves).
3. Input mutation: the functions should not modify their input lists.
4. Invalid inputs (None, non-iterables, non-integer elements): the description
   specifies no behavior, so those tests only check that the two
   implementations behave CONSISTENTLY with each other (both raise, or both
   return the same value). They do not assert a specific exception type.
5. The random list generator is not named or specified, so it is not tested.
   Tests that depend on it are limited to randomized agreement checks between
   the two counting functions, which are validated against an independent
   reference computed inside this test file.
"""

import random

import pytest

# ASSUMPTION: module and function names (see note 1 above).
from basic_counting import find_common, find_common_efficient

IMPLEMENTATIONS = [
    pytest.param(find_common, id="nested_loops"),
    pytest.param(find_common_efficient, id="sets"),
]


def reference_count(a, b):
    """Independent oracle: number of distinct values present in both lists."""
    return len(set(a) & set(b))


@pytest.fixture(params=IMPLEMENTATIONS)
def count_common(request):
    return request.param


# ---------------------------------------------------------------------------
# Normal inputs
# ---------------------------------------------------------------------------

class TestNormalInputs:
    def test_partial_overlap(self, count_common):
        assert count_common([1, 2, 3, 4], [3, 4, 5, 6]) == 2

    def test_single_common_element(self, count_common):
        assert count_common([1, 2, 3], [3, 7, 8]) == 1

    def test_unsorted_inputs(self, count_common):
        assert count_common([9, 1, 5, 3], [3, 8, 1, 2]) == 2

    def test_lists_of_different_lengths(self, count_common):
        assert count_common([1, 2, 3, 4, 5, 6, 7, 8], [2, 4]) == 2

    def test_first_list_shorter(self, count_common):
        assert count_common([2, 4], [1, 2, 3, 4, 5, 6, 7, 8]) == 2

    def test_returns_int(self, count_common):
        result = count_common([1, 2, 3], [2, 3, 4])
        assert isinstance(result, int)
        assert not isinstance(result, bool)


# ---------------------------------------------------------------------------
# Empty lists
# ---------------------------------------------------------------------------

class TestEmptyLists:
    def test_both_empty(self, count_common):
        assert count_common([], []) == 0

    def test_first_empty(self, count_common):
        assert count_common([], [1, 2, 3]) == 0

    def test_second_empty(self, count_common):
        assert count_common([1, 2, 3], []) == 0


# ---------------------------------------------------------------------------
# No common elements
# ---------------------------------------------------------------------------

class TestNoCommonElements:
    def test_disjoint_lists(self, count_common):
        assert count_common([1, 2, 3], [4, 5, 6]) == 0

    def test_disjoint_interleaved_values(self, count_common):
        assert count_common([1, 3, 5, 7], [2, 4, 6, 8]) == 0

    def test_disjoint_with_duplicates(self, count_common):
        assert count_common([1, 1, 2, 2], [3, 3, 4, 4]) == 0

    def test_positive_vs_negative(self, count_common):
        assert count_common([1, 2, 3], [-1, -2, -3]) == 0


# ---------------------------------------------------------------------------
# All elements in common
# ---------------------------------------------------------------------------

class TestAllElementsInCommon:
    def test_identical_lists(self, count_common):
        assert count_common([1, 2, 3, 4], [1, 2, 3, 4]) == 4

    def test_same_elements_different_order(self, count_common):
        assert count_common([1, 2, 3, 4], [4, 3, 2, 1]) == 4

    def test_single_element_both(self, count_common):
        assert count_common([7], [7]) == 1

    def test_same_list_object_passed_twice(self, count_common):
        data = [5, 6, 7]
        assert count_common(data, data) == 3

    def test_subset_first_in_second(self, count_common):
        assert count_common([2, 3], [1, 2, 3, 4, 5]) == 2

    def test_subset_second_in_first(self, count_common):
        assert count_common([1, 2, 3, 4, 5], [2, 3]) == 2


# ---------------------------------------------------------------------------
# Partial overlap
# ---------------------------------------------------------------------------

class TestPartialOverlap:
    def test_overlap_at_start(self, count_common):
        assert count_common([1, 2, 3, 4], [1, 2, 8, 9]) == 2

    def test_overlap_at_end(self, count_common):
        assert count_common([1, 2, 3, 4], [8, 9, 3, 4]) == 2

    def test_overlap_in_middle(self, count_common):
        assert count_common([1, 2, 3, 4, 5], [9, 3, 4, 10]) == 2

    def test_one_in_common_out_of_many(self, count_common):
        assert count_common(list(range(100)), [99, 200, 300]) == 1


# ---------------------------------------------------------------------------
# Duplicates: the result counts DISTINCT common values
# ---------------------------------------------------------------------------

class TestDuplicates:
    def test_duplicates_in_first_list_only(self, count_common):
        assert count_common([1, 1, 1, 2], [1, 2]) == 2

    def test_duplicates_in_second_list_only(self, count_common):
        assert count_common([1, 2], [1, 1, 1, 2, 2]) == 2

    def test_duplicates_in_both_lists(self, count_common):
        assert count_common([1, 1, 2, 2, 3], [1, 1, 1, 2, 4]) == 2

    def test_single_value_repeated_in_both(self, count_common):
        assert count_common([5, 5, 5, 5], [5, 5, 5]) == 1

    def test_repeated_value_not_counted_as_product(self, count_common):
        # A nested loop that counts every matching pair would return 3 * 4 = 12.
        # Counting distinct values must return 1.
        assert count_common([9, 9, 9], [9, 9, 9, 9]) == 1

    def test_repeated_value_not_counted_per_occurrence_in_first(self, count_common):
        assert count_common([4, 4, 4, 4], [4]) == 1

    def test_repeated_value_not_counted_per_occurrence_in_second(self, count_common):
        assert count_common([4], [4, 4, 4, 4]) == 1

    def test_duplicates_without_common_values(self, count_common):
        assert count_common([1, 1, 1], [2, 2, 2]) == 0

    def test_mixed_duplicate_and_unique_commons(self, count_common):
        assert count_common([1, 1, 2, 3, 3, 3], [3, 3, 1, 5, 5]) == 2

    def test_result_never_exceeds_distinct_size_of_either_list(self, count_common):
        a = [1, 1, 1, 2, 2]
        b = [1, 2, 3, 4, 5, 6, 7]
        assert count_common(a, b) <= len(set(a))
        assert count_common(a, b) <= len(set(b))


# ---------------------------------------------------------------------------
# Negative integers and zero
# ---------------------------------------------------------------------------

class TestNegativeAndZero:
    def test_negative_common(self, count_common):
        assert count_common([-1, -2, -3], [-3, -4, -5]) == 1

    def test_all_negative_all_common(self, count_common):
        assert count_common([-5, -4, -3], [-3, -4, -5]) == 3

    def test_all_negative_disjoint(self, count_common):
        assert count_common([-1, -2], [-3, -4]) == 0

    def test_zero_common(self, count_common):
        assert count_common([0, 1, 2], [0, 5, 6]) == 1

    def test_zero_only_in_one_list(self, count_common):
        assert count_common([0, 1, 2], [1, 2, 3]) == 2

    def test_zero_only_lists(self, count_common):
        assert count_common([0], [0]) == 1

    def test_zero_repeated(self, count_common):
        assert count_common([0, 0, 0], [0, 0]) == 1

    def test_mixed_negative_zero_positive(self, count_common):
        assert count_common([-2, -1, 0, 1, 2], [-1, 0, 1, 3]) == 3

    def test_positive_and_negative_of_same_magnitude_are_different(self, count_common):
        assert count_common([1, 2], [-1, -2]) == 0

    def test_negative_duplicates(self, count_common):
        assert count_common([-7, -7, -7], [-7, -7]) == 1

    def test_zero_not_confused_with_empty_or_falsy_handling(self, count_common):
        # Guards against implementations that treat 0 as "missing/False".
        assert count_common([0, 0], [0]) == 1
        assert count_common([0], [1]) == 0


# ---------------------------------------------------------------------------
# Boundary cases
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    def test_single_element_lists_equal(self, count_common):
        assert count_common([3], [3]) == 1

    def test_single_element_lists_different(self, count_common):
        assert count_common([3], [4]) == 0

    def test_single_element_vs_empty(self, count_common):
        assert count_common([3], []) == 0
        assert count_common([], [3]) == 0

    def test_single_element_vs_many(self, count_common):
        assert count_common([50], list(range(100))) == 1
        assert count_common([500], list(range(100))) == 0

    def test_adjacent_values_not_equal(self, count_common):
        assert count_common([1], [2]) == 0
        assert count_common([-1], [0]) == 0

    def test_large_integers(self, count_common):
        big = 10 ** 18
        assert count_common([big, big + 1], [big, big + 2]) == 1

    def test_very_large_integers_beyond_64_bit(self, count_common):
        huge = 2 ** 100
        assert count_common([huge, -huge], [huge]) == 1

    def test_large_negative_integers(self, count_common):
        assert count_common([-(10 ** 18)], [-(10 ** 18), 5]) == 1

    def test_ranges_touching_at_one_value(self, count_common):
        assert count_common(list(range(0, 11)), list(range(10, 21))) == 1

    def test_ranges_just_not_touching(self, count_common):
        assert count_common(list(range(0, 10)), list(range(10, 20))) == 0

    def test_larger_input_full_overlap(self, count_common):
        n = 1000
        assert count_common(list(range(n)), list(range(n))) == n

    def test_larger_input_half_overlap(self, count_common):
        assert count_common(list(range(1000)), list(range(500, 1500))) == 500

    def test_larger_input_with_heavy_duplication(self, count_common):
        a = [1, 2, 3] * 500
        b = [3, 4, 5] * 500
        assert count_common(a, b) == 1


# ---------------------------------------------------------------------------
# Symmetry and relationship to the reference definition
# ---------------------------------------------------------------------------

class TestMathematicalProperties:
    @pytest.mark.parametrize(
        "a, b",
        [
            ([1, 2, 3], [2, 3, 4]),
            ([1, 1, 2], [2, 2, 3]),
            ([], [1]),
            ([-1, 0, 1], [0]),
            ([5, 5], [5]),
        ],
    )
    def test_argument_order_does_not_matter(self, count_common, a, b):
        assert count_common(a, b) == count_common(b, a)

    @pytest.mark.parametrize(
        "a, b",
        [
            ([1, 2, 3], [2, 3, 4]),
            ([1, 1, 2], [2, 2, 3]),
            ([], [1]),
            ([-1, 0, 1], [0]),
            ([5, 5], [5]),
            ([1, 2, 3], [1, 2, 3]),
        ],
    )
    def test_matches_reference_definition(self, count_common, a, b):
        assert count_common(a, b) == reference_count(a, b)

    def test_result_is_non_negative(self, count_common):
        assert count_common([1, 2], [3, 4]) >= 0

    def test_self_comparison_equals_distinct_count(self, count_common):
        data = [1, 1, 2, 3, 3, 3, -4, 0, 0]
        assert count_common(data, data) == len(set(data))

    def test_order_of_elements_does_not_affect_result(self, count_common):
        a = [1, 2, 3, 4, 5]
        b = [4, 5, 6, 7]
        shuffled_a = a[:]
        random.Random(1).shuffle(shuffled_a)
        assert count_common(a, b) == count_common(shuffled_a, b)

    def test_adding_non_common_element_does_not_change_result(self, count_common):
        base = count_common([1, 2, 3], [2, 3, 4])
        assert count_common([1, 2, 3, 99], [2, 3, 4]) == base

    def test_adding_common_element_increases_result_by_one(self, count_common):
        base = count_common([1, 2, 3], [2, 3, 4])
        assert count_common([1, 2, 3, 77], [2, 3, 4, 77]) == base + 1

    def test_adding_duplicate_of_existing_common_does_not_change_result(self, count_common):
        base = count_common([1, 2, 3], [2, 3, 4])
        assert count_common([1, 2, 3, 2], [2, 3, 4, 3]) == base


# ---------------------------------------------------------------------------
# Input handling: no mutation, no aliasing side effects
# ---------------------------------------------------------------------------

class TestInputHandling:
    def test_does_not_mutate_first_list(self, count_common):
        a = [3, 1, 2, 2]
        b = [2, 3, 4]
        a_copy = a[:]
        count_common(a, b)
        assert a == a_copy

    def test_does_not_mutate_second_list(self, count_common):
        a = [3, 1, 2]
        b = [2, 3, 4, 4]
        b_copy = b[:]
        count_common(a, b)
        assert b == b_copy

    def test_repeated_calls_give_same_result(self, count_common):
        a = [1, 2, 3, 3]
        b = [3, 4, 1]
        results = {count_common(a, b) for _ in range(5)}
        assert results == {2}

    def test_does_not_mutate_when_same_object_passed_twice(self, count_common):
        data = [1, 1, 2]
        count_common(data, data)
        assert data == [1, 1, 2]


# ---------------------------------------------------------------------------
# Agreement between the nested-loop and set implementations
# ---------------------------------------------------------------------------

class TestImplementationsAgree:
    @pytest.mark.parametrize(
        "a, b",
        [
            ([], []),
            ([1], [1]),
            ([1, 1, 1], [1]),
            ([1, 2, 3], [4, 5, 6]),
            ([-1, 0, 1], [1, 0, -1]),
            ([1, 1, 2, 2, 3, 3], [3, 3, 4, 4, 5, 5]),
            (list(range(50)), list(range(25, 75))),
        ],
    )
    def test_fixed_cases_agree(self, a, b):
        assert find_common(a, b) == find_common_efficient(a, b)

    @pytest.mark.parametrize("seed", range(25))
    def test_random_lists_agree_with_each_other_and_reference(self, seed):
        rng = random.Random(seed)
        size = rng.randint(0, 60)
        # Mirrors the description: values drawn from a range based on list size.
        # The exact range formula is not specified, so a range of +/- size is
        # used here as an assumption (it includes negatives and zero).
        a = [rng.randint(-size, size) for _ in range(size)]
        b = [rng.randint(-size, size) for _ in range(size)]
        expected = reference_count(a, b)
        assert find_common(a, b) == expected
        assert find_common_efficient(a, b) == expected

    @pytest.mark.parametrize("seed", range(10))
    def test_random_lists_of_unequal_size_agree(self, seed):
        rng = random.Random(1000 + seed)
        a = [rng.randint(0, 30) for _ in range(rng.randint(0, 80))]
        b = [rng.randint(0, 30) for _ in range(rng.randint(0, 80))]
        expected = reference_count(a, b)
        assert find_common(a, b) == expected
        assert find_common_efficient(a, b) == expected

    @pytest.mark.parametrize("seed", range(10))
    def test_random_lists_with_heavy_duplicates_agree(self, seed):
        # Small value range relative to list length forces many duplicates.
        rng = random.Random(2000 + seed)
        a = [rng.randint(0, 5) for _ in range(100)]
        b = [rng.randint(0, 5) for _ in range(100)]
        expected = reference_count(a, b)
        assert find_common(a, b) == expected
        assert find_common_efficient(a, b) == expected


# ---------------------------------------------------------------------------
# Unusual and invalid inputs
# The description specifies NO behavior for these. Per assumption 4, the tests
# only require the two implementations to behave consistently (both raise, or
# both return equal values) and do not assert a specific exception type.
# ---------------------------------------------------------------------------

def _outcome(func, a, b):
    try:
        return ("value", func(a, b))
    except Exception as exc:  # noqa: BLE001 - intentionally broad, see note above
        return ("raised", type(exc).__name__)


class TestUnusualAndInvalidInputs:
    @pytest.mark.parametrize(
        "a, b",
        [
            (None, [1, 2]),
            ([1, 2], None),
            (None, None),
            (5, [1, 2]),
            ([1, 2], 5),
        ],
    )
    def test_non_list_arguments_handled_consistently(self, a, b):
        nested = _outcome(find_common, a, b)
        sets = _outcome(find_common_efficient, a, b)
        # Both should reject invalid arguments. Exact exception type is unspecified.
        assert nested[0] == "raised"
        assert sets[0] == "raised"

    @pytest.mark.parametrize(
        "a, b",
        [
            ([1, "a", 3], [3, "a"]),
            ([1.5, 2.5], [1.5]),
            ([None, 1], [None]),
            ([[1], [2]], [[1]]),
        ],
    )
    def test_non_integer_elements_handled_consistently(self, a, b):
        # Unspecified behavior: only check the two implementations don't disagree
        # about whether the input is accepted. If both accept it, results must match.
        nested = _outcome(find_common, a, b)
        sets = _outcome(find_common_efficient, a, b)
        assert nested[0] == sets[0]
        if nested[0] == "value":
            assert nested[1] == sets[1]

    def test_booleans_are_treated_like_integers_if_accepted(self):
        # ASSUMPTION: bool is a subclass of int in Python, so True == 1 and
        # False == 0. If the functions accept bools, both must agree.
        nested = _outcome(find_common, [True, False], [1, 0])
        sets = _outcome(find_common_efficient, [True, False], [1, 0])
        assert nested == sets
        if nested[0] == "value":
            assert nested[1] == 2

    def test_tuple_inputs_handled_consistently(self):
        # Unspecified whether non-list sequences are supported.
        nested = _outcome(find_common, (1, 2, 3), (2, 3, 4))
        sets = _outcome(find_common_efficient, (1, 2, 3), (2, 3, 4))
        assert nested == sets
        if nested[0] == "value":
            assert nested[1] == 2
