import pytest

# Explicit assumptions for interface names based on the description:
# - Class name: BSTSet
# - Insertion method: put(key)
# - Traversal methods: in_order(), pre_order(), post_order()
# - Size/length: __len__() or len() support
from BST import BSTSet


@pytest.fixture
def empty_bst():
    """Fixture to provide a fresh empty BSTSet instance for each test."""
    return BSTSet()


def test_initialization(empty_bst):
    """Test that a newly created BST set is empty."""
    assert len(empty_bst) == 0
    assert empty_bst.in_order() == []
    assert empty_bst.pre_order() == []
    assert empty_bst.post_order() == []


def test_single_insertion(empty_bst):
    """Test inserting a single element into the BST set."""
    empty_bst.put(10)
    assert len(empty_bst) == 1
    assert empty_bst.in_order() == [10]
    assert empty_bst.pre_order() == [10]
    assert empty_bst.post_order() == [10]


def test_multiple_insertions_and_traversals(empty_bst):
    """Test multiple insertions and verify all traversal orders."""
    keys = [5, 3, 7, 2, 4, 6, 8]
    for key in keys:
        empty_bst.put(key)
    
    assert len(empty_bst) == 7
    # In-order traversal of a BST must yield sorted elements
    assert empty_bst.in_order() == [2, 3, 4, 5, 6, 7, 8]
    assert empty_bst.pre_order() == [5, 3, 2, 4, 7, 6, 8]
    assert empty_bst.post_order() == [2, 4, 3, 6, 8, 7, 5]


def test_duplicate_keys(empty_bst):
    """Test that inserting duplicate keys does not alter the set (set property)."""
    empty_bst.put(10)
    empty_bst.put(10)
    empty_bst.put(5)
    empty_bst.put(5)
    
    assert len(empty_bst) == 2
    assert empty_bst.in_order() == [5, 10]


def test_right_skewed_tree(empty_bst):
    """Test insertions in strictly ascending order (right-skewed tree edge case)."""
    keys = [1, 2, 3, 4, 5]
    for key in keys:
        empty_bst.put(key)
    
    assert len(empty_bst) == 5
    assert empty_bst.in_order() == [1, 2, 3, 4, 5]
    assert empty_bst.pre_order() == [1, 2, 3, 4, 5]
    assert empty_bst.post_order() == [5, 4, 3, 2, 1]


def test_left_skewed_tree(empty_bst):
    """Test insertions in strictly descending order (left-skewed tree edge case)."""
    keys = [5, 4, 3, 2, 1]
    for key in keys:
        empty_bst.put(key)
    
    assert len(empty_bst) == 5
    assert empty_bst.in_order() == [1, 2, 3, 4, 5]
    assert empty_bst.pre_order() == [5, 4, 3, 2, 1]
    assert empty_bst.post_order() == [1, 2, 3, 4, 5]


def test_negative_and_zero_keys(empty_bst):
    """Test handling of unusual numeric inputs like zero and negative numbers."""
    keys = [0, -5, 5, -10, 10]
    for key in keys:
        empty_bst.put(key)
    
    assert len(empty_bst) == 5
    assert empty_bst.in_order() == [-10, -5, 0, 5, 10]


def test_string_keys(empty_bst):
    """Test handling of non-numeric keys (strings) supporting comparable operations."""
    keys = ["banana", "apple", "cherry", "date"]
    for key in keys:
        empty_bst.put(key)
    
    assert len(empty_bst) == 4
    assert empty_bst.in_order() == ["apple", "banana", "cherry", "date"]


def test_incompatible_types(empty_bst):
    """Test invalid input types where keys cannot be compared."""
    empty_bst.put(10)
    with pytest.raises((TypeError, ValueError)):
        empty_bst.put("invalid_string_key")