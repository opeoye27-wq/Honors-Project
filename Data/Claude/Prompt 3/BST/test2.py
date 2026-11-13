"""
pytest unit tests for a binary search tree (BST) set.

ASSUMPTIONS (the description does not specify these, so they are made explicit
and configurable in the CONFIG block below):

 A1. Module / class names: `BST.BSTSet`. Change MODULE_NAME / CLASS_NAME.
 A2. Construction: `BSTSet()` takes no arguments and creates an empty set.
 A3. Insertion: `put(key)` adds a key. Its return value is not tested.
 A4. Traversals: `in_order()`, `pre_order()`, `post_order()` return the keys in
     that order. They may return a list or any iterable; tests wrap the result
     in list().
 A5. "Set" semantics: inserting a duplicate key leaves the tree unchanged
     (no duplicate in any traversal).
 A6. Keys are mutually comparable (ints, floats, strings). Keys are placed
     using standard BST rules: smaller to the left, larger to the right.
 A7. Optional methods `__len__` and `__contains__` may not exist. Tests that
     use them are skipped if they are missing.
 A8. Invalid keys: inserting None, or a key not comparable with existing keys
     (e.g. str into an int tree), raises TypeError. Controlled by
     EXPECT_TYPEERROR_ON_INVALID. If the implementation raises a different
     exception, change INVALID_KEY_EXCEPTION.
 A9. Traversal results are independent snapshots: mutating a returned list
     must not alter the tree.
 A10. Very deep (degenerate) trees may exceed Python's recursion limit if the
     implementation is recursive. That test is marked xfail (non-strict)
     rather than treated as a definite failure.
 A11. NaN keys, and the exact return value of put, are unspecified and
     are not tested.
"""

import importlib
import random
import sys

import pytest

# --------------------------------------------------------------------------
# CONFIG: adjust to match the program under test
# --------------------------------------------------------------------------
MODULE_NAME = "BST"
CLASS_NAME = "BSTSet"
INSERT = "put"
INORDER = "in_order"
PREORDER = "pre_order"
POSTORDER = "post_order"

EXPECT_TYPEERROR_ON_INVALID = True
INVALID_KEY_EXCEPTION = TypeError

_module = importlib.import_module(MODULE_NAME)
BSTClass = getattr(_module, CLASS_NAME)


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def build(keys=()):
    tree = BSTClass()
    for k in keys:
        getattr(tree, INSERT)(k)
    return tree


def inorder(tree):
    return list(getattr(tree, INORDER)())


def preorder(tree):
    return list(getattr(tree, PREORDER)())


def postorder(tree):
    return list(getattr(tree, POSTORDER)())


class _RefNode:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def _ref_insert(root, key):
    if root is None:
        return _RefNode(key)
    if key < root.key:
        root.left = _ref_insert(root.left, key)
    elif key > root.key:
        root.right = _ref_insert(root.right, key)
    return root  # equal: ignored (set semantics)


def _ref_pre(n):
    return [] if n is None else [n.key] + _ref_pre(n.left) + _ref_pre(n.right)


def _ref_in(n):
    return [] if n is None else _ref_in(n.left) + [n.key] + _ref_in(n.right)


def _ref_post(n):
    return [] if n is None else _ref_post(n.left) + _ref_post(n.right) + [n.key]


def reference(keys):
    root = None
    for k in keys:
        root = _ref_insert(root, k)
    return _ref_pre(root), _ref_in(root), _ref_post(root)


# Canonical tree used in many tests:
#
#           5
#         /   \
#        3     8
#       / \   / \
#      1   4 7   9
CANON_KEYS = [5, 3, 8, 1, 4, 7, 9]
CANON_PRE = [5, 3, 1, 4, 8, 7, 9]
CANON_IN = [1, 3, 4, 5, 7, 8, 9]
CANON_POST = [1, 4, 3, 7, 9, 8, 5]


