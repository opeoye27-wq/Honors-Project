"""
Unit tests for a Python binary search tree set (BSTNode / BSTSet), using pytest.

ASSUMPTIONS (the description does not specify these, so they are made explicit):

A1. The code under test lives in a module named `BST` and exports `BSTNode`
    and `BSTSet`.
A2. `BSTSet()` takes no arguments and creates an empty set.
A3. `BSTSet.put(key)` inserts a key. Its return value is unspecified, so no
    test asserts on it.
A4. Traversal method names are unspecified. The helper `_call_traversal` tries
    the candidate names listed in TRAVERSAL_NAMES, on both BSTSet and BSTNode.
    Traversals are assumed to return a sequence of KEYS (not nodes). A list,
    tuple, or generator is accepted, because results are wrapped in list().
A5. `BSTNode(key)` creates a leaf node, with attributes `key`, `left`, `right`
    (`left` and `right` are None when the child is absent). `BSTNode.put(key)`
    inserts into the subtree rooted at that node.
A6. `BSTSet` exposes its root node as `._head`, which is None when the set is
    empty. Structural (BST-invariant) tests are skipped if `._head` is missing.
A7. Iterating over a `BSTSet` (`for k in tree` / `iter(tree)`) yields keys in
    ascending (in-order) order. Iteration tests are skipped if `__iter__` is not
    implemented ("where applicable").
A8. Duplicate insertion is silently ignored: no exception, no duplicate node.
A9. Only integers (negative, zero, positive) are specified as keys. Behavior for
    non-integer or mixed-type keys is unspecified, so it is NOT tested.
A10. `len()`, `in`, and delete/remove are not described, so they are NOT tested.
     Uniqueness is verified through the traversals and the tree structure.
A11. Deep-tree tests use 500 nodes to stay under Python's default recursion
     limit (1000) in case the implementation is recursive.
"""

import itertools
import random

import pytest

import importlib

MODULE_NAME = "BST"  # A1
_mod = importlib.import_module(MODULE_NAME)
BSTNode = _mod.BSTNode
BSTSet = _mod.BSTSet

# A4: candidate method names for each traversal order.
TRAVERSAL_NAMES = {
    "in": ["inorder", "in_order", "inorder_traversal", "in_order_traversal"],
    "pre": ["preorder", "pre_order", "preorder_traversal", "pre_order_traversal"],
    "post": ["postorder", "post_order", "postorder_traversal", "post_order_traversal"],
}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _call_traversal(obj, order):
    """Call the traversal `order` ('in' | 'pre' | 'post') on a BSTSet or BSTNode."""
    for name in TRAVERSAL_NAMES[order]:
        method = getattr(obj, name, None)
        if callable(method):
            return list(method())
    pytest.fail(
        f"{type(obj).__name__} has none of the expected {order}-order traversal "
        f"methods: {TRAVERSAL_NAMES[order]} (see assumption A4)"
    )


def inorder(obj):
    return _call_traversal(obj, "in")


def preorder(obj):
    return _call_traversal(obj, "pre")


def postorder(obj):
    return _call_traversal(obj, "post")


def build(keys):
    tree = BSTSet()
    for k in keys:
        tree.put(k)
    return tree


def build_node(root_key, keys):
    node = BSTNode(root_key)
    for k in keys:
        node.put(k)
    return node


def reference_traversals(keys):
    """Independent tuple-based BST model: returns (inorder, preorder, postorder)."""

    def ins(t, k):
        if t is None:
            return (k, None, None)
        key, l, r = t
        if k < key:
            return (key, ins(l, k), r)
        if k > key:
            return (key, l, ins(r, k))
        return t

    def walk(t, order, out):
        if t is None:
            return
        key, l, r = t
        if order == "pre":
            out.append(key)
        walk(l, order, out)
        if order == "in":
            out.append(key)
        walk(r, order, out)
        if order == "post":
            out.append(key)

    root = None
    for k in keys:
        root = ins(root, k)
    res = []
    for order in ("in", "pre", "post"):
        out = []
        walk(root, order, out)
        res.append(out)
    return tuple(res)


