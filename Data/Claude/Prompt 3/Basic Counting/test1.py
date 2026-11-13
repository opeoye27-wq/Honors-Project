"""
Unit tests (pytest) for functions that count the common elements of two
lists of integers.

ASSUMPTIONS (the description leaves these open, so they are explicit and
configurable below):

1. MODULE_NAME / FUNCTION_NAMES: the real module and function names were not
   given. Edit them to match your program. Every function listed is run
   through the same test suite, and each takes (list_a, list_b) and returns
   an int.

2. SEMANTICS: "common elements" is ambiguous when lists contain duplicates.
     - "distinct": count of distinct values present in both lists
                   (size of the set intersection).
     - "multiset": for each value, min(count in a, count in b), summed.
   Set SEMANTICS to whichever matches the intended behavior. Cases without
   duplicates give the same answer under both.

3. Invalid input: None or a non-iterable argument raises TypeError.

4. No type coercion: the string "1" is not considered equal to the integer 1.

5. The inputs are never modified, and the result is symmetric
   (f(a, b) == f(b, a)).
"""

import importlib

import pytest

# ----------------------------------------------------------------------------
# Configuration: adjust to match the program under test
# ----------------------------------------------------------------------------
MODULE_NAME = "basic_counting"
FUNCTION_NAMES = ["find_common"]
SEMANTICS = "distinct"  # "distinct" or "multiset"

assert SEMANTICS in ("distinct", "multiset")


@pytest.fixture(params=FUNCTION_NAMES)
def func(request):
    module = importlib.import_module(MODULE_NAME)
    return getattr(module, request.param)


def expected(distinct, multiset):
    return distinct if SEMANTICS == "distinct" else multiset


# (list_a, list_b, expected_if_distinct, expected_if_multiset, id)
CASES = [
    # --- Normal cases ---
    ([1, 2, 3], [2, 3, 4], 2, 2, "partial_overlap"),
    ([1, 2, 3], [4, 5, 6], 0, 0, "no_overlap"),
    ([1, 2, 3], [1, 2, 3], 3, 3, "identical_lists"),
    ([1, 2, 3, 4], [4], 1, 1, "single_common_at_end"),
    ([3, 1, 2], [2, 3, 1], 3, 3, "same_elements_different_order"),
    ([1, 2, 3], [1, 2, 3, 4, 5, 6], 3, 3, "a_subset_of_b"),
    ([1, 2, 3, 4, 5, 6], [2, 4], 2, 2, "b_subset_of_a"),
    # --- Empty lists ---
    ([], [], 0, 0, "both_empty"),
    ([], [1, 2], 0, 0, "first_empty"),
    ([1, 2], [], 0, 0, "second_empty"),
    # --- Single elements ---
    ([5], [5], 1, 1, "single_equal"),
    ([5], [6], 0, 0, "single_different"),
    # --- Negatives, zero, large values ---
    ([-1, -2, 3], [-2, 3, 4], 2, 2, "negatives_overlap"),
    ([-1], [1], 0, 0, "negative_vs_positive"),
    ([0, 1], [0, 2], 1, 1, "zero_common"),
    ([2**63, 2**64], [2**64, -(2**63)], 1, 1, "very_large_ints"),
    ([-5, -4, -3], [-3, -4, -5], 3, 3, "all_negative_reordered"),
    # --- Duplicates (semantics-dependent) ---
    ([1, 1, 1], [1], 1, 1, "dups_in_a_single_in_b"),
    ([1], [1, 1, 1], 1, 1, "single_in_a_dups_in_b"),
    ([1, 1, 1], [1, 1], 1, 2, "dups_unequal_counts"),
    ([7, 7, 7], [7, 7, 7], 1, 3, "dups_equal_counts"),
    ([1, 1, 2, 2], [1, 2, 2, 2], 2, 3, "mixed_dup_counts"),
    ([1, 1, 1], [2, 2, 2], 0, 0, "dups_but_no_overlap"),
    ([0, 0], [0], 1, 1, "zero_duplicates"),
]


@pytest.mark.parametrize(
    "a, b, exp_distinct, exp_multiset",
    [c[:4] for c in CASES],
    ids=[c[4] for c in CASES],
)
def test_count_common(func, a, b, exp_distinct, exp_multiset):
    assert func(a, b) == expected(exp_distinct, exp_multiset)


@pytest.mark.parametrize(
    "a, b, exp_distinct, exp_multiset",
    [c[:4] for c in CASES],
    ids=[c[4] for c in CASES],
)
def test_symmetry(func, a, b, exp_distinct, exp_multiset):
    assert func(a, b) == func(b, a)


@pytest.mark.parametrize(
    "a, b",
    [c[:2] for c in CASES],
    ids=[c[4] for c in CASES],
)
def test_inputs_not_modified(func, a, b):
    a_copy, b_copy = list(a), list(b)
    func(a, b)
    assert a == a_copy
    assert b == b_copy


def test_result_is_non_negative_int(func):
    result = func([1, 2, 3], [3, 4, 5])
    assert isinstance(result, int)
    assert not isinstance(result, bool)
    assert result >= 0


def test_result_bounded_by_shorter_list(func):
    a, b = [1, 2, 3, 4, 5], [1, 2]
    assert func(a, b) <= min(len(a), len(b))


def test_same_list_object_passed_twice(func):
    lst = [1, 2, 3, 3]
    assert func(lst, lst) == expected(3, 4)


def test_repeated_calls_are_deterministic(func):
    a, b = [1, 2, 2, 3], [2, 3, 3, 4]
    first = func(a, b)
    assert all(func(a, b) == first for _ in range(5))


def test_list_with_one_unique_value_repeated_many_times(func):
    a, b = [1] * 1000, [1] * 500
    assert func(a, b) == expected(1, 500)


def test_large_lists_partial_overlap(func):
    a = list(range(0, 100_000))
    b = list(range(50_000, 150_000))
    assert func(a, b) == 50_000


def test_large_lists_no_overlap(func):
    a = list(range(0, 50_000))
    b = list(range(50_000, 100_000))
    assert func(a, b) == 0


def test_large_lists_fully_identical(func):
    a = list(range(100_000))
    assert func(a, list(a)) == 100_000


# ----------------------------------------------------------------------------
# Unusual and invalid inputs (see assumptions 3 and 4)
# ----------------------------------------------------------------------------
def test_string_elements_are_not_coerced_to_ints(func):
    assert func([1, 2], ["1", "2"]) == 0


@pytest.mark.parametrize(
    "a, b",
    [
        (None, [1, 2]),
        ([1, 2], None),
        (None, None),
        (5, [1, 2]),
        ([1, 2], 5),
    ],
    ids=["a_none", "b_none", "both_none", "a_int", "b_int"],
)
def test_invalid_arguments_raise_type_error(func, a, b):
    with pytest.raises(TypeError):
        func(a, b)


def test_missing_argument_raises_type_error(func):
    with pytest.raises(TypeError):
        func([1, 2, 3])
