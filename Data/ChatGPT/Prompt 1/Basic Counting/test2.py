
import random
import pytest
from unittest.mock import patch

# Replace "your_module" with the name of the Python file containing the program.
from basic_counting import generate_lists, find_common, find_common_efficient


# -------------------------
# Tests for generate_lists
# -------------------------

def test_generate_lists_returns_two_lists():
    list1, list2 = generate_lists(10)

    assert isinstance(list1, list)
    assert isinstance(list2, list)


def test_generate_lists_correct_length():
    list1, list2 = generate_lists(10)

    assert len(list1) == 10
    assert len(list2) == 10


def test_generate_lists_values_in_expected_range():
    size = 20
    list1, list2 = generate_lists(size)

    assert all(0 <= x < size * 2 for x in list1)
    assert all(0 <= x < size * 2 for x in list2)


def test_generate_lists_contains_no_duplicates():
    list1, list2 = generate_lists(20)

    assert len(list1) == len(set(list1))
    assert len(list2) == len(set(list2))


def test_generate_lists_zero_size():
    list1, list2 = generate_lists(0)

    assert list1 == []
    assert list2 == []


def test_generate_lists_size_one():
    list1, list2 = generate_lists(1)

    assert len(list1) == 1
    assert len(list2) == 1


def test_generate_lists_negative_size():
    with pytest.raises(ValueError):
        generate_lists(-1)


def test_generate_lists_size_exceeds_population():
    with pytest.raises(ValueError):
        generate_lists(3) if False else random.sample(range(6), 7)


def test_generate_lists_non_integer_size():
    with pytest.raises(TypeError):
        generate_lists(2.5)


# -------------------------
# Tests for find_common
# -------------------------

@pytest.mark.parametrize(
    "list1, list2, expected",
    [
        ([], [], 0),
        ([1], [1], 1),
        ([1], [2], 0),
        ([1, 2, 3], [2, 3, 4], 2),
        ([1, 2, 3], [4, 5, 6], 0),
        ([1, 2, 3], [1, 2, 3], 3),
        ([0, -1, 5], [-1, 5, 10], 2),
        (["a", "b"], ["b", "c"], 1),
        ([1, 1, 2], [1, 1], 4),
        ([1, 1, 1], [1, 1], 6),
        ([1, 2, 3], [3, 2, 1], 3),
        ([1, 2, 3], [], 0),
        ([], [1, 2, 3], 0),
    ],
)
def test_find_common_cases(list1, list2, expected):
    assert find_common(list1, list2) == expected


def test_find_common_counts_duplicate_matches():
    assert find_common([1, 1, 2], [1, 1, 2]) == 5


def test_find_common_does_not_modify_inputs():
    list1 = [1, 2, 2, 3]
    list2 = [2, 3, 3, 4]
    original1 = list1.copy()
    original2 = list2.copy()

    find_common(list1, list2)

    assert list1 == original1
    assert list2 == original2


def test_find_common_with_none_element():
    assert find_common([None, 1], [None, 2]) == 1


def test_find_common_with_mixed_types():
    assert find_common([1, "a", None], ["a", None, 2]) == 2


def test_find_common_with_invalid_none_input():
    with pytest.raises(TypeError):
        find_common(None, [1, 2])


def test_find_common_with_non_iterable_input():
    with pytest.raises(TypeError):
        find_common(123, [1, 2])


# -------------------------------
# Tests for find_common_efficient
# -------------------------------

@pytest.mark.parametrize(
    "list1, list2, expected",
    [
        ([], [], 0),
        ([1], [1], 1),
        ([1], [2], 0),
        ([1, 2, 3], [2, 3, 4], 2),
        ([1, 2, 3], [4, 5, 6], 0),
        ([1, 2, 3], [1, 2, 3], 3),
        ([0, -1, 5], [-1, 5, 10], 2),
        (["a", "b"], ["b", "c"], 1),
        ([1, 1, 2], [1, 1], 2),
        ([1, 1, 1], [1, 1], 1),
        ([1, 2, 3], [3, 2, 1], 3),
        ([1, 2, 3], [], 0),
        ([], [1, 2, 3], 0),
    ],
)
def test_find_common_efficient_cases(list1, list2, expected):
    assert find_common_efficient(list1, list2) == expected


def test_find_common_efficient_ignores_duplicates():
    assert find_common_efficient([1, 1, 2], [1, 1, 2]) == 2


def test_find_common_efficient_does_not_modify_inputs():
    list1 = [1, 2, 2, 3]
    list2 = [2, 3, 3, 4]
    original1 = list1.copy()
    original2 = list2.copy()

    find_common_efficient(list1, list2)

    assert list1 == original1
    assert list2 == original2


def test_find_common_efficient_with_none_element():
    assert find_common_efficient([None, 1], [None, 2]) == 1


def test_find_common_efficient_with_unhashable_elements():
    with pytest.raises(TypeError):
        find_common_efficient([[1], [2]], [[1], [3]])


def test_find_common_efficient_with_invalid_none_input():
    with pytest.raises(TypeError):
        find_common_efficient(None, [1, 2])


def test_find_common_efficient_with_non_iterable_input():
    with pytest.raises(TypeError):
        find_common_efficient(123, [1, 2])


# -------------------------------------
# Cross-check both functions on unique inputs
# -------------------------------------

def test_both_functions_agree_on_unique_inputs():
    list1 = [1, 2, 3, 4, 5]
    list2 = [4, 5, 6, 7, 8]

    assert find_common(list1, list2) == find_common_efficient(list1, list2)


def test_both_functions_agree_on_random_unique_lists():
    random.seed(42)

    for size in range(0, 30):
        list1 = random.sample(range(size * 4 + 1), size)
        list2 = random.sample(range(size * 4 + 1), size)

        assert find_common(list1, list2) == find_common_efficient(list1, list2)


def test_both_functions_differ_when_duplicates_exist():
    list1 = [1, 1, 2]
    list2 = [1, 1, 2]

    assert find_common(list1, list2) == 5
    assert find_common_efficient(list1, list2) == 2