def assert_bst_invariant(node, lo=None, hi=None, seen=None):
    """Recursively verify strict BST ordering and key uniqueness (A5, A6)."""
    if seen is None:
        seen = set()
    if node is None:
        return seen
    if lo is not None:
        assert node.key > lo, f"{node.key} violates lower bound {lo}"
    if hi is not None:
        assert node.key < hi, f"{node.key} violates upper bound {hi}"
    assert node.key not in seen, f"duplicate key {node.key} found in tree"
    seen.add(node.key)
    assert_bst_invariant(node.left, lo, node.key, seen)
    assert_bst_invariant(node.right, node.key, hi, seen)
    return seen


def require_root(tree):
    if not hasattr(tree, "_head"):
        pytest.skip("BSTSet does not expose `._head` (assumption A6)")
    return tree._head


def require_iter():
    if not hasattr(BSTSet, "__iter__"):
        pytest.skip("BSTSet does not implement __iter__ (assumption A7)")


# Common sample trees --------------------------------------------------------
#
#            50
#          /    \
#        30      70
#       /  \    /  \
#     20   40  60   80
BALANCED_KEYS = [50, 30, 70, 20, 40, 60, 80]
BALANCED_IN = [20, 30, 40, 50, 60, 70, 80]
BALANCED_PRE = [50, 30, 20, 40, 70, 60, 80]
BALANCED_POST = [20, 40, 30, 60, 80, 70, 50]


# --------------------------------------------------------------------------- #
# Empty tree
# --------------------------------------------------------------------------- #

class TestEmptyTree:
    def test_inorder_empty(self):
        assert inorder(BSTSet()) == []

    def test_preorder_empty(self):
        assert preorder(BSTSet()) == []

    def test_postorder_empty(self):
        assert postorder(BSTSet()) == []

    def test_root_is_none_when_empty(self):
        assert require_root(BSTSet()) is None

    def test_iteration_empty(self):
        require_iter()
        assert list(BSTSet()) == []

    def test_repeated_traversal_of_empty_tree_is_stable(self):
        tree = BSTSet()
        assert inorder(tree) == inorder(tree) == []


# --------------------------------------------------------------------------- #
# Single node
# --------------------------------------------------------------------------- #

class TestSingleNode:
    @pytest.mark.parametrize("key", [0, 1, -1, 42, -42, 10**9, -(10**9)])
    def test_all_traversals_single_key(self, key):
        tree = build([key])
        assert inorder(tree) == [key]
        assert preorder(tree) == [key]
        assert postorder(tree) == [key]

    def test_single_node_has_no_children(self):
        root = require_root(build([5]))
        assert root is not None
        assert root.key == 5
        assert root.left is None
        assert root.right is None

    def test_iteration_single(self):
        require_iter()
        assert list(build([7])) == [7]

    def test_bstnode_constructor_leaf(self):
        node = BSTNode(3)
        assert node.key == 3
        assert node.left is None
        assert node.right is None

    def test_bstnode_single_traversals(self):
        node = BSTNode(3)
        assert inorder(node) == [3]
        assert preorder(node) == [3]
        assert postorder(node) == [3]


# --------------------------------------------------------------------------- #
# Basic insertion and structure
# --------------------------------------------------------------------------- #

