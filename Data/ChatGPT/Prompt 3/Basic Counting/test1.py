import pytest
from basic_counting import find_common

# Assumption: The function find_common(list1, list2) returns the number
# of common elements between the two lists.
# Assumption: Each matching value is counted only once per occurrence
# in list1 that also has a matching occurrence in list2.
# Assumption: The function does not modify either input list.


def test_both_lists_empty():
    assert find_common([], []) == 0


def test_first_list_empty():
    assert find_common([], [1, 2, 3]) == 0


def test_second_list_empty():
    assert find_common([1, 2, 3], []) == 0


def test_no_common_elements():
    assert find_common([1, 2, 3], [4, 5, 6]) == 0


def test_all_elements_common():
    assert find_common([1, 2, 3], [1, 2, 3]) == 3


def test_one_common_element():
    assert find_common([1, 2, 3], [3, 4, 5]) == 1


def test_multiple_common_elements():
    assert find_common([1, 2, 3, 4], [2, 4, 6, 8]) == 2


def test_common_elements_in_different_orders():
    assert find_common([1, 2, 3, 4], [4, 3, 2, 1]) == 4


def test_different_list_lengths():
    assert find_common([1, 2], [1, 2, 3, 4, 5]) == 2


def test_first_list_longer():
    assert find_common([1, 2, 3, 4, 5], [2, 4]) == 2


def test_negative_numbers():
    assert find_common([-1, -2, -3], [-2, -3, -4]) == 2


def test_zero_as_common_element():
    assert find_common([0, 1, 2], [0, 3, 4]) == 1


def test_all_negative_numbers():
    assert find_common([-1, -2, -3], [-1, -2, -3]) == 3


def test_mixed_positive_negative_and_zero():
    assert find_common([-2, -1, 0, 1, 2], [-3, -2, 0, 2, 3]) == 3


def test_duplicate_elements_in_first_list():
    assert find_common([1, 1, 2, 3], [1, 2, 3]) == 3


def test_duplicate_elements_in_second_list():
    assert find_common([1, 2, 3], [1, 1, 2, 3]) == 3


def test_duplicates_in_both_lists():
    assert find_common([1, 1, 2, 2], [1, 2, 2, 2]) == 3


def test_only_duplicate_elements():
    assert find_common([5, 5, 5], [5, 5]) == 2


def test_duplicates_with_no_common_elements():
    assert find_common([1, 1, 2, 2], [3, 3, 4, 4]) == 0


def test_repeated_zero():
    assert find_common([0, 0, 0], [0, 0]) == 2


def test_large_integer_values():
    assert find_common(
        [10**100, -(10**100), 5],
        [10**100, 5, 7]
    ) == 2


def test_single_element_lists_matching():
    assert find_common([42], [42]) == 1


def test_single_element_lists_not_matching():
    assert find_common([42], [43]) == 0


def test_large_lists_with_no_common_elements():
    list1 = list(range(1000))
    list2 = list(range(1000, 2000))
    assert find_common(list1, list2) == 0


def test_large_lists_with_all_common_elements():
    list1 = list(range(1000))
    list2 = list(range(1000))
    assert find_common(list1, list2) == 1000


def test_large_lists_with_partial_overlap():
    list1 = list(range(1000))
    list2 = list(range(500, 1500))
    assert find_common(list1, list2) == 500


def test_original_lists_are_not_modified():
    list1 = [1, 2, 3, 4]
    list2 = [3, 4, 5, 6]

    original1 = list1.copy()
    original2 = list2.copy()

    find_common(list1, list2)

    assert list1 == original1
    assert list2 == original2


@pytest.mark.parametrize(
    "list1, list2, expected",
    [
        ([1, 2, 3], [1, 2, 3], 3),
        ([1, 2, 3], [4, 5, 6], 0),
        ([1, 2, 3], [2, 3, 4], 2),
        ([5, 5, 5], [5], 1),
        ([5], [5, 5, 5], 1),
        ([-1, 0, 1], [-1, 1], 2),
        ([0, 0], [0, 0], 2),
        ([100, 200, 300], [300, 100], 2),
        ([], [], 0),
    ]
)
def test_various_inputs(list1, list2, expected):
    assert find_common(list1, list2) == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        123,
        "123",
        3.14,
        {"a": 1},
        (1, 2, 3),
    ]
)
def test_invalid_first_argument(invalid_input):
    with pytest.raises((TypeError, ValueError)):
        find_common(invalid_input, [1, 2, 3])


@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        123,
        "123",
        3.14,
        {"a": 1},
        (1, 2, 3),
    ]
)
def test_invalid_second_argument(invalid_input):
    with pytest.raises((TypeError, ValueError)):
        find_common([1, 2, 3], invalid_input)


@pytest.mark.parametrize(
    "list1, list2",
    [
        ([1, "2", 3], [1, 2, 3]),
        ([1, 2, 3], [1, "2", 3]),
        ([1, None, 3], [1, 2, 3]),
        ([1, 2, 3], [1, None, 3]),
        ([1, 2.5, 3], [1, 2, 3]),
    ]
)
def test_non_integer_elements(list1, list2):
    # Assumption: Both lists must contain integers only.
    with pytest.raises((TypeError, ValueError)):
        find_common(list1, list2)


def test_boolean_elements():
    # Assumption: Booleans are not accepted as integers for this function.
    with pytest.raises((TypeError, ValueError)):
        find_common([True, False], [1, 0])


def test_very_large_list_with_duplicates():
    list1 = [7] * 10000
    list2 = [7] * 5000

    assert find_common(list1, list2) == 5000


def test_lists_with_interleaved_common_elements():
    list1 = [1, 100, 2, 200, 3, 300]
    list2 = [300, 3, 200, 2, 100, 1]

    assert find_common(list1, list2) == 6