"""
pytest unit tests: counting common elements between two lists of integers.

ASSUMPTIONS (the description leaves these open, so they are explicit and configurable):

1. Module and function names are not given. Edit MODULE_NAME and FUNCTION_NAMES below.
   Every test runs against every listed function, and all must satisfy the same contract.
   Each function takes (list_a, list_b) and returns an int.

2. Duplicate handling is ambiguous. Set DUPLICATE_SEMANTICS to:
     "distinct": counts distinct values present in both lists (set-intersection size).
     "multiset": counts with multiplicity, i.e. sum of min(count_a, count_b) per value.
   Tests with no duplicates are unaffected by this setting.

3. The result is symmetric: f(a, b) == f(b, a).

4. Invalid containers (None, a bare int) raise TypeError or ValueError
   (see EXPECTED_INVALID_EXCEPTIONS).

5. NOT tested because the description does not define the behavior: strings, floats, bools,
   or unhashable elements inside the lists, and tuples or other iterables in place of lists.
"""
import importlib
import sys

import pytest

# ----------------------------- configuration -----------------------------
MODULE_NAME = "basic_counting"                   # <-- change to your module name
FUNCTION_NAMES = ["find_common"]        # <-- change/add your function names
DUPLICATE_SEMANTICS = "distinct"                  # "distinct" or "multiset"
EXPECTED_INVALID_EXCEPTIONS = (TypeError, ValueError)
# --------------------------------------------------------------------------

assert DUPLICATE_SEMANTICS in ("distinct", "multiset")

_module = importlib.import_module(MODULE_NAME)
_FUNCS = [getattr(_module, name) for name in FUNCTION_NAMES]


@pytest.fixture(params=_FUNCS, ids=FUNCTION_NAMES)
def count_common(request):
    return request.param


# ------------------------------ normal cases ------------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([1, 2, 3], [2, 3, 4], 2),                 # partial overlap
        ([1, 2, 3], [4, 5, 6], 0),                 # no overlap
        ([1, 2, 3], [1, 2, 3], 3),                 # identical lists
        ([1, 2, 3, 4, 5], [3], 1),                 # one element in common
        ([3, 1, 2], [2, 3, 1], 3),                 # same elements, different order
        ([5, 1, 9, 3], [3, 9, 7, 8, 1], 3),        # unsorted inputs
        ([1, 2], [1, 2, 3, 4], 2),                 # first is subset of second
        ([1, 2, 3, 4], [1, 2], 2),                 # second is subset of first
        ([1, 3, 5, 7], [2, 4, 6, 8], 0),           # interleaved, disjoint
        ([10, 20, 30], [30, 20, 10, 40], 3),       # reversed order plus extra
    ],
)
def test_normal_cases(count_common, a, b, expected):
    assert count_common(a, b) == expected


# ------------------------------ empty inputs ------------------------------
@pytest.mark.parametrize(
    "a, b",
    [([], []), ([1, 2, 3], []), ([], [1, 2, 3]), ([0], []), ([], [0])],
)
def test_empty_inputs_return_zero(count_common, a, b):
    assert count_common(a, b) == 0


# --------------------------- single-element lists --------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [([7], [7], 1), ([7], [8], 0), ([0], [0], 1), ([-5], [-5], 1), ([-5], [5], 0)],
)
def test_single_element_lists(count_common, a, b, expected):
    assert count_common(a, b) == expected


# ------------------- negatives, zero, and integer extremes -------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([-1, -2, -3], [-3, 0, 3], 1),             # one negative match
        ([-1, -2, -3], [-1, -2, -3], 3),           # all negative, identical
        ([-1], [1], 0),                            # sign matters
        ([-3, -2, -1, 0, 1, 2, 3], [0], 1),        # zero in the middle
        ([0, 1], [0, -0], 1),                      # -0 is 0 for ints
        ([sys.maxsize, 1], [sys.maxsize, 2], 1),   # 64-bit max
        ([-sys.maxsize - 1, 1], [-sys.maxsize - 1, 2], 1),  # 64-bit min
        ([sys.maxsize], [-sys.maxsize - 1], 0),    # opposite extremes
        ([2**70, 1], [2**70, 2], 1),               # beyond 64-bit
        ([10**100], [10**100], 1),                 # very large int
        ([10**100], [10**100 + 1], 0),             # off by one at large magnitude
    ],
)
def test_negative_zero_and_large_integers(count_common, a, b, expected):
    assert count_common(a, b) == expected


# ------------------------------- duplicates -------------------------------
# Columns: a, b, expected under "distinct", expected under "multiset".
_DUPLICATE_CASES = [
    ([1, 1, 1], [1], 1, 1),
    ([1], [1, 1, 1], 1, 1),
    ([1, 1, 1], [1, 1], 1, 2),
    ([1, 1, 1], [1, 1, 1], 1, 3),
    ([1, 1, 2], [1, 2, 2], 2, 2),
    ([2, 2, 3, 3], [2, 3, 3, 3], 2, 3),
    ([5, 5, 5, 5], [6, 6], 0, 0),                  # duplicates, no overlap
    ([4, 4, 4], [4, 4, 4, 4, 4], 1, 3),
    ([1, 2, 2, 3], [1, 2, 2, 3], 3, 4),            # identical lists with a duplicate
    ([0, 0], [0, 0, 0], 1, 2),                     # duplicated zeros
    ([-1, -1, -1], [-1, -1], 1, 2),                # duplicated negatives
]


