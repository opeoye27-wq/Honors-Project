import pytest

# Assumption:
# The two functions are named find_common and find_common_set.
# Both functions should return the number of DISTINCT integers
# that appear in both input lists.
#
# Replace the import below with the actual filename of your program.
from basic_counting import find_common, find_common_efficient


@pytest.mark.parametrize("func", [find_common, find_common_efficient])
class TestCommonElements:

    # Normal inputs
    def test_identical_lists(self, func):
        assert func([1, 2, 3], [1, 2, 3]) == 3

    def test_partially_overlapping_lists(self, func):
        assert func([1, 2, 3, 4], [3, 4, 5, 6]) == 2

    def test_one_common_element(self, func):
        assert func([1, 2, 3], [3, 4, 5]) == 1

    def test_no_common_elements(self, func):
        assert func([1, 2, 3], [4, 5, 6]) == 0

    # Empty lists
    def test_both_lists_empty(self, func):
        assert func([], []) == 0

    def test_first_list_empty(self, func):
        assert func([], [1, 2, 3]) == 0

    def test_second_list_empty(self, func):
        assert func([1, 2, 3], []) == 0

    # Lists with all elements in common
    def test_all_elements_common(self, func):
        assert func([5, 10, 15], [15, 10, 5]) == 3

    def test_single_element_lists_with_match(self, func):
        assert func([7], [7]) == 1

    def test_single_element_lists_without_match(self, func):
        assert func([7], [8]) == 0

    # Duplicate values
    def test_duplicates_in_first_list(self, func):
        assert func([1, 1, 1, 2, 3], [1, 2, 4]) == 2

    def test_duplicates_in_second_list(self, func):
        assert func([1, 2, 3], [1, 1, 1, 2, 4]) == 2

    def test_duplicates_in_both_lists(self, func):
        assert func([1, 1, 2, 2, 3], [1, 1, 1, 2, 2]) == 2

    def test_only_duplicate_common_value(self, func):
        assert func([5, 5, 5], [5, 5]) == 1

    def test_duplicates_with_no_common_values(self, func):
        assert func([1, 1, 2, 2], [3, 3, 4, 4]) == 0

    # Negative integers and zero
    def test_negative_integers(self, func):
        assert func([-1, -2, -3], [-2, -3, -4]) == 2

    def test_zero_common(self, func):
        assert func([0, 1, 2], [0, 3, 4]) == 1

    def test_zero_and_negative_integers(self, func):
        assert func([-2, -1, 0, 1], [-1, 0, 2]) == 2

    def test_all_negative_integers_common(self, func):
        assert func([-5, -4, -3], [-3, -4, -5]) == 3

    # Boundary cases
    def test_large_positive_integers(self, func):
        assert func([10**12, 10**15], [10**15, 10**18]) == 1

    def test_large_negative_integers(self, func):
        assert func([-10**12, -10**15], [-10**15, -10**18]) == 1

    def test_consecutive_integers(self, func):
        assert func(list(range(100)), list(range(50, 150))) == 50

    def test_large_lists_no_overlap(self, func):
        assert func(list(range(1000)), list(range(1000, 2000))) == 0

    def test_large_lists_complete_overlap(self, func):
        assert func(list(range(1000)), list(range(1000))) == 1000

    def test_unequal_list_lengths(self, func):
        assert func([1, 2, 3, 4, 5, 6], [2, 4]) == 2

    def test_common_elements_at_opposite_positions(self, func):
        assert func([1, 2, 3, 4], [4, 3, 2, 1]) == 4

    # Unusual input arrangements
    def test_reversed_lists(self, func):
        assert func([1, 2, 3, 4], [4, 3, 2, 1]) == 4

    def test_interleaved_common_and_unique_values(self, func):
        assert func(
            [1, 10, 2, 20, 3, 30],
            [10, 100, 20, 200, 30, 300]
        ) == 3

    def test_same_value_repeated_many_times(self, func):
        assert func([9] * 100, [9] * 200) == 1

    def test_common_values_with_different_frequencies(self, func):
        assert func([1, 1, 1, 2, 3, 3], [1, 2, 2, 2, 3]) == 3


# Verify that both approaches produce identical results.
@pytest.mark.parametrize(
    "list1,list2",
    [
        ([], []),
        ([], [1, 2, 3]),
        ([1, 2, 3], []),
        ([1, 2, 3], [4, 5, 6]),
        ([1, 2, 3], [2, 3, 4]),
        ([1, 1, 2, 2], [1, 2, 2, 3]),
        ([-5, -4, 0, 1], [-4, 0, 2]),
        (list(range(500)), list(range(250, 750))),
        ([7] * 100, [7] * 200),
    ]
)
def test_both_functions_agree(list1, list2):
    assert find_common(list1, list2) == find_common_efficient(list1, list2)


# Verify symmetry: switching the lists should not change the result.
@pytest.mark.parametrize("func", [find_common, find_common_efficient])
@pytest.mark.parametrize(
    "list1,list2",
    [
        ([1, 2, 3], [2, 3, 4]),
        ([1, 1, 2], [1, 2, 2]),
        ([-3, -2, 0], [-2, 0, 1]),
        ([], [1, 2, 3]),
        ([5], [5, 5, 5]),
    ]
)
def test_symmetry(func, list1, list2):
    assert func(list1, list2) == func(list2, list1)


# Verify that the result never exceeds the number of distinct
# elements in either input list.
@pytest.mark.parametrize("func", [find_common, find_common_efficient])
@pytest.mark.parametrize(
    "list1,list2",
    [
        ([1, 1, 1, 2], [1, 2, 3]),
        ([1, 2, 3], [1, 1, 1]),
        ([-1, 0, 1], [-1, 0, 1, 2]),
    ]
)
def test_result_does_not_exceed_distinct_list_size(func, list1, list2):
    result = func(list1, list2)

    assert result <= len(set(list1))
    assert result <= len(set(list2))
    assert result >= 0