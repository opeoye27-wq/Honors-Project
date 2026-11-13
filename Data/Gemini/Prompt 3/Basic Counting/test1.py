import pytest

# ==========================================
# EXPLICIT ASSUMPTIONS:
# 1. The function under test is named `find_common(list1, list2)`.
# 2. It treats lists as sets for counting common elements (i.e., duplicate values 
#    within the same list do not inflate the count; unique common elements are counted).
# 3. Inputs are expected to be lists of integers; non-list inputs should raise a TypeError.
# ==========================================

try:
    from basic_counting import find_common
except ImportError:
    # Fallback or stub for static analysis / standalone testing structure
    def find_common(l1, l2):
        raise NotImplementedError("Function under test not imported.")


def test_normal_overlapping_elements():
    """Test standard lists with some overlapping integers."""
    assert find_common([1, 2, 3, 4], [3, 4, 5, 6]) == 2


def test_normal_no_common_elements():
    """Test lists with completely disjoint integers."""
    assert find_common([1, 2, 3], [4, 5, 6]) == 0


def test_normal_identical_lists():
    """Test lists that are exact duplicates of each other."""
    assert find_common([1, 2, 3], [1, 2, 3]) == 3


def test_edge_case_both_lists_empty():
    """Test boundary condition where both input lists are empty."""
    assert find_common([], []) == 0


def test_edge_case_one_list_empty():
    """Test boundary condition where one list is empty and the other is not."""
    assert find_common([1, 2, 3], []) == 0
    assert find_common([], [1, 2, 3]) == 0


def test_edge_case_internal_duplicates():
    """Test behavior when lists contain duplicate values internally."""
    # Assuming unique set intersection: {1, 2} and {2, 3} share {2} -> count is 1
    assert find_common([1, 2, 2], [2, 2, 3]) == 1


def test_unusual_inputs_negative_numbers():
    """Test unusual input containing negative integers and mixed signs."""
    assert find_common([-5, -2, 0, 3], [-2, 0, 3, 9]) == 3


def test_unusual_inputs_large_ranges():
    """Test performance/correctness with larger datasets."""
    list1 = list(range(1000))
    list2 = list(range(500, 1500))
    assert find_common(list1, list2) == 500


def test_invalid_inputs_wrong_types():
    """Test invalid inputs where arguments are not lists."""
    with pytest.raises((TypeError, AttributeError)):
        find_common(None, [1, 2, 3])
    
    with pytest.raises((TypeError, AttributeError)):
        find_common([1, 2, 3], "1,2,3")