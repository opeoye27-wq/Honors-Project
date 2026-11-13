import pytest
from BST import BSTSet  # Assuming the implementation is in BST.py


def test_empty_tree():
    bst = BSTSet()
    assert bst.in_order() == []
    assert bst.pre_order() == []
    assert bst.post_order() == []


def test_single_insertion():
    bst = BSTSet()
    bst.put(10)
    assert bst.in_order() == [10]
    assert bst.pre_order() == [10]
    assert bst.post_order() == [10]


def test_normal_insertions_and_traversals():
    bst = BSTSet()
    keys = [5, 3, 7, 2, 4, 6, 8]
    for key in keys:
        bst.put(key)

    # In-order traversal of a BST set should yield sorted unique elements
    assert bst.in_order() == [2, 3, 4, 5, 6, 7, 8]
    # Pre-order traversal check (root -> left -> right)
    assert bst.pre_order() == [5, 3, 2, 4, 7, 6, 8]
    # Post-order traversal check (left -> right -> root)
    assert bst.post_order() == [2, 4, 3, 6, 8, 7, 5]


def test_duplicate_insertions():
    bst = BSTSet()
    keys = [5, 3, 5, 3, 7, 7]
    for key in keys:
        bst.put(key)

    # As a set, duplicates should be ignored
    assert bst.in_order() == [3, 5, 7]


def test_negative_and_zero_inputs():
    bst = BSTSet()
    keys = [0, -5, 5, -10, 10]
    for key in keys:
        bst.put(key)

    assert bst.in_order() == [-10, -5, 0, 5, 10]


def test_degenerate_tree_left_skewed():
    bst = BSTSet()
    keys = [5, 4, 3, 2, 1]
    for key in keys:
        bst.put(key)

    assert bst.in_order() == [1, 2, 3, 4, 5]
    assert bst.pre_order() == [5, 4, 3, 2, 1]
    assert bst.post_order() == [1, 2, 3, 4, 5]


def test_degenerate_tree_right_skewed():
    bst = BSTSet()
    keys = [1, 2, 3, 4, 5]
    for key in keys:
        bst.put(key)

    assert bst.in_order() == [1, 2, 3, 4, 5]
    assert bst.pre_order() == [1, 2, 3, 4, 5]
    assert bst.post_order() == [5, 4, 3, 2, 1]