import pytest
from BST import BSTSet, BSTNode

# Assumption: The implementation exposes BSTNode and BSTSet classes.
# Assumption: BSTSet supports put(key), traversal methods named
# in_order(), pre_order(), and post_order(), and iteration through __iter__.
# If the actual method names differ, adjust the test calls accordingly.
#
# Assumption: Traversals return lists (or another iterable containing
# the traversal results). Iteration order is not specified, so iteration
# tests check membership and uniqueness rather than a particular order.
#
# Assumption: The public insertion method is BSTSet.put(key).
# No behavior is assumed for invalid key types because the description
# specifies integer keys only.


def make_tree(values):
    """Create a BSTSet and insert the supplied values."""
    tree = BSTSet()
    for value in values:
        tree.put(value)
    return tree


def assert_bst_properties(node, lower=None, upper=None):
    """Recursively verify BST ordering and node uniqueness."""
    if node is None:
        return

    assert lower is None or node.key > lower
    assert upper is None or node.key < upper

    assert_bst_properties(node.left, lower, node.key)
    assert_bst_properties(node.right, node.key, upper)


def collect_all_nodes(node):
    """Collect all nodes using recursive traversal."""
    if node is None:
        return []

    return (
        [node]
        + collect_all_nodes(node.left)
        + collect_all_nodes(node.right)
    )


def test_empty_tree():
    tree = BSTSet()

    assert list(tree.in_order()) == []
    assert list(tree.pre_order()) == []
    assert list(tree.post_order()) == []


def test_insert_single_node():
    tree = make_tree([10])

    assert list(tree.in_order()) == [10]
    assert list(tree.pre_order()) == [10]
    assert list(tree.post_order()) == [10]


def test_insert_multiple_nodes():
    tree = make_tree([10, 5, 15, 3, 7, 12, 18])

    assert list(tree.in_order()) == [3, 5, 7, 10, 12, 15, 18]
    assert list(tree.pre_order()) == [10, 5, 3, 7, 15, 12, 18]
    assert list(tree.post_order()) == [3, 7, 5, 12, 18, 15, 10]


def test_insert_duplicate_root():
    tree = make_tree([10, 10, 10])

    assert list(tree.in_order()) == [10]
    assert len(collect_all_nodes(tree._head)) == 1


def test_insert_duplicate_non_root():
    tree = make_tree([10, 5, 15, 5, 15, 5])

    assert list(tree.in_order()) == [5, 10, 15]
    assert len(collect_all_nodes(tree._head)) == 3


def test_insert_all_duplicate_values():
    tree = make_tree([7, 7, 7, 7, 7, 7])

    assert list(tree.in_order()) == [7]
    assert list(tree.pre_order()) == [7]
    assert list(tree.post_order()) == [7]


def test_insert_negative_zero_and_positive_values():
    tree = make_tree([-10, 0, 10, -5, 5, -20, 20])

    assert list(tree.in_order()) == [-20, -10, -5, 0, 5, 10, 20]


def test_insert_negative_root():
    tree = make_tree([-10, -20, -5, 0, 10])

    assert list(tree.in_order()) == [-20, -10, -5, 0, 10]


def test_insert_zero_as_root():
    tree = make_tree([0, -10, 10, -5, 5])

    assert list(tree.in_order()) == [-10, -5, 0, 5, 10]


def test_insert_ascending_order():
    values = [1, 2, 3, 4, 5, 6, 7]
    tree = make_tree(values)

    assert list(tree.in_order()) == values
    assert list(tree.pre_order()) == values
    assert list(tree.post_order()) == list(reversed(values))


def test_insert_descending_order():
    values = [7, 6, 5, 4, 3, 2, 1]
    tree = make_tree(values)

    assert list(tree.in_order()) == sorted(values)
    assert list(tree.pre_order()) == values
    assert list(tree.post_order()) == list(reversed(values))


def test_insert_values_smaller_than_root():
    tree = make_tree([50, 40, 30, 20, 10])

    assert list(tree.in_order()) == [10, 20, 30, 40, 50]


def test_insert_values_larger_than_root():
    tree = make_tree([50, 60, 70, 80, 90])

    assert list(tree.in_order()) == [50, 60, 70, 80, 90]


def test_insert_values_on_both_sides_of_root():
    tree = make_tree([50, 25, 75, 10, 40, 60, 90])

    assert list(tree.in_order()) == [10, 25, 40, 50, 60, 75, 90]
    assert list(tree.pre_order()) == [50, 25, 10, 40, 75, 60, 90]
    assert list(tree.post_order()) == [10, 40, 25, 60, 90, 75, 50]


def test_tree_with_only_left_children():
    tree = make_tree([50, 40, 30, 20])

    assert list(tree.in_order()) == [20, 30, 40, 50]
    assert list(tree.pre_order()) == [50, 40, 30, 20]
    assert list(tree.post_order()) == [20, 30, 40, 50]


def test_tree_with_only_right_children():
    tree = make_tree([10, 20, 30, 40])

    assert list(tree.in_order()) == [10, 20, 30, 40]
    assert list(tree.pre_order()) == [10, 20, 30, 40]
    assert list(tree.post_order()) == [40, 30, 20, 10]


