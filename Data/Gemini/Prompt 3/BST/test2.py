import pytest

# Assuming the BST Set class is implemented in a module named `BST` 
# with class name `BSTSet`.
try:
    from BST import BSTSet
except ImportError:
    BSTSet = None


@pytest.fixture
def bst():
    if BSTSet is None:
        pytest.skip("BSTSet implementation not found")
    return BSTSet()


def test_empty_tree(bst):
    """Test traversals and properties on a newly created empty tree."""
    assert bst.in_order() == []
    assert bst.pre_order() == []
    assert bst.post_order() == []


def test_single_insertion(bst):
    """Test inserting a single element."""
    bst.put(10)
    assert bst.in_order() == [10]
    assert bst.pre_order() == [10]
    assert bst.post_order() == [10]


def test_multiple_insertions_and_traversals(bst):
    """Test standard insertions and different traversal orders."""
    # Inserting values to form a balanced-ish BST
    values = [5, 3, 7, 2, 4, 6, 8]
    for v in values:
        bst.put(v)

    # In-order traversal should always return elements in sorted order
    assert bst.in_order() == [2, 3, 4, 5, 6, 7, 8]

    # Pre-order traversal: Root -> Left Subtree -> Right Subtree
    assert bst.pre_order() == [5, 3, 2, 4, 7, 6, 8]

    # Post-order traversal: Left Subtree -> Right Subtree -> Root
    assert bst.post_order() == [2, 4, 3, 6, 8, 7, 5]


def test_duplicate_insertions(bst):
    """Test that inserting duplicate keys does not create duplicate entries (Set behavior)."""
    values = [5, 5, 3, 7, 3, 7]
    for v in values:
        bst.put(v)

    # Duplicates should be ignored, leaving only unique sorted elements
    assert bst.in_order() == [3, 5, 7]


def test_skewed_tree_ascending(bst):
    """Test edge case of inserting elements in strictly ascending order (right-skewed tree)."""
    values = [1, 2, 3, 4, 5]
    for v in values:
        bst.put(v)

    assert bst.in_order() == [1, 2, 3, 4, 5]
    assert bst.pre_order() == [1, 2, 3, 4, 5]
    assert bst.post_order() == [5, 4, 3, 2, 1]


def test_skewed_tree_descending(bst):
    """Test edge case of inserting elements in strictly descending order (left-skewed tree)."""
    values = [5, 4, 3, 2, 1]
    for v in values:
        bst.put(v)

    assert bst.in_order() == [1, 2, 3, 4, 5]
    assert bst.pre_order() == [5, 4, 3, 2, 1]
    assert bst.post_order() == [1, 2, 3, 4, 5]


def test_unusual_inputs_negative_numbers(bst):
    """Test unusual inputs including negative integers and zero."""
    values = [0, -5, 5, -10, 10]
    for v in values:
        bst.put(v)

    assert bst.in_order() == [-10, -5, 0, 5, 10]


def test_unusual_inputs_strings(bst):
    """Test inserting comparable string objects instead of numbers."""
    values = ["banana", "apple", "cherry", "date"]
    for v in values:
        bst.put(v)

    assert bst.in_order() == ["apple", "banana", "cherry", "date"]