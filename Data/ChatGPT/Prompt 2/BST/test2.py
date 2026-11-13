import pytest
from BST import BSTSet, BSTNode

# Assumption:
# BSTSet provides put(key), __iter__(), and traversal methods
# named in_order(), pre_order(), and post_order().
# BSTNode supports equivalent traversal operations.
#
# If the actual method names differ, adjust the method names in
# the tests accordingly.
#
# Assumption:
# Traversal methods return iterables of keys or lists of keys.


@pytest.fixture
def empty_tree():
    return BSTSet()


@pytest.fixture
def populated_tree():
    tree = BSTSet()
    for key in [50, 30, 70, 20, 40, 60, 80]:
        tree.put(key)
    return tree


# -------------------------
# Empty Tree Tests
# -------------------------

def test_empty_tree_in_order(empty_tree):
    assert list(empty_tree.in_order()) == []


def test_empty_tree_pre_order(empty_tree):
    assert list(empty_tree.pre_order()) == []


def test_empty_tree_post_order(empty_tree):
    assert list(empty_tree.post_order()) == []


def test_empty_tree_iteration(empty_tree):
    assert list(empty_tree) == []


# -------------------------
# Single Node Tests
# -------------------------

def test_insert_single_node(empty_tree):
    empty_tree.put(10)

    assert list(empty_tree.in_order()) == [10]


def test_single_node_all_traversals(empty_tree):
    empty_tree.put(10)

    assert list(empty_tree.in_order()) == [10]
    assert list(empty_tree.pre_order()) == [10]
    assert list(empty_tree.post_order()) == [10]


def test_insert_single_node_iteration(empty_tree):
    empty_tree.put(10)

    assert list(empty_tree) == [10]


# -------------------------
# Basic Insertion Tests
# -------------------------

def test_insert_multiple_keys(empty_tree):
    keys = [50, 30, 70, 20, 40, 60, 80]

    for key in keys:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [20, 30, 40, 50, 60, 70, 80]


def test_insert_smaller_than_root(empty_tree):
    empty_tree.put(50)
    empty_tree.put(25)

    assert list(empty_tree.in_order()) == [25, 50]


def test_insert_larger_than_root(empty_tree):
    empty_tree.put(50)
    empty_tree.put(75)

    assert list(empty_tree.in_order()) == [50, 75]


def test_insert_negative_keys(empty_tree):
    for key in [-10, -30, -5, -20, -1]:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [-30, -20, -10, -5, -1]


def test_insert_zero(empty_tree):
    empty_tree.put(0)

    assert list(empty_tree.in_order()) == [0]


def test_insert_negative_zero_and_positive_keys(empty_tree):
    keys = [-10, 0, 10, -5, 5]

    for key in keys:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [-10, -5, 0, 5, 10]


# -------------------------
# Duplicate Insertion Tests
# -------------------------

def test_insert_duplicate_key(empty_tree):
    empty_tree.put(10)
    empty_tree.put(10)

    assert list(empty_tree.in_order()) == [10]


def test_insert_duplicate_multiple_times(empty_tree):
    for _ in range(10):
        empty_tree.put(25)

    assert list(empty_tree.in_order()) == [25]


def test_insert_duplicates_in_populated_tree(populated_tree):
    for key in [50, 30, 70, 20, 40, 60, 80]:
        populated_tree.put(key)

    assert list(populated_tree.in_order()) == [
        20, 30, 40, 50, 60, 70, 80
    ]


def test_duplicate_insertion_preserves_all_traversals(empty_tree):
    for key in [50, 30, 70, 30, 50, 70]:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [30, 50, 70]
    assert list(empty_tree.pre_order()) == [50, 30, 70]
    assert list(empty_tree.post_order()) == [30, 70, 50]


# -------------------------
# Ascending and Descending Insertion
# -------------------------

def test_insert_ascending_order(empty_tree):
    for key in [1, 2, 3, 4, 5]:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [1, 2, 3, 4, 5]


def test_insert_descending_order(empty_tree):
    for key in [5, 4, 3, 2, 1]:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [1, 2, 3, 4, 5]


def test_ascending_insertion_pre_order(empty_tree):
    for key in [1, 2, 3, 4]:
        empty_tree.put(key)

    assert list(empty_tree.pre_order()) == [1, 2, 3, 4]


def test_ascending_insertion_post_order(empty_tree):
    for key in [1, 2, 3, 4]:
        empty_tree.put(key)

    assert list(empty_tree.post_order()) == [4, 3, 2, 1]