# --------------------------------------------------------------------------
# Construction / empty tree
# --------------------------------------------------------------------------
class TestEmptyTree:
    def test_can_construct_empty_tree(self):
        assert BSTClass() is not None

    def test_inorder_of_empty_tree_is_empty(self):
        assert inorder(build()) == []

    def test_preorder_of_empty_tree_is_empty(self):
        assert preorder(build()) == []

    def test_postorder_of_empty_tree_is_empty(self):
        assert postorder(build()) == []

    def test_traversing_empty_tree_repeatedly_is_stable(self):
        tree = build()
        for _ in range(3):
            assert inorder(tree) == []
            assert preorder(tree) == []
            assert postorder(tree) == []

    def test_empty_trees_are_independent_instances(self):
        a, b = build(), build()
        getattr(a, INSERT)(1)
        assert inorder(b) == []


# --------------------------------------------------------------------------
# Single and small trees
# --------------------------------------------------------------------------
class TestSmallTrees:
    def test_single_element_all_traversals(self):
        tree = build([42])
        assert inorder(tree) == [42]
        assert preorder(tree) == [42]
        assert postorder(tree) == [42]

    def test_two_elements_right_child(self):
        tree = build([1, 2])
        assert inorder(tree) == [1, 2]
        assert preorder(tree) == [1, 2]
        assert postorder(tree) == [2, 1]

    def test_two_elements_left_child(self):
        tree = build([2, 1])
        assert inorder(tree) == [1, 2]
        assert preorder(tree) == [2, 1]
        assert postorder(tree) == [1, 2]

    def test_three_elements_balanced(self):
        tree = build([2, 1, 3])
        assert inorder(tree) == [1, 2, 3]
        assert preorder(tree) == [2, 1, 3]
        assert postorder(tree) == [1, 3, 2]

    def test_three_elements_zigzag_left_right(self):
        # 3 -> left 1 -> right 2
        tree = build([3, 1, 2])
        assert inorder(tree) == [1, 2, 3]
        assert preorder(tree) == [3, 1, 2]
        assert postorder(tree) == [2, 1, 3]

    def test_three_elements_zigzag_right_left(self):
        # 1 -> right 3 -> left 2
        tree = build([1, 3, 2])
        assert inorder(tree) == [1, 2, 3]
        assert preorder(tree) == [1, 3, 2]
        assert postorder(tree) == [2, 3, 1]


# --------------------------------------------------------------------------
# Traversal order on a known tree
# --------------------------------------------------------------------------
class TestKnownTraversals:
    def test_inorder_canonical(self):
        assert inorder(build(CANON_KEYS)) == CANON_IN

    def test_preorder_canonical(self):
        assert preorder(build(CANON_KEYS)) == CANON_PRE

    def test_postorder_canonical(self):
        assert postorder(build(CANON_KEYS)) == CANON_POST

    def test_inorder_is_sorted_ascending(self):
        keys = [50, 20, 70, 10, 30, 60, 80, 25, 35]
        assert inorder(build(keys)) == sorted(keys)

    def test_traversals_contain_same_elements(self):
        tree = build(CANON_KEYS)
        assert sorted(preorder(tree)) == CANON_IN
        assert sorted(postorder(tree)) == CANON_IN

    def test_preorder_first_element_is_first_inserted_key(self):
        # The first inserted key is the root, and root comes first in preorder.
        assert preorder(build([10, 5, 15, 1]))[0] == 10

    def test_postorder_last_element_is_first_inserted_key(self):
        # The root is always visited last in postorder.
        assert postorder(build([10, 5, 15, 1]))[-1] == 10


