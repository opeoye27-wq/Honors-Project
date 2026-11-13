import pytest
from BST import BSTNode, BSTSet


def make_tree(values=None):
    tree = BSTSet()
    if values:
        for value in values:
            tree.put(value)
    return tree


# Empty tree

def test_empty_in_order():
    tree = make_tree()
    assert tree.in_order() == []


def test_empty_pre_order():
    tree = make_tree()
    assert tree.pre_order() == []


def test_empty_post_order():
    tree = make_tree()
    assert tree.post_order() == []


def test_empty_iteration():
    tree = make_tree()
    assert list(tree) == []


# Single node

def test_single_node():
    tree = make_tree([10])
    assert tree.in_order() == [10]
    assert tree.pre_order() == [10]
    assert tree.post_order() == [10]


def test_single_node_iteration():
    tree = make_tree([10])
    assert list(tree) == [10]


# Basic insertion

def test_insert_multiple_values():
    tree = make_tree([10, 5, 15, 3, 7, 12, 20])
    assert tree.in_order() == [3, 5, 7, 10, 12, 15, 20]


def test_insert_smaller_than_root():
    tree = make_tree([10, 5])
    assert tree.in_order() == [5, 10]


def test_insert_larger_than_root():
    tree = make_tree([10, 15])
    assert tree.in_order() == [10, 15]


def test_insert_negative_numbers():
    tree = make_tree([-10, -20, -5, -30, -15])
    assert tree.in_order() == [-30, -20, -15, -10, -5]


def test_insert_zero():
    tree = make_tree([0])
    assert tree.in_order() == [0]


def test_insert_mixed_numbers():
    tree = make_tree([0, -5, 5, -10, 10])
    assert tree.in_order() == [-10, -5, 0, 5, 10]


# Duplicate insertion

def test_duplicate_root():
    tree = make_tree([10, 10])
    assert tree.in_order() == [10]


def test_duplicate_left_child():
    tree = make_tree([10, 5, 15, 5])
    assert tree.in_order() == [5, 10, 15]


def test_duplicate_right_child():
    tree = make_tree([10, 5, 15, 15])
    assert tree.in_order() == [5, 10, 15]


def test_multiple_duplicates():
    tree = make_tree([10, 5, 15, 10, 5, 15, 10])
    assert tree.in_order() == [5, 10, 15]


def test_duplicate_insertion_does_not_change_tree():
    tree = make_tree([10, 5, 15, 3, 7])

    original_in = tree.in_order()
    original_pre = tree.pre_order()
    original_post = tree.post_order()

    for value in [10, 5, 15, 3, 7]:
        tree.put(value)

    assert tree.in_order() == original_in
    assert tree.pre_order() == original_pre
    assert tree.post_order() == original_post


# Ascending and descending insertion

def test_ascending_insertion():
    tree = make_tree([1, 2, 3, 4, 5])

    assert tree.in_order() == [1, 2, 3, 4, 5]
    assert tree.pre_order() == [1, 2, 3, 4, 5]
    assert tree.post_order() == [5, 4, 3, 2, 1]


def test_descending_insertion():
    tree = make_tree([5, 4, 3, 2, 1])

    assert tree.in_order() == [1, 2, 3, 4, 5]
    assert tree.pre_order() == [5, 4, 3, 2, 1]
    assert tree.post_order() == [1, 2, 3, 4, 5]


# Traversal tests

def test_balanced_tree_traversals():
    tree = make_tree([4, 2, 6, 1, 3, 5, 7])

    assert tree.in_order() == [1, 2, 3, 4, 5, 6, 7]
    assert tree.pre_order() == [4, 2, 1, 3, 6, 5, 7]
    assert tree.post_order() == [1, 3, 2, 5, 7, 6, 4]


def test_left_heavy_tree():
    tree = make_tree([10, 8, 6, 4, 2])

    assert tree.in_order() == [2, 4, 6, 8, 10]
    assert tree.pre_order() == [10, 8, 6, 4, 2]
    assert tree.post_order() == [2, 4, 6, 8, 10]


def test_right_heavy_tree():
    tree = make_tree([2, 4, 6, 8, 10])

    assert tree.in_order() == [2, 4, 6, 8, 10]
    assert tree.pre_order() == [2, 4, 6, 8, 10]
    assert tree.post_order() == [10, 8, 6, 4, 2]


def test_tree_with_only_left_child():
    tree = make_tree([10, 5])

    assert tree.in_order() == [5, 10]
    assert tree.pre_order() == [10, 5]
    assert tree.post_order() == [5, 10]


def test_tree_with_only_right_child():
    tree = make_tree([10, 15])

    assert tree.in_order() == [10, 15]
    assert tree.pre_order() == [10, 15]
    assert tree.post_order() == [15, 10]


def test_missing_left_subtree():
    tree = make_tree([10, 15, 20])

    assert tree.in_order() == [10, 15, 20]
    assert tree.pre_order() == [10, 15, 20]
    assert tree.post_order() == [20, 15, 10]


