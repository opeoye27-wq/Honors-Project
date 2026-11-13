import pytest

from BST import BSTSet, BSTNode


def test_empty_tree():
    bst = BSTSet()
    assert list(bst.in_order()) == []
    assert list(bst.pre_order()) == []
    assert list(bst.post_order()) == []
    assert list(bst) == []


def test_single_node():
    bst = BSTSet()
    bst.put(10)
    assert list(bst.in_order()) == [10]
    assert list(bst.pre_order()) == [10]
    assert list(bst.post_order()) == [10]
    assert list(bst) == [10]


def test_duplicate_keys():
    bst = BSTSet()
    bst.put(5)
    bst.put(5)
    bst.put(5)
    assert list(bst.in_order()) == [5]
    assert list(bst.pre_order()) == [5]
    assert list(bst.post_order()) == [5]


def test_negative_zero_positive_integers():
    bst = BSTSet()
    keys = [0, -5, 10, -10, 5]
    for key in keys:
        bst.put(key)
    assert list(bst.in_order()) == [-10, -5, 0, 5, 10]


def test_ascending_insertion_order():
    bst = BSTSet()
    for i in range(1, 6):
        bst.put(i)
    assert list(bst.in_order()) == [1, 2, 3, 4, 5]
    assert list(bst.pre_order()) == [1, 2, 3, 4, 5]
    assert list(bst.post_order()) == [5, 4, 3, 2, 1]


def test_descending_insertion_order():
    bst = BSTSet()
    for i in range(5, 0, -1):
        bst.put(i)
    assert list(bst.in_order()) == [1, 2, 3, 4, 5]
    assert list(bst.pre_order()) == [5, 4, 3, 2, 1]
    assert list(bst.post_order()) == [1, 2, 3, 4, 5]


def test_traversal_orders_complex():
    bst = BSTSet()
    keys = [10, 5, 15, 2, 7, 12, 20]
    for k in keys:
        bst.put(k)

    assert list(bst.in_order()) == [2, 5, 7, 10, 12, 15, 20]
    assert list(bst.pre_order()) == [10, 5, 2, 7, 15, 12, 20]
    assert list(bst.post_order()) == [2, 7, 5, 12, 20, 15, 10]


def test_missing_children_cases():
    # Tree with only right children / missing left children
    bst_right = BSTSet()
    for k in [10, 15, 20]:
        bst_right.put(k)

    assert list(bst_right.in_order()) == [10, 15, 20]
    assert list(bst_right.pre_order()) == [10, 15, 20]
    assert list(bst_right.post_order()) == [20, 15, 10]

    # Tree with only left children / missing right children
    bst_left = BSTSet()
    for k in [10, 5, 2]:
        bst_left.put(k)

    assert list(bst_left.in_order()) == [2, 5, 10]
    assert list(bst_left.pre_order()) == [10, 5, 2]
    assert list(bst_left.post_order()) == [2, 5, 10]


def test_iteration():
    bst = BSTSet()
    keys = [8, 3, 10, 1, 6, 14]
    for k in keys:
        bst.put(k)

    assert list(bst) == [1, 3, 6, 8, 10, 14]