class TestInsertionStructure:
    def test_smaller_key_goes_left_of_root(self):
        root = require_root(build([10, 5]))
        assert root.left is not None and root.left.key == 5
        assert root.right is None

    def test_larger_key_goes_right_of_root(self):
        root = require_root(build([10, 15]))
        assert root.right is not None and root.right.key == 15
        assert root.left is None

    def test_both_children(self):
        root = require_root(build([10, 5, 15]))
        assert root.left.key == 5
        assert root.right.key == 15

    def test_first_inserted_key_is_root(self):
        for keys in ([3, 1, 2], [1, 2, 3], [2, 1, 3]):
            assert require_root(build(keys)).key == keys[0]

    def test_deeper_placement(self):
        # 10 -> left 5 -> left 2, right 7 ; 10 -> right 15 -> left 12, right 20
        root = require_root(build([10, 5, 15, 2, 7, 12, 20]))
        assert root.left.left.key == 2
        assert root.left.right.key == 7
        assert root.right.left.key == 12
        assert root.right.right.key == 20

    def test_bst_invariant_on_balanced_tree(self):
        root = require_root(build(BALANCED_KEYS))
        assert assert_bst_invariant(root) == set(BALANCED_KEYS)

    def test_bst_invariant_with_negatives_and_zero(self):
        keys = [0, -5, 5, -10, -1, 1, 10]
        root = require_root(build(keys))
        assert assert_bst_invariant(root) == set(keys)

    def test_node_level_insert_places_children(self):
        node = BSTNode(10)
        node.put(5)
        node.put(15)
        assert node.left.key == 5
        assert node.right.key == 15

    def test_node_level_insert_deep(self):
        node = build_node(10, [5, 3, 7])
        assert node.left.key == 5
        assert node.left.left.key == 3
        assert node.left.right.key == 7
        assert node.right is None

    def test_node_invariant_after_many_inserts(self):
        keys = [8, 3, 10, 1, 6, 14, 4, 7, 13]
        node = build_node(keys[0], keys[1:])
        assert assert_bst_invariant(node) == set(keys)


# --------------------------------------------------------------------------- #
# Traversal order on a balanced tree
# --------------------------------------------------------------------------- #

class TestTraversalsBalanced:
    def test_inorder(self):
        assert inorder(build(BALANCED_KEYS)) == BALANCED_IN

    def test_preorder(self):
        assert preorder(build(BALANCED_KEYS)) == BALANCED_PRE

    def test_postorder(self):
        assert postorder(build(BALANCED_KEYS)) == BALANCED_POST

    def test_node_level_traversals_match(self):
        node = build_node(BALANCED_KEYS[0], BALANCED_KEYS[1:])
        assert inorder(node) == BALANCED_IN
        assert preorder(node) == BALANCED_PRE
        assert postorder(node) == BALANCED_POST

    def test_traversal_does_not_mutate_tree(self):
        tree = build(BALANCED_KEYS)
        before = (inorder(tree), preorder(tree), postorder(tree))
        for _ in range(3):
            inorder(tree)
            preorder(tree)
            postorder(tree)
        after = (inorder(tree), preorder(tree), postorder(tree))
        assert before == after

    def test_traversals_are_permutations_of_same_keys(self):
        tree = build(BALANCED_KEYS)
        assert sorted(preorder(tree)) == sorted(inorder(tree)) == sorted(postorder(tree))

    def test_preorder_first_is_root_postorder_last_is_root(self):
        tree = build(BALANCED_KEYS)
        assert preorder(tree)[0] == BALANCED_KEYS[0]
        assert postorder(tree)[-1] == BALANCED_KEYS[0]

    def test_traversal_returns_keys_not_nodes(self):
        tree = build([2, 1, 3])
        for result in (inorder(tree), preorder(tree), postorder(tree)):
            assert all(isinstance(k, int) for k in result)


# --------------------------------------------------------------------------- #
# Degenerate trees: ascending / descending insertion
# --------------------------------------------------------------------------- #