# --------------------------------------------------------------------------
# Insertion order effects
# --------------------------------------------------------------------------
class TestInsertionOrder:
    def test_inorder_independent_of_insertion_order(self):
        keys = [5, 3, 8, 1, 4, 7, 9]
        for perm in ([1, 3, 4, 5, 7, 8, 9], [9, 8, 7, 5, 4, 3, 1], [4, 9, 1, 7, 3, 8, 5]):
            assert inorder(build(perm)) == sorted(keys)

    def test_preorder_depends_on_insertion_order(self):
        # Same key set, different shapes -> different preorder.
        assert preorder(build([1, 2, 3])) == [1, 2, 3]
        assert preorder(build([2, 1, 3])) == [2, 1, 3]
        assert preorder(build([3, 2, 1])) == [3, 2, 1]

    def test_ascending_insertion_is_right_skewed(self):
        keys = list(range(1, 8))
        tree = build(keys)
        assert inorder(tree) == keys
        assert preorder(tree) == keys
        assert postorder(tree) == keys[::-1]

    def test_descending_insertion_is_left_skewed(self):
        keys = list(range(7, 0, -1))
        tree = build(keys)
        assert inorder(tree) == sorted(keys)
        assert preorder(tree) == keys
        assert postorder(tree) == sorted(keys)

    def test_interleaved_insertion_extremes(self):
        keys = [1, 100, 2, 99, 3, 98]
        tree = build(keys)
        assert inorder(tree) == sorted(keys)
        pre, _, post = reference(keys)[0], None, reference(keys)[2]
        assert preorder(tree) == pre
        assert postorder(tree) == post


# --------------------------------------------------------------------------
# Duplicates (set semantics, assumption A5)
# --------------------------------------------------------------------------
class TestDuplicates:
    def test_duplicate_root_ignored(self):
        tree = build([5, 5])
        assert inorder(tree) == [5]
        assert preorder(tree) == [5]
        assert postorder(tree) == [5]

    def test_same_key_many_times(self):
        tree = build([7] * 50)
        assert inorder(tree) == [7]

    def test_duplicate_leaf_ignored(self):
        tree = build(CANON_KEYS + [1, 9, 4])
        assert inorder(tree) == CANON_IN
        assert preorder(tree) == CANON_PRE
        assert postorder(tree) == CANON_POST

    def test_duplicate_internal_node_ignored(self):
        tree = build(CANON_KEYS + [3, 8])
        assert inorder(tree) == CANON_IN
        assert preorder(tree) == CANON_PRE

    def test_duplicates_do_not_change_structure(self):
        with_dups = build([5, 3, 5, 8, 3, 8, 1, 1])
        without = build([5, 3, 8, 1])
        assert preorder(with_dups) == preorder(without)
        assert postorder(with_dups) == postorder(without)

    def test_equal_int_and_float_treated_as_duplicate(self):
        # ASSUMPTION: equality via ==, so 1 and 1.0 are the same key.
        tree = build([1, 1.0])
        assert len(inorder(tree)) == 1


# --------------------------------------------------------------------------
# Value ranges and key types
# --------------------------------------------------------------------------
class TestKeyValues:
    def test_negative_numbers(self):
        keys = [-5, -10, -1, -7]
        tree = build(keys)
        assert inorder(tree) == sorted(keys)

    def test_zero_included(self):
        keys = [0, -1, 1]
        tree = build(keys)
        assert inorder(tree) == [-1, 0, 1]
        assert preorder(tree) == [0, -1, 1]

    def test_zero_only(self):
        # Guards against falsy-value bugs (e.g. `if not key`).
        assert inorder(build([0])) == [0]

    def test_mixed_positive_and_negative(self):
        keys = [3, -3, 2, -2, 1, -1, 0]
        assert inorder(build(keys)) == sorted(keys)

    def test_very_large_integers(self):
        keys = [10**30, -(10**30), 0, 10**18]
        assert inorder(build(keys)) == sorted(keys)

    def test_floats(self):
        keys = [2.5, 1.5, 3.5, -0.5, 0.0]
        assert inorder(build(keys)) == sorted(keys)

    def test_floats_very_close_together(self):
        keys = [1.0, 1.0000000001, 0.9999999999]
        assert inorder(build(keys)) == sorted(keys)

    def test_infinities(self):
        keys = [float("inf"), float("-inf"), 0]
        assert inorder(build(keys)) == [float("-inf"), 0, float("inf")]

    def test_strings(self):
        keys = ["m", "c", "x", "a", "d"]
        assert inorder(build(keys)) == sorted(keys)

    def test_strings_case_sensitive(self):
        # ASSUMPTION: default Python string ordering ("B" < "a").
        keys = ["a", "B", "A", "b"]
        assert inorder(build(keys)) == sorted(keys)

    def test_empty_string_key(self):
        keys = ["", "a", "b"]
        assert inorder(build(keys)) == ["", "a", "b"]

    def test_strings_with_common_prefix(self):
        keys = ["app", "apple", "ap", "apples"]
        assert inorder(build(keys)) == sorted(keys)

    def test_unicode_strings(self):
        keys = ["é", "e", "z", "ñ", "日本"]
        assert inorder(build(keys)) == sorted(keys)

    def test_tuples(self):
        keys = [(2, "b"), (1, "z"), (2, "a"), (1, "a")]
        assert inorder(build(keys)) == sorted(keys)

    def test_integer_min_max_extremes(self):
        keys = [-(2**63), 2**63 - 1, 0]
        assert inorder(build(keys)) == sorted(keys)


