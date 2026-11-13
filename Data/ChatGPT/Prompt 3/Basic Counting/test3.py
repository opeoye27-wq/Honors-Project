
import pytest
from basic_counting import find_common

# Assumption: Common elements are counted by unique value.
# Duplicate occurrences do not increase the count.
# Assumption: Invalid inputs should raise TypeError or ValueError.


def test_identical_lists():
    assert find_common([1, 2, 3], [1, 2, 3]) == 3


def test_no_common_elements():
    assert find_common([1, 2, 3], [4, 5, 6]) == 0


def test_one_common_element():
    assert find_common([1, 2, 3], [3, 4, 5]) == 1


def test_multiple_common_elements():
    assert find_common([1, 2, 3, 4], [2, 4, 6, 8]) == 2


def test_empty_lists():
    assert find_common([], []) == 0


def test_first_list_empty():
    assert find_common([], [1, 2, 3]) == 0


def test_second_list_empty():
    assert find_common([1, 2, 3], []) == 0


def test_single_matching_element():
    assert find_common([5], [5]) == 1


def test_single_nonmatching_element():
    assert find_common([5], [10]) == 0


def test_negative_numbers():
    assert find_common([-1, -2, -3], [-2, -3, -4]) == 2


def test_positive_and_negative_numbers():
    assert find_common([-1, 0, 1], [0, 1, 2]) == 2


def test_zero():
    assert find_common([0, 1, 2], [0, 3, 4]) == 1


def test_large_integers():
    assert find_common(
        [10**100, 10**200],
        [10**200, 10**300]
    ) == 1


def test_duplicate_elements_first_list():
    assert find_common([1, 1, 1, 2], [1, 2, 3]) == 2


def test_duplicate_elements_second_list():
    assert find_common([1, 2, 3], [1, 1, 1, 2]) == 2


def test_duplicates_in_both_lists():
    assert find_common([1, 1, 2, 2], [1, 1, 2, 2]) == 2


def test_all_elements_duplicated():
    assert find_common([7, 7, 7], [7, 7, 7]) == 1


def test_different_list_lengths():
    assert find_common([1, 2], [1, 2, 3, 4, 5]) == 2


def test_reversed_lists():
    assert find_common([1, 2, 3, 4], [4, 3, 2, 1]) == 4


def test_common_elements_in_different_positions():
    assert find_common([10, 20, 30, 40], [40, 10, 50, 30]) == 3


def test_large_lists():
    list1 = list(range(10000))
    list2 = list(range(5000, 15000))
    assert find_common(list1, list2) == 5000


def test_no_overlap_negative_and_positive():
    assert find_common([-5, -4, -3], [1, 2, 3]) == 0


def test_repeated_zero():
    assert find_common([0, 0, 0], [0, 0]) == 1


def test_order_does_not_affect_result():
    assert find_common([1, 2, 3], [3, 1, 2]) == find_common(
        [3, 1, 2], [1, 2, 3]
    )


def test_result_does_not_exceed_smaller_unique_list():
    list1 = [1, 1, 2, 3]
    list2 = [1, 2, 2]
    result = find_common(list1, list2)
    assert 0 <= result <= 2


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