class TestSkewedTrees:
    def test_ascending_insertion(self):
        tree = build([1, 2, 3, 4, 5])
        assert inorder(tree) == [1, 2, 3, 4, 5]
        assert preorder(tree) == [1, 2, 3, 4, 5]
        assert postorder(tree) == [5, 4, 3, 2, 1]

    def test_descending_insertion(self):
        tree = build([5, 4, 3, 2, 1])
        assert inorder(tree) == [1, 2, 3, 4, 5]
        assert preorder(tree) == [5, 4, 3, 2, 1]
        assert postorder(tree) == [1, 2, 3, 4, 5]

    def test_ascending_forms_right_chain(self):
        node = require_root(build([1, 2, 3, 4]))
        keys = []
        while node is not None:
            assert node.left is None
            keys.append(node.key)
            node = node.right
        assert keys == [1, 2, 3, 4]

    def test_descending_forms_left_chain(self):
        node = require_root(build([4, 3, 2, 1]))
        keys = []
        while node is not None:
            assert node.right is None
            keys.append(node.key)
            node = node.left
        assert keys == [4, 3, 2, 1]

    def test_ascending_negative_to_positive(self):
        tree = build([-3, -2, -1, 0, 1, 2, 3])
        assert inorder(tree) == [-3, -2, -1, 0, 1, 2, 3]
        assert preorder(tree) == [-3, -2, -1, 0, 1, 2, 3]
        assert postorder(tree) == [3, 2, 1, 0, -1, -2, -3]

    def test_descending_positive_to_negative(self):
        tree = build([3, 2, 1, 0, -1, -2, -3])
        assert inorder(tree) == [-3, -2, -1, 0, 1, 2, 3]
        assert preorder(tree) == [3, 2, 1, 0, -1, -2, -3]
        assert postorder(tree) == [-3, -2, -1, 0, 1, 2, 3]

    def test_deep_ascending_chain(self):  # A11
        keys = list(range(500))
        tree = build(keys)
        assert inorder(tree) == keys
        assert preorder(tree) == keys
        assert postorder(tree) == keys[::-1]

    def test_deep_descending_chain(self):  # A11
        keys = list(range(500, 0, -1))
        tree = build(keys)
        assert inorder(tree) == sorted(keys)
        assert preorder(tree) == keys
        assert postorder(tree) == sorted(keys)


# --------------------------------------------------------------------------- #
# Missing left / right children
# --------------------------------------------------------------------------- #

class TestMissingChildren:
    def test_root_with_only_left_child(self):
        tree = build([10, 5])
        assert inorder(tree) == [5, 10]
        assert preorder(tree) == [10, 5]
        assert postorder(tree) == [5, 10]

    def test_root_with_only_right_child(self):
        tree = build([10, 20])
        assert inorder(tree) == [10, 20]
        assert preorder(tree) == [10, 20]
        assert postorder(tree) == [20, 10]

    def test_left_chain_of_three(self):
        tree = build([10, 5, 2])
        assert inorder(tree) == [2, 5, 10]
        assert preorder(tree) == [10, 5, 2]
        assert postorder(tree) == [2, 5, 10]

    def test_right_chain_of_three(self):
        tree = build([10, 15, 20])
        assert inorder(tree) == [10, 15, 20]
        assert preorder(tree) == [10, 15, 20]
        assert postorder(tree) == [20, 15, 10]

    def test_left_child_has_only_right_child(self):
        # 10 -> left 5 -> right 7
        tree = build([10, 5, 7])
        assert inorder(tree) == [5, 7, 10]
        assert preorder(tree) == [10, 5, 7]
        assert postorder(tree) == [7, 5, 10]

    def test_right_child_has_only_left_child(self):
        # 10 -> right 20 -> left 15
        tree = build([10, 20, 15])
        assert inorder(tree) == [10, 15, 20]
        assert preorder(tree) == [10, 20, 15]
        assert postorder(tree) == [15, 20, 10]

    def test_zigzag_tree(self):
        # 10 -> left 5 -> right 8 -> left 6
        tree = build([10, 5, 8, 6])
        assert inorder(tree) == [5, 6, 8, 10]
        assert preorder(tree) == [10, 5, 8, 6]
        assert postorder(tree) == [6, 8, 5, 10]

    def test_asymmetric_tree_full_left_sparse_right(self):
        # 10; left 5 (2, 7); right 20 (no children)
        tree = build([10, 5, 20, 2, 7])
        assert inorder(tree) == [2, 5, 7, 10, 20]
        assert preorder(tree) == [10, 5, 2, 7, 20]
        assert postorder(tree) == [2, 7, 5, 20, 10]

    def test_asymmetric_tree_sparse_left_full_right(self):
        # 10; left 5 (no children); right 20 (15, 25)
        tree = build([10, 5, 20, 15, 25])
        assert inorder(tree) == [5, 10, 15, 20, 25]
        assert preorder(tree) == [10, 5, 20, 15, 25]
        assert postorder(tree) == [5, 15, 25, 20, 10]

    def test_node_level_missing_left(self):
        node = build_node(10, [20])
        assert node.left is None
        assert inorder(node) == [10, 20]
        assert preorder(node) == [10, 20]
        assert postorder(node) == [20, 10]

    def test_node_level_missing_right(self):
        node = build_node(10, [5])
        assert node.right is None
        assert inorder(node) == [5, 10]
        assert preorder(node) == [10, 5]
        assert postorder(node) == [5, 10]