# --------------------------------------------------------------------------
# Invalid / unusual inputs (assumption A8)
# --------------------------------------------------------------------------
@pytest.mark.skipif(not EXPECT_TYPEERROR_ON_INVALID, reason="invalid-input behavior not asserted")
class TestInvalidInputs:
    def test_insert_none_into_empty_tree_raises_or_is_documented(self):
        # ASSUMPTION: None is not a valid key. Some implementations accept a
        # single None into an empty tree since no comparison is needed, so this
        # test inserts None into a non-empty tree, which forces a comparison.
        tree = build([1])
        with pytest.raises(INVALID_KEY_EXCEPTION):
            getattr(tree, INSERT)(None)

    def test_insert_string_into_int_tree_raises(self):
        tree = build([1, 2, 3])
        with pytest.raises(INVALID_KEY_EXCEPTION):
            getattr(tree, INSERT)("a")

    def test_insert_int_into_string_tree_raises(self):
        tree = build(["a", "b"])
        with pytest.raises(INVALID_KEY_EXCEPTION):
            getattr(tree, INSERT)(1)

    def test_insert_list_into_int_tree_raises(self):
        tree = build([1])
        with pytest.raises(INVALID_KEY_EXCEPTION):
            getattr(tree, INSERT)([1])

    def test_failed_insert_leaves_tree_unchanged(self):
        tree = build(CANON_KEYS)
        with pytest.raises(INVALID_KEY_EXCEPTION):
            getattr(tree, INSERT)("bad")
        assert inorder(tree) == CANON_IN
        assert preorder(tree) == CANON_PRE
        assert postorder(tree) == CANON_POST

    def test_tree_still_usable_after_failed_insert(self):
        tree = build([10, 20])
        with pytest.raises(INVALID_KEY_EXCEPTION):
            getattr(tree, INSERT)(object())
        getattr(tree, INSERT)(15)
        assert inorder(tree) == [10, 15, 20]


# --------------------------------------------------------------------------
# State, repeatability and isolation
# --------------------------------------------------------------------------
class TestStateAndIsolation:
    def test_repeated_traversals_return_same_result(self):
        tree = build(CANON_KEYS)
        assert inorder(tree) == inorder(tree)
        assert preorder(tree) == preorder(tree)
        assert postorder(tree) == postorder(tree)

    def test_traversal_does_not_mutate_tree(self):
        tree = build(CANON_KEYS)
        inorder(tree)
        preorder(tree)
        postorder(tree)
        assert inorder(tree) == CANON_IN
        assert preorder(tree) == CANON_PRE
        assert postorder(tree) == CANON_POST

    def test_insert_after_traversal(self):
        tree = build([5, 3])
        assert inorder(tree) == [3, 5]
        getattr(tree, INSERT)(4)
        assert inorder(tree) == [3, 4, 5]
        assert preorder(tree) == [5, 3, 4]

    def test_interleaved_insert_and_traverse(self):
        tree = build()
        expected = []
        for k in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
            getattr(tree, INSERT)(k)
            expected.append(k)
            assert inorder(tree) == sorted(expected)

    def test_two_trees_do_not_share_state(self):
        a = build([1, 2, 3])
        b = build([10, 20])
        assert inorder(a) == [1, 2, 3]
        assert inorder(b) == [10, 20]

    def test_returned_list_mutation_does_not_affect_tree(self):
        # ASSUMPTION A9
        tree = build(CANON_KEYS)
        result = getattr(tree, INORDER)()
        if not isinstance(result, list):
            pytest.skip("traversal does not return a list")
        result.clear()
        assert inorder(tree) == CANON_IN

    def test_traversal_returns_list_like_of_plain_keys(self):
        tree = build([2, 1, 3])
        result = inorder(tree)
        assert all(isinstance(x, int) for x in result)


