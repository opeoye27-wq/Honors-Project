
import pytest
from basic_counting import find_common

# Assumption: Common elements are counted based on unique values,
# and duplicate occurrences in either list are counted only once.
# If the intended behavior counts duplicate occurrences, some expected
# results below should be adjusted.


def test_identical_lists():
    assert find_common([1, 2, 3], [1, 2, 3]) == 3


def test_no_common_elements():
    assert find_common([1, 2, 3], [4, 5, 6]) == 0


def test_one_common_element():
    assert find_common([1, 2, 3], [3, 4, 5]) == 1


def test_multiple_common_elements():
    assert find_common([1, 2, 3, 4], [2, 4, 6, 8]) == 2


def test_empty_first_list():
    assert find_common([], [1, 2, 3]) == 0


def test_empty_second_list():
    assert find_common([1, 2, 3], []) == 0


def test_both_lists_empty():
    assert find_common([], []) == 0


def test_single_element_matching_lists():
    assert find_common([5], [5]) == 1


def test_single_element_nonmatching_lists():
    assert find_common([5], [10]) == 0


def test_negative_numbers():
    assert find_common([-1, -2, -3], [-2, -3, -4]) == 2


def test_zero_as_common_element():
    assert find_common([0, 1, 2], [0, 3, 4]) == 1


def test_large_integer_values():
    assert find_common(
        [10**100, 10**200, 3],
        [10**200, 10**300, 4]
    ) == 1


def test_duplicate_elements_in_first_list():
    assert find_common([1, 1, 1, 2], [1, 2, 3]) == 2


def test_duplicate_elements_in_second_list():
    assert find_common([1, 2, 3], [1, 1, 1, 2]) == 2


def test_duplicates_in_both_lists():
    assert find_common([1, 1, 2, 2], [1, 1, 2, 2]) == 2


def test_all_elements_identical():
    assert find_common([7, 7, 7], [7, 7, 7]) == 1


def test_different_list_lengths():
    assert find_common([1, 2], [1, 2, 3, 4, 5, 6]) == 2


def test_reversed_lists():
    assert find_common([1, 2, 3, 4], [4, 3, 2, 1]) == 4


def test_common_elements_at_different_positions():
    assert find_common([10, 20, 30, 40], [40, 10, 50, 30]) == 3


def test_large_lists():
    list1 = list(range(1000))
    list2 = list(range(500, 1500))
    assert find_common(list1, list2) == 500


def test_no_overlap_with_negative_and_positive_numbers():
    assert find_common([-5, -4, -3], [1, 2, 3]) == 0


def test_repeated_zero():
    assert find_common([0, 0, 0], [0, 0]) == 1


@pytest.mark.parametrize(
    "list1, list2, expected",
    [
        ([1, 2, 3], [1, 2, 3], 3),
        ([1, 2, 3], [3, 2, 1], 3),
        ([1, 2, 3], [4, 5, 6], 0),
        ([-1, -2], [-2, -3], 1),
        ([0], [0], 1),
        ([1, 1, 2], [1, 2, 2], 2),
        ([], [], 0),
        ([], [1], 0),
        ([100], [100, 200, 300], 1),
    ]
)
def test_various_inputs(list1, list2, expected):
    assert find_common(list1, list2) == expected


# Invalid input tests.
# Assumption: The functions accept only lists of integers.
# The description does not specify whether invalid inputs should raise
# TypeError or ValueError, so these tests require rejection via either.

@pytest.mark.parametrize(
    "list1, list2",
    [
        (None, [1, 2]),
        ([1, 2], None),
        (None, None),
        ("123", [1, 2]),
        ([1, 2], "123"),
        (123, [1, 2]),
        ([1, 2], 123),
        ([1.5, 2.5], [1, 2]),
        ([1, 2], [1.5, 2.5]),
        ([[1], [2]], [1, 2]),
        ([1, 2], [[1], [2]]),
        ([None, 1], [1, 2]),
        ([1, 2], [None, 1]),
    ]
)
def test_invalid_inputs(list1, list2):
    with pytest.raises((TypeError, ValueError)):
        find_common(list1, list2)
