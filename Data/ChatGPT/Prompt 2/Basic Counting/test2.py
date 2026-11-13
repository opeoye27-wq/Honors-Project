import pytest

# Assumption: The two functions accept two lists of integers and return
# the number of DISTINCT values appearing in both lists.
# Duplicate occurrences must only be counted once.
#
# Replace the function names below with the actual names from your program.
# Import the functions from the appropriate module.

from basic_counting import find_common, find_common_efficient


@pytest.fixture
def counting_functions():
    """Provide both implementations for testing."""
    return [
        find_common,
        find_common_efficient
    ]


@pytest.mark.parametrize("list1, list2, expected", [
    # Normal inputs
    ([1, 2, 3], [2, 3, 4], 2),
    ([1, 2, 3], [4, 5, 6], 0),
    ([1, 2, 3], [1, 2, 3], 3),
    ([5, 10, 15], [5, 10, 15], 3),

    # Empty lists
    ([], [], 0),
    ([], [1, 2, 3], 0),
    ([1, 2, 3], [], 0),

    # No common elements
    ([1, 2, 3], [4, 5, 6], 0),
    ([-1, -2, -3], [1, 2, 3], 0),

    # Partial overlap
    ([1, 2, 3, 4], [3, 4, 5, 6], 2),
    ([1, 2, 3, 4, 5], [1, 3, 5], 3),
    ([10, 20, 30], [30, 40, 50], 1),

    # Negative integers
    ([-1, -2, -3], [-2, -3, -4], 2),
    ([-5, -4, -3], [-5, -4, -3], 3),
    ([-1, -2], [-3, -4], 0),

    # Zero
    ([0, 1, 2], [0, 2, 3], 2),
    ([0], [0], 1),
    ([0, 0, 0], [0, 0], 1),
    ([0, 1], [2, 3], 0),

    # Duplicate values
    ([1, 1, 1], [1, 1, 1], 1),
    ([1, 1, 2, 2], [1, 2, 2, 2], 2),
    ([1, 1, 1, 2, 3], [1, 2, 2, 4], 2),
    ([1, 1, 2, 2], [3, 3, 4, 4], 0),
    ([1, 2, 3], [1, 1, 1, 2, 2, 2, 3], 3),
    ([1, 1, 1, 1], [1, 2, 3, 4], 1),

    # Different list lengths
    ([1], [1, 2, 3, 4, 5], 1),
    ([1, 2, 3, 4, 5], [1], 1),
    ([1, 2], [1, 2, 3, 4, 5, 6], 2),
    ([1, 2, 3, 4, 5, 6], [1, 2], 2),

    # Boundary and unusual integer values
    ([0, -1, 1], [-1, 0, 1], 3),
    ([10**100], [10**100], 1),
    ([-10**100], [-10**100], 1),
    ([10**100, -10**100], [10**100, 0], 1),

    # Repeated and reordered elements
    ([1, 2, 3, 4], [4, 3, 2, 1], 4),
    ([1, 2, 2, 3], [3, 2, 1, 1], 3),
    ([5, 5, 5, 6, 6], [6, 6, 6, 5], 2),

    # Single-element lists
    ([7], [7], 1),
    ([7], [8], 0),
    ([-7], [-7], 1),

    # Larger lists
    (list(range(100)), list(range(50, 150)), 50),
    (list(range(1000)), list(range(1000)), 1000),
    (list(range(1000)), list(range(1000, 2000)), 0),
])
def test_count_common_values(counting_functions, list1, list2, expected):
    """Test both implementations against expected distinct counts."""
    for function in counting_functions:
        assert function(list1, list2) == expected


@pytest.mark.parametrize("list1, list2, expected", [
    ([1, 2, 3], [2, 3, 4], 2),
    ([1, 1, 2, 2], [1, 2, 2, 3], 2),
    ([], [1, 2], 0),
    ([0, -1, -2], [-1, -2, 0], 3),
    ([1, 2, 3], [4, 5, 6], 0),
])
def test_both_implementations_agree(
    counting_functions, list1, list2, expected
):
    """Verify that both approaches produce the same result."""
    nested_result = find_common(list1, list2)
    set_result = find_common_efficient(list1, list2)

    assert nested_result == set_result
    assert nested_result == expected


def test_duplicate_occurrences_do_not_inflate_count(counting_functions):
    """Repeated occurrences of a shared value count only once."""
    list1 = [1, 1, 1, 2, 2, 3]
    list2 = [1, 1, 2, 2, 2, 3, 3]

    for function in counting_functions:
        assert function(list1, list2) == 3


def test_result_is_not_greater_than_smaller_distinct_set(counting_functions):
    """The result cannot exceed the number of distinct values in either list."""
    list1 = [1, 1, 2, 2, 3, 3]
    list2 = [1, 2, 2, 4]

    for function in counting_functions:
        result = function(list1, list2)

        assert result <= len(set(list1))
        assert result <= len(set(list2))


def test_symmetry(counting_functions):
    """Swapping the two lists must not change the result."""
    list1 = [1, 2, 2, 3, 4]
    list2 = [2, 3, 3, 5]

    for function in counting_functions:
        assert function(list1, list2) == function(list2, list1)


def test_result_is_nonnegative(counting_functions):
    """The number of common distinct values cannot be negative."""
    test_cases = [
        ([], []),
        ([1, 2, 3], [4, 5, 6]),
        ([-1, 0, 1], [-1, 0, 1]),
        ([1, 1, 1], [1, 1, 1]),
    ]

    for function in counting_functions:
        for list1, list2 in test_cases:
            assert function(list1, list2) >= 0


def test_identical_lists_count_distinct_values(counting_functions):
    """Identical lists return their number of distinct values."""
    list1 = [1, 1, 2, 2, 3, 3, 3]

    for function in counting_functions:
        assert function(list1, list1) == 3


def test_input_lists_are_not_modified(counting_functions):
    """Counting common values should not modify either input list."""
    list1 = [1, 2, 2, 3, 4]
    list2 = [2, 3, 3, 5]

    original1 = list1.copy()
    original2 = list2.copy()

    for function in counting_functions:
        function(list1, list2)

        assert list1 == original1
        assert list2 == original2


def test_result_type_is_integer(counting_functions):
    """The functions should return an integer count."""
    list1 = [1, 2, 3]
    list2 = [2, 3, 4]

    for function in counting_functions:
        result = function(list1, list2)

        assert isinstance(result, int)
        assert not isinstance(result, bool)