def test_descending_insertion_pre_order(empty_tree):
    for key in [4, 3, 2, 1]:
        empty_tree.put(key)

    assert list(empty_tree.pre_order()) == [4, 3, 2, 1]


def test_descending_insertion_post_order(empty_tree):
    for key in [4, 3, 2, 1]:
        empty_tree.put(key)

    assert list(empty_tree.post_order()) == [1, 2, 3, 4]


# -------------------------
# Traversal Tests
# -------------------------

def test_in_order_traversal(populated_tree):
    assert list(populated_tree.in_order()) == [
        20, 30, 40, 50, 60, 70, 80
    ]


def test_pre_order_traversal(populated_tree):
    assert list(populated_tree.pre_order()) == [
        50, 30, 20, 40, 70, 60, 80
    ]


def test_post_order_traversal(populated_tree):
    assert list(populated_tree.post_order()) == [
        20, 40, 30, 60, 80, 70, 50
    ]


def test_traversals_with_missing_left_children(empty_tree):
    for key in [10, 20, 30]:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [10, 20, 30]
    assert list(empty_tree.pre_order()) == [10, 20, 30]
    assert list(empty_tree.post_order()) == [30, 20, 10]


def test_traversals_with_missing_right_children(empty_tree):
    for key in [30, 20, 10]:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [10, 20, 30]
    assert list(empty_tree.pre_order()) == [30, 20, 10]
    assert list(empty_tree.post_order()) == [10, 20, 30]


def test_traversals_with_only_left_subtree(empty_tree):
    for key in [50, 30, 20, 10]:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [10, 20, 30, 50]
    assert list(empty_tree.pre_order()) == [50, 30, 20, 10]
    assert list(empty_tree.post_order()) == [10, 20, 30, 50]


def test_traversals_with_only_right_subtree(empty_tree):
    for key in [10, 20, 30, 40]:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [10, 20, 30, 40]
    assert list(empty_tree.pre_order()) == [10, 20, 30, 40]
    assert list(empty_tree.post_order()) == [40, 30, 20, 10]


def test_traversals_with_alternating_children(empty_tree):
    for key in [50, 30, 70, 40, 60, 35, 65]:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == [
        30, 35, 40, 50, 60, 65, 70
    ]

    assert list(empty_tree.pre_order()) == [
        50, 30, 40, 35, 70, 60, 65
    ]

    assert list(empty_tree.post_order()) == [
        35, 40, 30, 65, 60, 70, 50
    ]


# -------------------------
# Iteration Tests
# -------------------------

def test_iteration_returns_sorted_keys(populated_tree):
    assert list(populated_tree) == [
        20, 30, 40, 50, 60, 70, 80
    ]


def test_iteration_after_insertions(empty_tree):
    for key in [8, 3, 10, 1, 6]:
        empty_tree.put(key)

    assert list(empty_tree) == [1, 3, 6, 8, 10]


def test_iteration_after_duplicate_insertions(empty_tree):
    for key in [5, 3, 5, 7, 3, 7]:
        empty_tree.put(key)

    assert list(empty_tree) == [3, 5, 7]


def test_iteration_does_not_modify_tree(populated_tree):
    expected = [20, 30, 40, 50, 60, 70, 80]

    list(populated_tree)

    assert list(populated_tree.in_order()) == expected


def test_multiple_iterations_produce_same_result(populated_tree):
    first = list(populated_tree)
    second = list(populated_tree)

    assert first == second


# -------------------------
# Uniqueness and BST Property Tests
# -------------------------

def test_all_inserted_keys_are_unique(empty_tree):
    keys = [10, 5, 15, 5, 10, 15, 20, 20]

    for key in keys:
        empty_tree.put(key)

    result = list(empty_tree.in_order())

    assert len(result) == len(set(result))


def test_in_order_traversal_is_strictly_increasing(populated_tree):
    result = list(populated_tree.in_order())

    assert all(
        result[i] < result[i + 1]
        for i in range(len(result) - 1)
    )


def test_all_unique_inserted_keys_are_preserved(empty_tree):
    keys = [15, 10, 20, 5, 12, 18, 25]

    for key in keys:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == sorted(set(keys))


def test_root_remains_first_inserted_key(empty_tree):
    empty_tree.put(50)

    for key in [30, 70, 20, 40]:
        empty_tree.put(key)

    assert empty_tree._head.key == 50


def test_left_subtree_contains_smaller_keys(populated_tree):
    root = populated_tree._head

    assert root.left.key < root.key


def test_right_subtree_contains_larger_keys(populated_tree):
    root = populated_tree._head

    assert root.right.key > root.key