# --------------------------------------------------------------------------
# Optional API: __len__ and __contains__ (assumption A7)
# --------------------------------------------------------------------------
class TestOptionalApi:
    def test_len_of_empty_tree(self):
        tree = build()
        if not hasattr(tree, "__len__"):
            pytest.skip("__len__ not implemented")
        assert len(tree) == 0

    def test_len_counts_unique_keys_only(self):
        tree = build([1, 2, 2, 3, 3, 3])
        if not hasattr(tree, "__len__"):
            pytest.skip("__len__ not implemented")
        assert len(tree) == 3

    def test_contains_present_and_absent(self):
        tree = build(CANON_KEYS)
        if not hasattr(tree, "__contains__"):
            pytest.skip("__contains__ not implemented")
        assert 5 in tree
        assert 1 in tree
        assert 9 in tree
        assert 6 not in tree
        assert 0 not in tree

    def test_contains_on_empty_tree(self):
        tree = build()
        if not hasattr(tree, "__contains__"):
            pytest.skip("__contains__ not implemented")
        assert 1 not in tree


# --------------------------------------------------------------------------
# Larger and randomized inputs
# --------------------------------------------------------------------------
class TestLargeAndRandom:
    def test_many_random_unique_keys(self):
        rng = random.Random(12345)
        keys = rng.sample(range(-10_000, 10_000), 500)
        tree = build(keys)
        pre, ino, post = reference(keys)
        assert inorder(tree) == ino == sorted(keys)
        assert preorder(tree) == pre
        assert postorder(tree) == post

    def test_many_random_keys_with_duplicates(self):
        rng = random.Random(777)
        keys = [rng.randint(0, 100) for _ in range(1000)]
        tree = build(keys)
        pre, ino, post = reference(keys)
        assert inorder(tree) == ino == sorted(set(keys))
        assert preorder(tree) == pre
        assert postorder(tree) == post

    @pytest.mark.parametrize("seed", range(10))
    def test_randomized_against_reference_model(self, seed):
        rng = random.Random(seed)
        n = rng.randint(0, 60)
        keys = [rng.randint(-50, 50) for _ in range(n)]
        tree = build(keys)
        pre, ino, post = reference(keys)
        assert inorder(tree) == ino
        assert preorder(tree) == pre
        assert postorder(tree) == post

    def test_moderately_deep_degenerate_tree(self):
        # 400 levels: should work even with a recursive implementation.
        keys = list(range(400))
        tree = build(keys)
        assert inorder(tree) == keys
        assert preorder(tree) == keys
        assert postorder(tree) == keys[::-1]

    @pytest.mark.xfail(
        raises=RecursionError,
        strict=False,
        reason="A10: recursive implementations may exceed the recursion limit "
        "on a very deep degenerate tree",
    )
    def test_very_deep_degenerate_tree(self):
        depth = sys.getrecursionlimit() * 3
        keys = list(range(depth))
        tree = build(keys)
        assert inorder(tree) == keys
        assert preorder(tree) == keys
        assert postorder(tree) == keys[::-1]

    def test_large_balanced_insertion(self):
        # Insert in an order that builds a perfectly balanced tree.
        def balanced_order(lo, hi):
            if lo > hi:
                return []
            mid = (lo + hi) // 2
            return [mid] + balanced_order(lo, mid - 1) + balanced_order(mid + 1, hi)

        keys = balanced_order(0, 1022)
        tree = build(keys)
        assert inorder(tree) == list(range(1023))
        assert preorder(tree) == keys