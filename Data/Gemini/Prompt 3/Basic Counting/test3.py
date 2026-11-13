import pytest

# Assumption: The function under test is named `find_common(list1, list2)`
# and returns the count of common elements between two lists of integers.
from basic_counting import find_common


def test_normal_case_basic_overlap():
    assert find_common([1, 2, 3], [2, 3, 4]) == 2


def test_normal_case_no_overlap():
    assert find_common([1, 2, 3], [4, 5, 6]) == 0


def test_normal_case_identical_lists():
    assert find_common([1, 2, 3], [1, 2, 3]) == 3


def test_edge_case_both_empty():
    assert find_common([], []) == 0


def test_edge_case_one_empty():
    assert find_common([1, 2, 3], []) == 0
    assert find_common([], [1, 2, 3]) == 0


def test_edge_case_single_element_match():
    assert find_common([5], [5]) == 1


def test_edge_case_single_element_no_match():
    assert find_common([5], [3]) == 0


def test_unusual_input_duplicates_within_lists():
    assert find_common([1, 1, 2], [1, 2, 2]) == 2


def test_unusual_input_negative_numbers():
    assert find_common([-1, -2, 3], [-2, -3, 3]) == 2


def test_unusual_input_mixed_signs_and_zero():
    assert find_common([0, -1, 5], [0, 1, -5]) == 1


def test_unusual_input_large_lists():
    list1 = list(range(1000))
    list2 = list(range(500, 1500))
    assert find_common(list1, list2) == 500