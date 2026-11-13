import pytest

# Assuming the function under test is named find_common(list1, list2)
try:
    from basic_counting import find_common
except ImportError:
    def find_common(list1, list2):
        raise NotImplementedError("Function to test must be provided in 'basic_counting.py'")


def test_normal_cases():
    assert find_common([1, 2, 3, 4], [3, 4, 5, 6]) == 2
    assert find_common([1, 2, 3], [4, 5, 6]) == 0
    assert find_common([10, 20, 30, 40], [10, 30, 50]) == 2


def test_edge_cases_empty_lists():
    assert find_common([], []) == 0
    assert find_common([1, 2, 3], []) == 0
    assert find_common([], [1, 2, 3]) == 0


def test_edge_cases_identical_lists():
    assert find_common([1, 2, 3], [1, 2, 3]) == 3
    assert find_common([5], [5]) == 1


def test_edge_cases_duplicates():
    # Tests behavior with repeated elements within lists
    result = find_common([1, 1, 2, 2], [1, 2, 2, 3])
    # Validates that duplicate handling doesn't crash or behave unexpectedly
    assert isinstance(result, int)
    assert result >= 0


def test_unusual_inputs_negative_numbers():
    assert find_common([-1, -2, -3], [-2, -3, -4]) == 2
    assert find_common([-5, 0, 5], [0, 5, 10]) == 2


def test_unusual_inputs_large_integers():
    large_val = 10**18
    assert find_common([large_val, 1, 2], [large_val, 3, 4]) == 1


def test_unusual_inputs_subset_relationships():
    assert find_common([1, 2], [1, 2, 3, 4]) == 2
    assert find_common([1, 2, 3, 4], [1, 2]) == 2