# --------------------------------------------------------------------------- #
# Duplicates / uniqueness
# --------------------------------------------------------------------------- #

class TestDuplicates:
    def test_duplicate_root_only(self):
        tree = build([7, 7, 7])
        assert inorder(tree) == [7]
        assert preorder(tree) == [7]
        assert postorder(tree) == [7]

    def test_duplicate_root_has_no_children(self):
        root = require_root(build([7, 7]))
        assert root.left is None
        assert root.right is None

    def test_duplicates_interleaved(self):
        tree = build([5, 3, 5, 3, 8, 8])
        assert inorder(tree) == [3, 5, 8]
        assert preorder(tree) == [5, 3, 8]
        assert postorder(tree) == [3, 8, 5]

    def test_duplicate_leaf(self):
        tree = build([10, 5, 15, 5, 15])
        assert inorder(tree) == [5, 10, 15]

    def test_duplicate_internal_node(self):
        tree = build([10, 5, 15, 3, 7, 5])
        assert inorder(tree) == [3, 5, 7, 10, 15]
        assert preorder(tree) == [10, 5, 3, 7, 15]

    def test_duplicates_do_not_raise(self):  # A8
        tree = BSTSet()
        for _ in range(5):
            tree.put(1)

    def test_duplicates_zero(self):
        tree = build([0, 0, 0])
        assert inorder(tree) == [0]

    def test_duplicate_negative(self):
        tree = build([-1, -1, -2, -2])
        assert inorder(tree) == [-2, -1]

    def test_reinserting_everything_changes_nothing(self):
        tree = build(BALANCED_KEYS)
        for k in BALANCED_KEYS:
            tree.put(k)
        assert inorder(tree) == BALANCED_IN
        assert preorder(tree) == BALANCED_PRE
        assert postorder(tree) == BALANCED_POST

    def test_duplicate_does_not_alter_structure(self):
        tree = build(BALANCED_KEYS)
        pre_before = preorder(tree)
        tree.put(50)
        tree.put(20)
        tree.put(80)
        assert preorder(tree) == pre_before

    def test_no_duplicate_keys_in_structure(self):
        keys = [4, 2, 6, 2, 4, 6, 1, 3, 5, 7, 1, 7]
        root = require_root(build(keys))
        assert assert_bst_invariant(root) == set(keys)  # raises on duplicate node

    def test_all_traversals_have_unique_keys(self):
        tree = build([3, 3, 1, 1, 2, 2, 3, 1])
        for result in (inorder(tree), preorder(tree), postorder(tree)):
            assert len(result) == len(set(result)) == 3

    def test_node_level_duplicate_ignored(self):
        node = BSTNode(10)
        node.put(10)
        node.put(5)
        node.put(5)
        assert node.left.key == 5
        assert node.left.left is None and node.left.right is None
        assert node.right is None
        assert inorder(node) == [5, 10]


# --------------------------------------------------------------------------- #
# Negative numbers, zero, positives
# --------------------------------------------------------------------------- #