@pytest.mark.parametrize("a, b, distinct, multiset", _DUPLICATE_CASES)
def test_duplicates(count_common, a, b, distinct, multiset):
    expected = distinct if DUPLICATE_SEMANTICS == "distinct" else multiset
    assert count_common(a, b) == expected


@pytest.mark.parametrize("a, b, distinct, multiset", _DUPLICATE_CASES)
def test_duplicates_symmetric(count_common, a, b, distinct, multiset):
    assert count_common(a, b) == count_common(b, a)


# ------------------------ same object passed twice ------------------------
def test_same_list_object_for_both_arguments(count_common):
    data = [1, 2, 2, 3]
    expected = 3 if DUPLICATE_SEMANTICS == "distinct" else 4
    assert count_common(data, data) == expected


def test_same_list_object_without_duplicates(count_common):
    data = [4, 5, 6, 7]
    assert count_common(data, data) == 4


# --------------------------- general properties ---------------------------
@pytest.mark.parametrize(
    "a, b",
    [
        ([1, 2, 3], [2, 3, 4]),
        ([], [1]),
        ([-1, 0, 1], [1, 0, -1]),
        ([9], [8]),
        ([1, 1, 2], [2, 2, 1]),
    ],
)
def test_symmetry(count_common, a, b):
    assert count_common(a, b) == count_common(b, a)


@pytest.mark.parametrize(
    "a, b",
    [([1, 2, 3], [2, 3, 4]), ([], []), ([1, 1], [1]), ([-1], [-1])],
)
def test_return_type_is_nonnegative_int(count_common, a, b):
    result = count_common(a, b)
    assert isinstance(result, int)
    assert not isinstance(result, bool)
    assert result >= 0


def test_result_never_exceeds_shorter_list_length(count_common):
    a, b = [1, 1, 1, 2, 3], [1, 1, 1, 1, 1, 1, 2, 3, 4]
    assert count_common(a, b) <= min(len(a), len(b))


def test_inputs_are_not_mutated(count_common):
    a, b = [3, 1, 2, 2, -1], [2, 5, 3, 3, 0]
    a_copy, b_copy = list(a), list(b)
    count_common(a, b)
    assert a == a_copy
    assert b == b_copy


def test_repeated_calls_give_same_result(count_common):
    a, b = [1, 2, 3, 3], [3, 4, 1]
    first = count_common(a, b)
    assert count_common(a, b) == first
    assert count_common(a, b) == first


def test_no_state_leaks_between_calls(count_common):
    assert count_common([1, 2, 3], [1, 2, 3]) == 3
    assert count_common([4], [5]) == 0
    assert count_common([], []) == 0
    assert count_common([1, 2, 3], [3]) == 1


# ------------------------------- larger inputs -------------------------------
def test_large_partial_overlap(count_common):
    n = 10_000
    a = list(range(n))                       # 0 .. 9999
    b = list(range(n // 2, n + n // 2))      # 5000 .. 14999
    assert count_common(a, b) == n // 2      # 5000..9999 are common


def test_large_disjoint_lists(count_common):
    a = list(range(0, 10_000))
    b = list(range(10_000, 20_000))
    assert count_common(a, b) == 0


def test_large_identical_lists(count_common):
    a = list(range(10_000))
    assert count_common(a, list(a)) == 10_000


def test_large_list_with_small_list(count_common):
    big = list(range(10_000))
    assert count_common(big, [0, 9_999, 10_000, -1]) == 2
    assert count_common([0, 9_999, 10_000, -1], big) == 2


def test_large_all_duplicates(count_common):
    a = [7] * 5_000
    b = [7] * 3_000
    expected = 1 if DUPLICATE_SEMANTICS == "distinct" else 3_000
    assert count_common(a, b) == expected


# ------------------------------ invalid inputs ------------------------------
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
def test_invalid_container_types_raise(count_common, a, b):
    with pytest.raises(EXPECTED_INVALID_EXCEPTIONS):
        count_common(a, b)


def test_missing_arguments_raise_type_error(count_common):
    with pytest.raises(TypeError):
        count_common()
    with pytest.raises(TypeError):
        count_common([1, 2, 3])


def test_too_many_arguments_raise_type_error(count_common):
    with pytest.raises(TypeError):
        count_common([1], [1], [1])


# ------------------- cross-function consistency (if several) -------------------
@pytest.mark.skipif(len(_FUNCS) < 2, reason="needs at least two functions to compare")
@pytest.mark.parametrize(
    "a, b",
    [
        ([1, 2, 3], [2, 3, 4]),
        ([], []),
        ([1, 1, 2, 2], [2, 2, 2, 1]),
        ([-5, 0, 5], [5, 0, -5, 10]),
        (list(range(500)), list(range(250, 750))),
    ],
)
def test_all_functions_agree(a, b):
    results = [f(a, b) for f in _FUNCS]
    assert len(set(results)) == 1, f"functions disagree: {dict(zip(FUNCTION_NAMES, results))}"
