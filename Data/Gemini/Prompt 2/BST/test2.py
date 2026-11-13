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
    bst.put(10)
    assert list(bst.in_order()) == [10]
    assert list(bst.pre_order()) == [10]
    assert list(bst.post_order()) == [10]
    assert list(bst) == [10]


def test_duplicate_insertion():
    bst = BSTSet()
    bst.put(5)
    bst.put(5)
    bst.put(5)
    assert list(bst.in_order()) == [5]
    assert list(bst) == [5]


def test_negative_zero_positive_integers():
    bst = BSTSet()
    keys = [0, -5, 10, -10, 5]
    for k in keys:
        bst.put(k)
    assert list(bst.in_order()) == [-10, -5, 0, 5, 10]


def test_ascending_insertion_skewed():
    bst = BSTSet()
    for k in [1, 2, 3, 4, 5]:
        bst.put(k)
    assert list(bst.in_order()) == [1, 2, 3, 4, 5]
    assert list(bst.pre_order()) == [1, 2, 3, 4, 5]
    assert list(bst.post_order()) == [5, 4, 3, 2, 1]


def test_descending_insertion_skewed():
    bst = BSTSet()
    for k in [5, 4, 3, 2, 1]:
        bst.put(k)
    assert list(bst.in_order()) == [1, 2, 3, 4, 5]
    assert list(bst.pre_order()) == [5, 4, 3, 2, 1]
    assert list(bst.post_order()) == [1, 2, 3, 4, 5]


def test_balanced_tree_traversals():
    bst = BSTSet()
    keys = [10, 5, 15, 2, 7, 20]
    for k in keys:
        bst.put(k)

    assert list(bst.in_order()) == [2, 5, 7, 10, 15, 20]
    assert list(bst.pre_order()) == [10, 5, 2, 7, 15, 20]
    assert list(bst.post_order()) == [2, 7, 5, 20, 15, 10]


def test_missing_children_variations():
    bst = BSTSet()
    bst.put(10)
    bst.put(15)
    bst.put(12)

    assert list(bst.in_order()) == [10, 12, 15]
    assert list(bst.pre_order()) == [10, 15, 12]
    assert list(bst.post_order()) == [12, 15, 10]


def test_uniqueness_and_bst_property():
    bst = BSTSet()
    keys = [15, 10, 20, 8, 12, 17, 25, 10, 15, 25]
    for k in keys:
        bst.put(k)

    # In-order traversal must always yield strictly sorted unique elements
    in_order_res = list(bst.in_order())
    assert in_order_res == sorted(list(set(keys)))
    assert len(in_order_res) == len(set(keys))


def test_iteration():
    bst = BSTSet()
    keys = [3, 1, 4, 1, 5, 9, 2, 6]
    for k in keys:
        bst.put(k)

    assert list(bst) == [1, 2, 3, 4, 5, 6, 9]