class TestIntegerRange:
    def test_mixed_sign_traversals(self):
        #          0
        #       /     \
        #     -5       5
        #    /  \     /  \
        #  -10  -1   1    10
        tree = build([0, -5, 5, -10, -1, 1, 10])
        assert inorder(tree) == [-10, -5, -1, 0, 1, 5, 10]
        assert preorder(tree) == [0, -5, -10, -1, 5, 1, 10]
        assert postorder(tree) == [-10, -1, -5, 1, 10, 5, 0]

    def test_all_negative(self):
        tree = build([-5, -10, -1, -7, -3])
        assert inorder(tree) == [-10, -7, -5, -3, -1]
        assert preorder(tree) == [-5, -10, -7, -1, -3]
        assert postorder(tree) == [-7, -10, -3, -1, -5]

    def test_negative_root_with_positive_right(self):
        tree = build([-1, 1])
        assert inorder(tree) == [-1, 1]
        assert preorder(tree) == [-1, 1]
        assert postorder(tree) == [1, -1]

    def test_zero_as_root(self):
        root = require_root(build([0, -1, 1]))
        assert root.key == 0
        assert root.left.key == -1
        assert root.right.key == 1

    def test_zero_as_non_root_leaf(self):
        # Guards against falsy-zero bugs (e.g. `if not key`).
        tree = build([5, 0])
        assert inorder(tree) == [0, 5]
        assert preorder(tree) == [5, 0]
        assert postorder(tree) == [0, 5]

    def test_zero_inserted_first_then_others(self):
        tree = build([0, 3, -3])
        assert inorder(tree) == [-3, 0, 3]

    def test_adjacent_negative_boundary(self):
        tree = build([0, -1])
        assert require_root(tree).left.key == -1

    def test_large_magnitude_values(self):
        keys = [0, 10**12, -(10**12), 10**18, -(10**18)]
        tree = build(keys)
        assert inorder(tree) == sorted(keys)

    def test_values_less_than_root_all_left(self):
        root = require_root(build([100, 50, 25, 75, 10]))
        seen = assert_bst_invariant(root.left)
        assert seen == {50, 25, 75, 10}
        assert root.right is None

    def test_values_greater_than_root_all_right(self):
        root = require_root(build([0, 50, 25, 75, 10]))
        seen = assert_bst_invariant(root.right)
        assert seen == {50, 25, 75, 10}
        assert root.left is None

    def test_left_subtree_below_root_right_subtree_above_root(self):
        root = require_root(build([50, 10, 90, 30, 70, 20, 80, 60, 40]))
        assert max(inorder(root.left)) < root.key
        assert min(inorder(root.right)) > root.key


# --------------------------------------------------------------------------- #
# Insertion order variations
# --------------------------------------------------------------------------- #