def test_tree_with_missing_left_children():
    tree = make_tree([10, 20, 30])

    assert list(tree.in_order()) == [10, 20, 30]
    assert list(tree.pre_order()) == [10, 20, 30]
    assert list(tree.post_order()) == [30, 20, 10]


def test_tree_with_missing_right_children():
    tree = make_tree([30, 20, 10])

    assert list(tree.in_order()) == [10, 20, 30]
    assert list(tree.pre_order()) == [30, 20, 10]
    assert list(tree.post_order()) == [10, 20, 30]


def test_tree_with_alternating_missing_children():
    tree = make_tree([50, 30, 70, 20, 40, 60])

    assert list(tree.in_order()) == [20, 30, 40, 50, 60, 70]
    assert list(tree.pre_order()) == [50, 30, 20, 40, 70, 60]
    assert list(tree.post_order()) == [20, 40, 30, 60, 70, 50]


def test_inorder_traversal_is_sorted():
    tree = make_tree([15, 8, 22, 4, 12, 18, 30, 2, 6])

    result = list(tree.in_order())

    assert result == sorted(result)


def test_preorder_traversal_starts_with_root():
    tree = make_tree([15, 8, 22, 4, 12])

    assert list(tree.pre_order())[0] == 15


def test_postorder_traversal_ends_with_root():
    tree = make_tree([15, 8, 22, 4, 12])

    assert list(tree.post_order())[-1] == 15


def test_all_traversals_contain_same_elements():
    tree = make_tree([50, 25, 75, 10, 30, 60, 90])

    inorder = list(tree.in_order())
    preorder = list(tree.pre_order())
    postorder = list(tree.post_order())

    assert sorted(inorder) == sorted(preorder)
    assert sorted(preorder) == sorted(postorder)


def test_traversals_do_not_contain_duplicates():
    tree = make_tree([10, 5, 15, 5, 10, 15, 20])

    for traversal in (
        tree.in_order(),
        tree.pre_order(),
        tree.post_order(),
    ):
        result = list(traversal)
        assert len(result) == len(set(result))


def test_traversal_does_not_modify_tree():
    tree = make_tree([10, 5, 15, 3, 7])

    before = (
        list(tree.in_order()),
        list(tree.pre_order()),
        list(tree.post_order()),
    )

    list(tree.in_order())
    list(tree.pre_order())
    list(tree.post_order())

    after = (
        list(tree.in_order()),
        list(tree.pre_order()),
        list(tree.post_order()),
    )

    assert before == after


def test_repeated_traversals_produce_same_results():
    tree = make_tree([10, 5, 15, 3, 7])

    assert list(tree.in_order()) == list(tree.in_order())
    assert list(tree.pre_order()) == list(tree.pre_order())
    assert list(tree.post_order()) == list(tree.post_order())


def test_bst_property_after_insertions():
    tree = make_tree([50, 25, 75, 10, 30, 60, 90])

    assert_bst_properties(tree._head)


def test_bst_property_after_duplicate_insertions():
    tree = make_tree([50, 25, 75, 25, 50, 75, 10, 90])

    assert_bst_properties(tree._head)


def test_bst_property_after_ascending_insertions():
    tree = make_tree(list(range(1, 51)))

    assert_bst_properties(tree._head)


def test_bst_property_after_descending_insertions():
    tree = make_tree(list(range(50, 0, -1)))

    assert_bst_properties(tree._head)


def test_node_count_matches_unique_insertions():
    values = [10, 5, 15, 5, 10, 20, 15, 25]
    tree = make_tree(values)

    assert len(collect_all_nodes(tree._head)) == len(set(values))


def test_root_remains_first_inserted_value():
    tree = make_tree([50, 25, 75, 10, 90])

    assert tree._head.key == 50


def test_large_number_of_unique_insertions():
    values = list(range(-500, 501))
    tree = make_tree(values)

    assert list(tree.in_order()) == values
    assert len(collect_all_nodes(tree._head)) == 1001


def test_large_number_of_duplicate_insertions():
    values = [42] * 1000
    tree = make_tree(values)

    assert list(tree.in_order()) == [42]
    assert len(collect_all_nodes(tree._head)) == 1


def test_iteration_on_empty_tree():
    tree = BSTSet()

    assert list(tree) == []


def test_iteration_on_single_node():
    tree = make_tree([42])

    assert list(tree) == [42]


def test_iteration_contains_all_inserted_values():
    values = [50, 25, 75, 10, 30, 60, 90]
    tree = make_tree(values)

    result = list(tree)

    assert set(result) == set(values)
    assert len(result) == len(values)


def test_iteration_does_not_repeat_duplicate_values():
    tree = make_tree([10, 5, 15, 5, 10, 15])

    result = list(tree)

    assert len(result) == len(set(result))


def test_iteration_matches_inorder_traversal():
    # Assumption: BSTSet iteration follows in-order traversal.
    tree = make_tree([50, 25, 75, 10, 30, 60, 90])

    assert list(tree) == list(tree.in_order())


def test_iteration_can_be_repeated():
    tree = make_tree([10, 5, 15, 3, 7])

    assert list(tree) == list(tree)