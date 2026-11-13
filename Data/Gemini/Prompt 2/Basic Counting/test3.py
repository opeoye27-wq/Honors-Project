import pytest

try:
    from basic_counting import find_common, find_common_efficient

    FUNCTIONS_TO_TEST = [
        ("nested_loops", find_common),
        ("sets", find_common_efficient),
    ]
except ImportError:
    FUNCTIONS_TO_TEST = []


@pytest.mark.parametrize("func_name, func", FUNCTIONS_TO_TEST)
def test_empty_lists(func_name, func):
    assert func([], []) == 0


@pytest.mark.parametrize("func_name, func", FUNCTIONS_TO_TEST)
def test_one_empty_list(func_name, func):
    assert func([1, 2, 3], []) == 0
    assert func([], [1, 2, 3]) == 0


@pytest.mark.parametrize("func_name, func", FUNCTIONS_TO_TEST)
def test_no_common_elements(func_name, func):
    assert func([1, 2, 3], [4, 5, 6]) == 0


@pytest.mark.parametrize("func_name, func", FUNCTIONS_TO_TEST)
def test_all_elements_common(func_name, func):
    assert func([1, 2, 3], [1, 2, 3]) == 3


@pytest.mark.parametrize("func_name, func", FUNCTIONS_TO_TEST)
def test_partially_overlapping(func_name, func):
    assert func([1, 2, 3, 4], [3, 4, 5, 6]) == 2


@pytest.mark.parametrize("func_name, func", FUNCTIONS_TO_TEST)
def test_duplicates_within_and_across_lists(func_name, func):
    # Testing that duplicate values are correctly handled as distinct counts
    assert func([1, 1, 2, 2, 3], [2, 2, 3, 3, 4]) == 2  # common distinct: 2, 3


@pytest.mark.parametrize("func_name, func", FUNCTIONS_TO_TEST)
def test_negative_integers_and_zero(func_name, func):
    assert func([-3, -2, -1, 0, 1], [-1, 0, 1, 2, 3]) == 3  # common distinct: -1, 0, 1


@pytest.mark.parametrize("func_name, func", FUNCTIONS_TO_TEST)
def test_single_element_lists_match(func_name, func):
    assert func([5], [5]) == 1


@pytest.mark.parametrize("func_name, func", FUNCTIONS_TO_TEST)
def test_single_element_lists_no_match(func_name, func):
    assert func([5], [6]) == 0


@pytest.mark.parametrize("func_name, func", FUNCTIONS_TO_TEST)
def test_unsorted_lists(func_name, func):
    assert func([9, 2, 5, 1, 7], [5, 1, 8, 9, 4]) == 3  # common distinct: 1, 5, 9