def test_recursive_bst_property(populated_tree):
    def check_bst(node, lower=float("-inf"), upper=float("inf")):
        if node is None:
            return True

        if not lower < node.key < upper:
            return False

        return (
            check_bst(node.left, lower, node.key)
            and check_bst(node.right, node.key, upper)
        )

    assert check_bst(populated_tree._head)


# -------------------------
# Larger and Unusual Input Tests
# -------------------------

def test_insert_large_positive_integer(empty_tree):
    value = 10**100
    empty_tree.put(value)

    assert list(empty_tree.in_order()) == [value]


def test_insert_large_negative_integer(empty_tree):
    value = -(10**100)
    empty_tree.put(value)

    assert list(empty_tree.in_order()) == [value]


def test_insert_consecutive_integers(empty_tree):
    keys = list(range(-100, 101))

    for key in keys:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == keys


def test_insert_many_randomized_order_keys(empty_tree):
    keys = [42, -10, 0, 17, 99, -50, 3, 25, -1, 70]

    for key in keys:
        empty_tree.put(key)

    assert list(empty_tree.in_order()) == sorted(keys)


def test_repeated_insertion_does_not_change_tree_structure(empty_tree):
    for key in [50, 25, 75, 10, 35]:
        empty_tree.put(key)

    original_pre_order = list(empty_tree.pre_order())
    original_post_order = list(empty_tree.post_order())

    for key in [50, 25, 75, 10, 35]:
        empty_tree.put(key)

    assert list(empty_tree.pre_order()) == original_pre_order
    assert list(empty_tree.post_order()) == original_post_order


# -------------------------
# BSTNode Tests
# -------------------------

def test_bstnode_single_node_traversals():
    node = BSTNode(10)

    assert list(node.in_order()) == [10]
    assert list(node.pre_order()) == [10]
    assert list(node.post_order()) == [10]


def test_bstnode_left_child_traversals():
    root = BSTNode(10)
    root.left = BSTNode(5)

    assert list(root.in_order()) == [5, 10]
    assert list(root.pre_order()) == [10, 5]
    assert list(root.post_order()) == [5, 10]


def test_bstnode_right_child_traversals():
    root = BSTNode(10)
    root.right = BSTNode(15)

    assert list(root.in_order()) == [10, 15]
    assert list(root.pre_order()) == [10, 15]
    assert list(root.post_order()) == [15, 10]


def test_bstnode_both_children_traversals():
    root = BSTNode(10)
    root.left = BSTNode(5)
    root.right = BSTNode(15)

    assert list(root.in_order()) == [5, 10, 15]
    assert list(root.pre_order()) == [10, 5, 15]
    assert list(root.post_order()) == [5, 15, 10]


# -------------------------
# Invalid Input Tests
# -------------------------

@pytest.mark.parametrize(
    "invalid_key",
    [None, "10", 10.5, [], {}, set()]
)
def test_insert_invalid_key(empty_tree, invalid_key):
    """
    Assumption: The implementation accepts integer keys only.

    The description explicitly specifies integer support but does not
    define how non-integer inputs should be handled. These tests assume
    invalid types raise TypeError.
    """
    with pytest.raises(TypeError):
        empty_tree.put(invalid_key)


# -------------------------
# Traversal Consistency Tests
# -------------------------

def test_all_traversals_contain_same_keys(populated_tree):
    in_order = list(populated_tree.in_order())
    pre_order = list(populated_tree.pre_order())
    post_order = list(populated_tree.post_order())

    assert sorted(in_order) == sorted(pre_order)
    assert sorted(in_order) == sorted(post_order)


def test_all_traversals_have_same_number_of_elements(populated_tree):
    in_order = list(populated_tree.in_order())
    pre_order = list(populated_tree.pre_order())
    post_order = list(populated_tree.post_order())

    assert len(in_order) == len(pre_order) == len(post_order)


def test_traversal_results_contain_no_duplicates(populated_tree):
    for traversal in [
        populated_tree.in_order(),
        populated_tree.pre_order(),
        populated_tree.post_order()
    ]:
        result = list(traversal)
        assert len(result) == len(set(result))


def test_traversal_results_after_mixed_insertions(empty_tree):
    keys = [100, 50, 150, 25, 75, 125, 175, 50, 100, 125]

    for key in keys:
        empty_tree.put(key)

    expected = sorted(set(keys))

    assert list(empty_tree.in_order()) == expected
    assert sorted(empty_tree.pre_order()) == expected
    assert sorted(empty_tree.post_order()) == expected
    assert list(empty_tree) == expected