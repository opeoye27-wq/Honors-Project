"""
Pytest unit tests for functions that count the common elements between two
lists of integers.

ASSUMPTIONS (the description does not specify these, so they are made explicit):

A1. Module and function names. The tests import from a module named
    `basic_counting`. Every function that should satisfy the contract is
    listed in FUNCTION_NAMES. Edit MODULE_NAME / FUNCTION_NAMES to match the
    real program; every test runs against every listed function.

A2. Signature. Each function is called as f(list1, list2) and returns an int.

A3. Duplicates. The description does not say how repeated values are counted.
    Set DUPLICATE_MODE to choose the interpretation tested:
      - "distinct": the number of distinct values present in both lists.
                    [1, 1] vs [1, 1] -> 1
      - "multiset": the multiset intersection size, i.e. sum of
                    min(count_in_a, count_in_b) per value.
                    [1, 1] vs [1, 1] -> 2
    Tests that give the same answer under both interpretations always run.
    Tests whose answer differs are selected by DUPLICATE_MODE.

A4. Invalid inputs. None or a non-iterable (e.g. an int) in place of a list
    is expected to raise TypeError.

A5. Non-integer elements are out of the stated domain. The behavior is
    ambiguous (raise or compare normally), so the only requirement tested
    is that a string such as "1" is never counted as equal to the integer 1.
    Either raising (TypeError/ValueError) or returning 0 is accepted.

A6. Inputs are not mutated, and the functions are pure (same input gives the
    same output).
"""

import importlib
from collections import Counter

import pytest

# ----------------------------------------------------------------------------
# Configuration (see assumptions A1 and A3)
# ----------------------------------------------------------------------------
MODULE_NAME = "basic_counting"
FUNCTION_NAMES = ["find_common"]
DUPLICATE_MODE = "distinct"  # "distinct" or "multiset"


@pytest.fixture(params=FUNCTION_NAMES)
def count_common(request):
    module = importlib.import_module(MODULE_NAME)
    return getattr(module, request.param)


def expected_count(a, b):
    """Independent reference oracle that follows DUPLICATE_MODE."""
    if DUPLICATE_MODE == "distinct":
        return len(set(a) & set(b))
    if DUPLICATE_MODE == "multiset":
        return sum((Counter(a) & Counter(b)).values())
    raise ValueError("DUPLICATE_MODE must be 'distinct' or 'multiset'")


