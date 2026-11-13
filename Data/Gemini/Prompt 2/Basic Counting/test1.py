import pytest

# Assuming the functions are imported from the implementation module.
# Replace `basic_counting` with the actual module name if necessary.
from basic_counting import find_common, find_common_efficient

@pytest.mark.parametrize("func", [find_common, find_common_efficient])
class TestCommonElements:

    def test_normal_overlapping_with_duplicates(self, func):
        list1 = [1, 2, 2, 3, 4]
        list2 = [3, 4, 4, 5, 6]
        # Distinct common values are 3 and 4 -> count is 2
        assert func(list1, list2) == 2

    def test_empty_lists(self, func):
        assert func([], []) == 0
        assert func([1, 2, 3], []) == 0
        assert func([], [1, 2, 3]) == 0

    def test_no_common_elements(self, func):
        assert func([1, 2, 3], [4, 5, 6]) == 0

    def test_all_elements_in_common(self, func):
        list1 = [1, 2, 3, 3, 3]
        list2 = [3, 2, 1, 1]
        # Distinct common values are 1, 2, 3 -> count is 3
        assert func(list1, list2) == 3

    def test_negative_integers_and_zero(self, func):
        list1 = [-5, -2, 0, 3]
        list2 = [-2, 0, 3, 5]
        # Distinct common values are -2, 0, 3 -> count is 3
        assert func(list1, list2) == 3

    def test_single_element_lists_match(self, func):
        assert func([42], [42]) == 1

    def test_single_element_lists_no_match(self, func):
        assert func([42], [24]) == 0

    def test_only_duplicates_within_lists(self, func):
        list1 = [7, 7, 7, 7]
        list2 = [7, 7]
        # Distinct common value is 7 -> count is 1
        assert func(list1, list2) == 1