class TestInsertionOrder:
    def test_inorder_independent_of_insertion_order(self):
        keys = [1, 2, 3, 4]
        for perm in itertools.permutations(keys):
            assert inorder(build(perm)) == keys, f"failed for order {perm}"

    def test_all_permutations_match_reference_model(self):
        keys = [3, 1, 4, 2]
        for perm in itertools.permutations(keys):
            ref_in, ref_pre, ref_post = reference_traversals(perm)
            tree = build(perm)
            assert inorder(tree) == ref_in
            assert preorder(tree) == ref_pre
            assert postorder(tree) == ref_post

    def test_same_keys_different_order_different_shape(self):
        # Same key set, different insertion order -> same in-order, different pre-order.
        a = build([2, 1, 3])
        b = build([1, 2, 3])
        assert inorder(a) == inorder(b) == [1, 2, 3]
        assert preorder(a) == [2, 1, 3]
        assert preorder(b) == [1, 2, 3]

    def test_incremental_insertion_keeps_sorted_inorder(self):
        tree = BSTSet()
        inserted = []
        for k in [5, 2, 8, 1, 9, 3, 7, 4, 6, 0]:
            tree.put(k)
            inserted.append(k)
            assert inorder(tree) == sorted(inserted)

    def test_interleaved_insertions_and_traversals(self):
        tree = BSTSet()
        tree.put(2)
        assert preorder(tree) == [2]
        tree.put(1)
        assert preorder(tree) == [2, 1]
        tree.put(3)
        assert preorder(tree) == [2, 1, 3]
        assert postorder(tree) == [1, 3, 2]

    def test_zigzag_insertion_order(self):
        tree = build([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
        assert inorder(tree) == list(range(1, 11))


# --------------------------------------------------------------------------- #
# Randomized / property-style tests
# --------------------------------------------------------------------------- #

class TestRandomized:
    @pytest.mark.parametrize("seed", [0, 1, 2, 3, 42, 1234])
    def test_random_inserts_match_reference(self, seed):
        rng = random.Random(seed)
        keys = [rng.randint(-100, 100) for _ in range(200)]  # many duplicates
        ref_in, ref_pre, ref_post = reference_traversals(keys)
        tree = build(keys)
        assert inorder(tree) == ref_in == sorted(set(keys))
        assert preorder(tree) == ref_pre
        assert postorder(tree) == ref_post

    @pytest.mark.parametrize("seed", [0, 7, 99])
    def test_random_tree_satisfies_bst_invariant(self, seed):
        rng = random.Random(seed)
        keys = [rng.randint(-1000, 1000) for _ in range(300)]
        root = require_root(build(keys))
        assert assert_bst_invariant(root) == set(keys)

    @pytest.mark.parametrize("seed", [5, 6])
    def test_random_unique_permutation(self, seed):
        rng = random.Random(seed)
        keys = list(range(-50, 51))
        rng.shuffle(keys)
        tree = build(keys)
        assert inorder(tree) == sorted(keys)
        assert len(preorder(tree)) == len(postorder(tree)) == len(keys)


# --------------------------------------------------------------------------- #
# Iteration (A7)
# --------------------------------------------------------------------------- #

class TestIteration:
    def test_iteration_matches_inorder(self):
        require_iter()
        tree = build(BALANCED_KEYS)
        assert list(tree) == BALANCED_IN

    def test_iteration_is_ascending(self):
        require_iter()
        tree = build([9, -3, 4, 0, -8, 7, 2])
        result = list(tree)
        assert result == sorted(result)

    def test_iteration_skips_duplicates(self):
        require_iter()
        assert list(build([2, 2, 1, 1, 3, 3])) == [1, 2, 3]

    def test_iteration_with_for_loop(self):
        require_iter()
        collected = []
        for key in build([3, 1, 2]):
            collected.append(key)
        assert collected == [1, 2, 3]

    def test_iteration_can_be_repeated(self):
        require_iter()
        tree = build([3, 1, 2])
        assert list(tree) == list(tree) == [1, 2, 3]

    def test_iteration_skewed_trees(self):
        require_iter()
        assert list(build([1, 2, 3, 4])) == [1, 2, 3, 4]
        assert list(build([4, 3, 2, 1])) == [1, 2, 3, 4]

    def test_iteration_with_negatives_and_zero(self):
        require_iter()
        assert list(build([0, -2, 2, -1, 1])) == [-2, -1, 0, 1, 2]

    def test_iteration_reflects_later_insertions(self):
        require_iter()
        tree = build([2, 1])
        assert list(tree) == [1, 2]
        tree.put(3)
        assert list(tree) == [1, 2, 3]

    def test_iteration_does_not_mutate(self):
        require_iter()
        tree = build(BALANCED_KEYS)
        list(tree)
        assert preorder(tree) == BALANCED_PRE

    def test_independent_iterators(self):
        require_iter()
        tree = build([1, 2, 3])
        it1, it2 = iter(tree), iter(tree)
        assert next(it1) == 1
        assert next(it1) == 2
        assert next(it2) == 1  # second iterator is not affected by the first

    def test_iterator_exhaustion(self):
        require_iter()
        it = iter(build([1]))
        assert next(it) == 1
        with pytest.raises(StopIteration):
            next(it)

    def test_iteration_equals_sorted_for_random_input(self):
        require_iter()
        rng = random.Random(2024)
        keys = [rng.randint(-500, 500) for _ in range(250)]
        assert list(build(keys)) == sorted(set(keys))


# --------------------------------------------------------------------------- #
# Isolation between instances
# --------------------------------------------------------------------------- #

class TestInstanceIsolation:
    def test_two_sets_do_not_share_state(self):
        a = build([1, 2, 3])
        b = BSTSet()
        assert inorder(b) == []
        b.put(99)
        assert inorder(a) == [1, 2, 3]
        assert inorder(b) == [99]

    def test_new_set_after_populated_set_is_empty(self):
        build([1, 2, 3])
        assert inorder(BSTSet()) == []

    def test_separate_nodes_do_not_share_children(self):
        n1 = BSTNode(10)
        n2 = BSTNode(10)
        n1.put(5)
        assert n2.left is None
        assert inorder(n2) == [10]