def test_missing_right_subtree():
    tree = make_tree([10, 5, 2])

    assert tree.in_order() == [2, 5, 10]
    assert tree.pre_order() == [10, 5, 2]
    assert tree.post_order() == [2, 5, 10]


def test_internal_missing_children():
    tree = make_tree([10, 5, 15, 3, 12])

    assert tree.in_order() == [3, 5, 10, 12, 15]
    assert tree.pre_order() == [10, 5, 3, 15, 12]
    assert tree.post_order() == [3, 5, 12, 15, 10]


# Iteration

def test_iteration_returns_sorted_values():
    tree = make_tree([8, 3, 10, 1, 6, 14, 4])
    assert list(tree) == [1, 3, 4, 6, 8, 10, 14]


def test_iteration_with_duplicates():
    tree = make_tree([5, 3, 7, 3, 5, 7])
    assert list(tree) == [3, 5, 7]


def test_iteration_matches_in_order():
    tree = make_tree([20, 10, 30, 5, 15, 25, 35])
    assert list(tree) == tree.in_order()


def test_multiple_iterations():
    tree = make_tree([4, 2, 6, 1, 3, 5, 7])

    assert list(tree) == [1, 2, 3, 4, 5, 6, 7]
    assert list(tree) == [1, 2, 3, 4, 5, 6, 7]


# Uniqueness and BST properties

def test_in_order_is_sorted():
    values = [15, 10, 20, 8, 12, 17, 25]
    tree = make_tree(values)

    result = tree.in_order()
    assert result == sorted(result)


def test_no_duplicate_values():
    values = [10, 5, 15, 5, 10, 15, 20, 20]
    tree = make_tree(values)

    result = tree.in_order()
    assert len(result) == len(set(result))


def test_all_unique_values_are_preserved():
    values = [10, 5, 15, 3, 7, 12, 20, -5, 0]
    tree = make_tree(values)

    assert tree.in_order() == sorted(set(values))


def test_all_traversals_contain_same_values():
    tree = make_tree([10, 5, 15, 3, 7, 12, 20])

    assert sorted(tree.in_order()) == sorted(tree.pre_order())
    assert sorted(tree.in_order()) == sorted(tree.post_order())


def test_all_traversals_have_same_length():
    tree = make_tree([10, 5, 15, 3, 7, 12, 20])

    assert len(tree.in_order()) == len(tree.pre_order())
    assert len(tree.pre_order()) == len(tree.post_order())


# Repeated operations

def test_traversals_do_not_modify_tree():
    tree = make_tree([10, 5, 15, 3, 7])
    original = tree.in_order()

    tree.pre_order()
    tree.post_order()
    tree.in_order()

    assert tree.in_order() == original


def test_insert_after_traversal():
    tree = make_tree([10, 5, 15])

    tree.in_order()
    tree.pre_order()
    tree.post_order()

    tree.put(7)

    assert tree.in_order() == [5, 7, 10, 15]


def test_insert_after_iteration():
    tree = make_tree([10, 5, 15])

    list(tree)
    tree.put(7)

    assert tree.in_order() == [5, 7, 10, 15]


# BSTNode tests

def test_bstnode_instantiation():
    node = BSTNode(10)
    assert node is not None


def test_bstnode_stores_key():
    node = BSTNode(10)
    assert node.key == 10


def test_bstnode_initial_children():
    node = BSTNode(10)

    assert node.left is None
    assert node.right is None


def test_bstnode_negative_key():
    node = BSTNode(-10)
    assert node.key == -10


def test_bstnode_zero_key():
    node = BSTNode(0)
    assert node.key == 0


# Large inputs

def test_large_ascending_insertion():
    tree = make_tree(list(range(1000)))
    assert tree.in_order() == list(range(1000))


def test_large_descending_insertion():
    tree = make_tree(list(range(1000, -1, -1)))
    assert tree.in_order() == list(range(1001))


def test_large_number_of_duplicates():
    tree = make_tree([42] * 1000)
    assert tree.in_order() == [42]


def test_large_mixed_input():
    values = list(range(-100, 101))
    tree = make_tree(values)

    assert tree.in_order() == values


# Randomized inputs

def test_randomized_insertion():
    import random

    random.seed(42)
    values = random.sample(range(-1000, 1000), 200)
    tree = make_tree(values)

    assert tree.in_order() == sorted(values)


def test_randomized_insertion_with_duplicates():
    import random

    random.seed(42)
    values = [random.randint(-50, 50) for _ in range(500)]
    tree = make_tree(values)

    assert tree.in_order() == sorted(set(values))


def test_randomized_traversal_consistency():
    import random

    random.seed(123)
    values = random.sample(range(-500, 500), 100)
    tree = make_tree(values)

    assert sorted(tree.pre_order()) == sorted(values)
    assert sorted(tree.post_order()) == sorted(values)
    assert tree.in_order() == sorted(values)