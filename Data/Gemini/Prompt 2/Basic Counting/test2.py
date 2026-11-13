import pytest
from basic_counting import find_common, find_common_efficient

@pytest.mark.parametrize("func", [find_common, find_common_efficient])
class TestCommonElements:

    def test_normal_overlap(self, func):
        list1 = [1, 2, 3, 4, 5]
        list2 = [4, 5, 6, 7, 8]
        assert func(list1, list2) == 2  # Common: 4, 5

    def test_empty_lists(self, func):
        assert func([], []) == 0
        assert func([1, 2, 3], []) == 0
        assert func([], [1, 2, 3]) == 0

    def test_no_common_elements(self, func):
        assert func([1, 2, 3], [4, 5, 6]) == 0

    def test_all_elements_common(self, func):
        assert func([1, 2, 3], [3, 2, 1]) == 3
        assert func([5, 5, 5], [5, 5]) == 1

    def test_duplicate_values_handling(self, func):
        # Distinct values count: intersection of {1, 2} and {1, 2, 3} is 2
        list1 = [1, 1, 1, 2, 2]
        list2 = [1, 2, 2, 2, 3]
        assert func(list1, list2) == 2

    def test_negative_integers_and_zero(self, func):
        list1 = [-5, -2, 0, 3]
        list2 = [-2, 0, 3, 5]
        assert func(list1, list2) == 3  # Common: -2, 0, 3

    def test_all_negative_integers(self, func):
        list1 = [-10, -5, -3]
        list2 = [-5, -3, -1]
        assert func(list1, list2) == 2  # Common: -5, -3

    def test_single_element_match(self, func):
        assert func([42], [42]) == 1
        assert func([42], [99]) == 0

    def test_disjoint_with_zero(self, func):
        assert func([0], [1]) == 0
        assert func([0], [0]) == 1

    def test_large_number_of_duplicates(self, func):
        list1 = [1] * 1000
        list2 = [1, 2] * 500
        assert func(list1, list2) == 1