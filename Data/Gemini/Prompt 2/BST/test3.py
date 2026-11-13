import pytest

try:
    from BST import BSTSet, BSTNode
except ImportError:
    pass


def test_empty_tree():
    bst = BSTSet()
    assert list(bst.in_order()) == []
    assert list(bst.pre_order()) == []
    assert list(bst.post_order()) == []
    assert list(bst) == []


def test_single_node():
    bst = BSTSet()
    bst.put(42)
    assert list(bst.in_order()) == [42]
    assert list(bst.pre_order()) == [42]
    assert list(bst.post_order()) == [42]
    assert list(bst) == [42]


def test_duplicate_keys():
    bst = BSTSet()
    bst.put(10)
    bst.put(10)
    bst.put(10)
    # Uniqueness check: duplicates should be ignored
    assert list(bst.in_order()) == [10]


def test_ascending_insertion_right_skewed():
    # Ascending insertion creates a right-skewed tree (missing left children)
    bst = BSTSet()
    for val in [1, 2, 3, 4, 5]:
        bst.put(val)

    assert list(bst.in_order()) == [1, 2, 3, 4, 5]
    assert list(bst.pre_order()) == [1, 2, 3, 4, 5]
    assert list(bst.post_order()) == [5, 4, 3, 2, 1]


def test_descending_insertion_left_skewed():
    # Descending insertion creates a left-skewed tree (missing right children)
    bst = BSTSet()
    for val in [5, 4, 3, 2, 1]:
        bst.put(val)

    assert list(bst.in_order()) == [1, 2, 3, 4, 5]
    assert list(bst.pre_order()) == [5, 4, 3, 2, 1]
    assert list(bst.post_order()) == [1, 2, 3, 4, 5]


def test_negative_zero_and_positive_integers():
    bst = BSTSet()
    keys = [0, -5, 5, -10, 10, -1, 1]
    for key in keys:
        bst.put(key)

    # In-order must always produce keys in strict ascending order
    assert list(bst.in_order()) == [-10, -5, -1, 0, 1, 5, 10]


def test_values_smaller_and_larger_than_root():
    bst = BSTSet()
    # Root node
    bst.put(10)
    # Values smaller than root
    bst.put(5)
    bst.put(2)
    # Values larger than root
    bst.put(15)
    bst.put(20)

    # In-order: left, current, right -> ascending order
    assert list(bst.in_order()) == [2, 5, 10, 15, 20]

    # Pre-order: current, left, right
    assert list(bst.pre_order()) == [10, 5, 2, 15, 20]

    # Post-order: left, right, current
    assert list(bst.post_order()) == [2, 5, 20, 15, 10]


def test_bst_properties_and_missing_children():
    # Constructing a tree with sparse left/right children
    bst = BSTSet()
    bst.put(50)
    bst.put(30)  # Left child of root
    bst.put(70)  # Right child of root
    bst.put(20)  # Left child of 30 (30 has no right child)
    bst.put(80)  # Right child of 70 (70 has no left child)

    assert list(bst.in_order()) == [20, 30, 50, 70, 80]
    assert list(bst.pre_order()) == [50, 30, 20, 70, 80]
    assert list(bst.post_order()) == [20, 30, 80, 70, 50]


def test_iteration_behavior():
    bst = BSTSet()
    keys = [8, 3, 10, 1, 6, 14, 4, 7, 13]
    for key in keys:
        bst.put(key)

    # Iteration should follow the in-order traversal (ascending order)
    assert list(bst) == sorted(list(set(keys)))