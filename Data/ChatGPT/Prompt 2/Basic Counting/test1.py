import pytest
from basic_counting import find_common, find_common_efficient


@pytest.mark.parametrize("list1, list2, expected", [
    ([], [], 0),
    ([], [1, 2, 3], 0),
    ([1, 2, 3], [], 0),
    ([1, 2, 3], [4, 5, 6], 0),
    ([1, 2, 3], [1, 2, 3], 3),
    ([1, 2, 3], [2, 3, 4], 2),
    ([1, 2, 3, 4], [3, 4, 5, 6], 2),
    ([10, 20, 30], [20, 40, 60], 1),
    ([-1, -2, -3], [-2, -3, -4], 2),
    ([-1, -2, -3], [-4, -5, -6], 0),
    ([0, 1, 2], [0, 3, 4], 1),
    ([0], [0], 1),
    ([0], [1], 0),
    ([-2, -1, 0, 1, 2], [-1, 0, 1], 3),
    ([1, 1, 1], [1, 1], 1),
    ([1, 1, 2, 2, 3], [1, 2, 2, 3, 3], 3),
    ([1, 1, 2, 2], [2, 2, 3, 3], 1),
    ([1, 2, 3], [1, 1, 1, 2, 2, 3, 3], 3),
    ([1], [1, 2, 3, 4, 5], 1),
    ([1, 2, 3, 4, 5], [1], 1),
    ([1, 2, 3, 4], [4, 3, 2, 1], 4),
    ([5, 1, 3, 2], [2, 5, 4, 3], 3),
    ([10**10, 10**20], [10**20, 10**30], 1),
    ([-10**20, 10**20], [-10**20, 10**20], 2),
    ([0, 0, 0], [0, 0, 0], 1),
    ([0, 0, 1], [0, 2, 2], 1),
])
def test_common_elements(list1, list2, expected):
    assert find_common(list1, list2) == expected
    assert find_common_efficient(list1, list2) == expected


def test_symmetry():
    list1 = [1, 2, 3, 4, 4]
    list2 = [3, 4, 5, 5]

    assert find_common(list1, list2) == find_common(list2, list1)
    assert find_common_efficient(list1, list2) == find_common_efficient(list2, list1)


def test_duplicates_counted_once():
    list1 = [1, 1, 1, 2, 2, 3]
    list2 = [1, 1, 2, 2, 2, 3, 3]

    assert find_common(list1, list2) == 3
    assert find_common_efficient(list1, list2) == 3


def test_adding_duplicates_does_not_change_result():
    list1 = [1, 2, 3]
    list2 = [2, 3, 4]

    list1.extend([2, 2, 2])
    list2.extend([3, 3, 3])

    assert find_common(list1, list2) == 2
    assert find_common_efficient(list1, list2) == 2


def test_adding_noncommon_values_does_not_change_result():
    list1 = [1, 2, 3, 10, 11]
    list2 = [2, 3, 4, 20, 21]

    assert find_common(list1, list2) == 2
    assert find_common_efficient(list1, list2) == 2


def test_functions_agree_on_large_lists():
    list1 = list(range(1000))
    list2 = list(range(500, 1500))

    assert find_common(list1, list2) == 500
    assert find_common_efficient(list1, list2) == 500


def test_functions_agree_on_large_lists_with_duplicates():
    list1 = [i % 100 for i in range(1000)]
    list2 = [i % 100 for i in range(500, 1500)]

    assert find_common(list1, list2) == 100
    assert find_common_efficient(list1, list2) == 100


def test_input_lists_are_not_modified():
    list1 = [1, 2, 2, 3]
    list2 = [2, 3, 3, 4]

    original_list1 = list1.copy()
    original_list2 = list2.copy()

    find_common(list1, list2)
    find_common_efficient(list1, list2)

    assert list1 == original_list1
    assert list2 == original_list2


def test_single_common_element_among_many_values():
    list1 = list(range(-100, 101))
    list2 = [500, 1000, 0, 2000]

    assert find_common(list1, list2) == 1
    assert find_common_efficient(list1, list2) == 1


def test_no_common_elements_with_duplicates():
    list1 = [1, 1, 1, 2, 2, 2]
    list2 = [3, 3, 3, 4, 4, 4]

    assert find_common(list1, list2) == 0
    assert find_common_efficient(list1, list2) == 0


def test_identical_lists_with_duplicates():
    list1 = [1, 1, 2, 2, 3, 3]
    list2 = [1, 1, 2, 2, 3, 3]

    assert find_common(list1, list2) == 3
    assert find_common_efficient(list1, list2) == 3


@pytest.mark.parametrize("list1, list2", [
    (None, [1, 2, 3]),
    ([1, 2, 3], None),
    (None, None),
])
def test_invalid_list_inputs(list1, list2):
    # Assumption: Invalid list arguments raise TypeError or ValueError.
    with pytest.raises((TypeError, ValueError)):
        find_common(list1, list2)

    with pytest.raises((TypeError, ValueError)):
        find_common_efficient(list1, list2)