# ----------------------------------------------------------------------------
# Normal cases
# ----------------------------------------------------------------------------
class TestNormalCases:
    def test_partial_overlap(self, count_common):
        assert count_common([1, 2, 3, 4], [3, 4, 5, 6]) == 2

    def test_single_common_element(self, count_common):
        assert count_common([1, 2, 3], [3, 4, 5]) == 1

    def test_no_common_elements(self, count_common):
        assert count_common([1, 2, 3], [4, 5, 6]) == 0

    def test_identical_lists(self, count_common):
        assert count_common([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == 5

    def test_first_is_subset_of_second(self, count_common):
        assert count_common([2, 3], [1, 2, 3, 4, 5]) == 2

    def test_second_is_subset_of_first(self, count_common):
        assert count_common([1, 2, 3, 4, 5], [2, 3]) == 2

    def test_unsorted_lists(self, count_common):
        assert count_common([9, 1, 7, 3], [3, 8, 9, 2]) == 2

    def test_same_elements_different_order(self, count_common):
        assert count_common([1, 2, 3, 4], [4, 3, 2, 1]) == 4

    def test_returns_int(self, count_common):
        result = count_common([1, 2], [2, 3])
        assert isinstance(result, int)
        assert not isinstance(result, bool)


# ----------------------------------------------------------------------------
# Edge cases: empty and tiny inputs
# ----------------------------------------------------------------------------
class TestEmptyAndTinyInputs:
    def test_both_empty(self, count_common):
        assert count_common([], []) == 0

    def test_first_empty(self, count_common):
        assert count_common([], [1, 2, 3]) == 0

    def test_second_empty(self, count_common):
        assert count_common([1, 2, 3], []) == 0

    def test_single_elements_equal(self, count_common):
        assert count_common([5], [5]) == 1

    def test_single_elements_different(self, count_common):
        assert count_common([5], [6]) == 0

    def test_single_element_in_longer_list(self, count_common):
        assert count_common([3], [1, 2, 3, 4]) == 1

    def test_single_element_absent_from_longer_list(self, count_common):
        assert count_common([9], [1, 2, 3, 4]) == 0


# ----------------------------------------------------------------------------
# Edge cases: value ranges
# ----------------------------------------------------------------------------
class TestValueRanges:
    def test_zero_is_a_valid_common_element(self, count_common):
        assert count_common([0, 1], [0, 2]) == 1

    def test_zero_not_confused_with_empty_or_falsy(self, count_common):
        assert count_common([0], [1]) == 0
        assert count_common([0], [0]) == 1

    def test_negative_numbers(self, count_common):
        assert count_common([-1, -2, -3], [-3, -4, -1]) == 2

    def test_negative_and_positive_of_same_magnitude_are_different(self, count_common):
        assert count_common([1, 2, 3], [-1, -2, -3]) == 0

    def test_mixed_signs_and_zero(self, count_common):
        assert count_common([-5, 0, 5], [5, 0, -5]) == 3

    def test_very_large_integers(self, count_common):
        big = 10**18
        assert count_common([big, big + 1], [big + 1, big + 2]) == 1

    def test_very_large_negative_integers(self, count_common):
        big = -(10**18)
        assert count_common([big, big - 1], [big, big - 2]) == 1

    def test_integers_beyond_64_bit(self, count_common):
        huge = 2**200
        assert count_common([huge], [huge]) == 1
        assert count_common([huge], [huge + 1]) == 0

    def test_adjacent_integers_not_confused(self, count_common):
        assert count_common([1, 3, 5], [2, 4, 6]) == 0


# ----------------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------------
class TestProperties:
    @pytest.mark.parametrize(
        "a, b",
        [
            ([1, 2, 3], [2, 3, 4]),
            ([], [1]),
            ([1, 1, 2], [1, 2, 2, 3]),
            ([-1, 0, 1], [1, 0, -1, 7]),
        ],
    )
    def test_symmetry(self, count_common, a, b):
        assert count_common(a, b) == count_common(b, a)

    def test_count_never_exceeds_shorter_list_length(self, count_common):
        a = [1, 2, 3]
        b = [1, 2, 3, 4, 5, 6, 7]
        assert count_common(a, b) <= min(len(a), len(b))

    def test_count_is_non_negative(self, count_common):
        assert count_common([1, 2], [3, 4]) >= 0

    def test_order_independence_within_each_list(self, count_common):
        a, b = [4, 1, 3, 2], [2, 5, 3, 9]
        assert count_common(a, b) == count_common(sorted(a), sorted(b))
        assert count_common(a, b) == count_common(a[::-1], b[::-1])

    def test_deterministic_across_repeated_calls(self, count_common):
        a, b = [1, 2, 3, 3], [3, 4, 1]
        results = {count_common(a, b) for _ in range(5)}
        assert len(results) == 1

    def test_self_comparison_of_unique_list_equals_its_length(self, count_common):
        a = [10, 20, 30, 40]
        assert count_common(a, a) == len(a)

    def test_same_object_passed_twice(self, count_common):
        a = [1, 2, 3]
        assert count_common(a, a) == 3

    def test_matches_reference_oracle_on_varied_inputs(self, count_common):
        cases = [
            ([], []),
            ([1], [1]),
            ([1, 2, 3], [3, 2, 1]),
            ([1, 1, 2, 2], [2, 2, 3, 3]),
            ([5, 5, 5], [5]),
            ([0, -1, 1], [1, 1, 0]),
            (list(range(20)), list(range(10, 30))),
        ]
        for a, b in cases:
            assert count_common(a, b) == expected_count(a, b), (a, b)


# ----------------------------------------------------------------------------
# Duplicates (see assumption A3)
# ----------------------------------------------------------------------------
class TestDuplicatesInterpretationIndependent:
    """Duplicate scenarios whose answer is the same under both interpretations."""

    def test_duplicates_with_no_overlap(self, count_common):
        assert count_common([1, 1, 1], [2, 2, 2]) == 0

    def test_duplicates_only_in_one_list_single_match(self, count_common):
        assert count_common([1, 1, 1], [1]) == 1

    def test_duplicate_in_second_list_only_single_match(self, count_common):
        assert count_common([1], [1, 1, 1]) == 1

    def test_duplicates_mixed_with_uniques(self, count_common):
        # 1 appears twice in a and once in b; 2 appears once in each.
        # distinct -> 2, multiset -> min(2,1) + min(1,1) = 2
        assert count_common([1, 1, 2], [1, 2, 3]) == 2

    def test_all_duplicate_lists_of_different_values(self, count_common):
        assert count_common([4, 4, 4, 4], [5, 5, 5, 5]) == 0


class TestDuplicatesInterpretationDependent:
    """Duplicate scenarios whose answer depends on DUPLICATE_MODE."""

    @pytest.mark.parametrize(
        "a, b, distinct, multiset",
        [
            ([1, 1], [1, 1], 1, 2),
            ([1, 1, 1], [1, 1], 1, 2),
            ([2, 2, 3], [2, 2, 2, 3], 2, 3),
            ([7, 7, 7, 7], [7, 7, 7, 7], 1, 4),
            ([1, 1, 2, 2], [1, 2, 2, 2], 2, 3),
        ],
    )
    def test_duplicate_handling(self, count_common, a, b, distinct, multiset):
        expected = distinct if DUPLICATE_MODE == "distinct" else multiset
        assert count_common(a, b) == expected

    def test_duplicate_count_is_not_a_pairwise_product(self, count_common):
        # A naive nested loop would give 3 * 3 = 9 for this input.
        result = count_common([1, 1, 1], [1, 1, 1])
        assert result in (1, 3)
        assert result == (1 if DUPLICATE_MODE == "distinct" else 3)


# ----------------------------------------------------------------------------
# Non-mutation (see assumption A6)
# ----------------------------------------------------------------------------
class TestNoMutation:
    def test_inputs_are_not_modified(self, count_common):
        a = [3, 1, 2, 2]
        b = [2, 5, 3, 3]
        a_copy, b_copy = list(a), list(b)
        count_common(a, b)
        assert a == a_copy
        assert b == b_copy

    def test_inputs_are_not_sorted_in_place(self, count_common):
        a = [9, 8, 7]
        b = [7, 6, 5]
        count_common(a, b)
        assert a == [9, 8, 7]
        assert b == [7, 6, 5]

    def test_inputs_are_not_emptied(self, count_common):
        a = [1, 2, 3]
        b = [3, 2, 1]
        count_common(a, b)
        assert len(a) == 3
        assert len(b) == 3


# ----------------------------------------------------------------------------
# Larger inputs
# ----------------------------------------------------------------------------
class TestLargeInputs:
    def test_large_lists_with_known_overlap(self, count_common):
        a = list(range(0, 100_000))
        b = list(range(50_000, 150_000))
        assert count_common(a, b) == 50_000

    def test_large_lists_with_no_overlap(self, count_common):
        a = list(range(0, 50_000))
        b = list(range(50_000, 100_000))
        assert count_common(a, b) == 0

    def test_large_identical_lists(self, count_common):
        a = list(range(30_000))
        assert count_common(a, list(a)) == 30_000

    def test_large_list_against_single_element(self, count_common):
        a = list(range(100_000))
        assert count_common(a, [99_999]) == 1
        assert count_common(a, [100_000]) == 0

    def test_large_list_of_one_repeated_value(self, count_common):
        a = [1] * 10_000
        b = [1] * 10_000
        expected = 1 if DUPLICATE_MODE == "distinct" else 10_000
        assert count_common(a, b) == expected


# ----------------------------------------------------------------------------
# Invalid inputs (see assumptions A4 and A5)
# ----------------------------------------------------------------------------
class TestInvalidInputs:
    def test_none_as_first_argument(self, count_common):
        with pytest.raises(TypeError):
            count_common(None, [1, 2, 3])

    def test_none_as_second_argument(self, count_common):
        with pytest.raises(TypeError):
            count_common([1, 2, 3], None)

    def test_none_for_both_arguments(self, count_common):
        with pytest.raises(TypeError):
            count_common(None, None)

    def test_integer_instead_of_list_first_argument(self, count_common):
        with pytest.raises(TypeError):
            count_common(5, [1, 2, 3])

    def test_integer_instead_of_list_second_argument(self, count_common):
        with pytest.raises(TypeError):
            count_common([1, 2, 3], 5)

    def test_missing_second_argument(self, count_common):
        with pytest.raises(TypeError):
            count_common([1, 2, 3])

    def test_no_arguments(self, count_common):
        with pytest.raises(TypeError):
            count_common()

    def test_too_many_arguments(self, count_common):
        with pytest.raises(TypeError):
            count_common([1], [1], [1])

    def test_string_elements_never_match_equal_looking_integers(self, count_common):
        # A5: either raising or returning 0 is acceptable, but "1" must never
        # be counted as equal to 1.
        try:
            result = count_common([1, 2, 3], ["1", "2", "3"])
        except (TypeError, ValueError):
            return
        assert result == 0

    def test_string_in_one_list_does_not_affect_integer_matches(self, count_common):
        # A5: either raising is acceptable, or the string is ignored.
        try:
            result = count_common([1, "1", 2], [1, 2])
        except (TypeError, ValueError):
            return
        assert result == 2