"""
Unit tests for a Python binary search tree set (BSTNode + BSTSet), written with pytest.

EXPLICIT ASSUMPTIONS (the description leaves these ambiguous):

A1. Module name: the classes are importable from a module named `BST`.
    Change the import below if your module is named differently.
A2. BSTSet() takes no required constructor arguments and starts empty.
A3. BSTSet.put(key) inserts a key. Its return value is NOT asserted.
A4. Traversal methods on BSTSet are named `in_order()`, `pre_order()`, and
    `post_order()`, and each returns a list of keys. If yours return generators
    or print, adjust the `_to_list` helper and the TRAVERSAL_METHODS names.
A5. Iteration: iter(BSTSet) / `for k in tree` yields keys in ascending
    (in-order) order. Tests marked "iteration" are skipped if __iter__ is absent.
A6. len(tree) and `key in tree` are NOT described, so they are not tested
    unconditionally. Tests that use them are skipped if unsupported.
A7. BSTNode(key) constructs a node with `.key`, `.left`, `.right` attributes,
    with `.left` and `.right` initially None. The description does not name
    these attributes, so tests that rely on them are skipped if absent.
A8. BSTNode.put(key) inserts into the subtree rooted at that node, and
    BSTNode has in_order/pre_order/post_order methods returning lists.
    These node-level tests are skipped if the methods are absent.
A9. Traversals on an empty tree return an empty list (not None, no exception).
A10. Inserting a duplicate is silently ignored (no exception, no duplicate).
A11. Inserting non-integer or None keys is unspecified, so there are no
     tests for invalid key types. Only integers are tested, as described.
"""

import pytest

from BST import BSTNode, BSTSet  # A1


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_list(result):
    """Normalize a traversal result (list or iterable) to a list. (A4)"""
    return list(result)


def build(keys):
    """Build a BSTSet by inserting keys in the given order."""
    tree = BSTSet()
    for k in keys:
        tree.put(k)
    return tree


def inorder(tree):
    return _to_list(tree.in_order())


def preorder(tree):
    return _to_list(tree.pre_order())


def postorder(tree):
    return _to_list(tree.post_order())


def _has(obj, name):
    return hasattr(obj, name)


TRAVERSAL_METHODS = ["in_order", "pre_order", "post_order"]


# ---------------------------------------------------------------------------
# Empty tree
# ---------------------------------------------------------------------------

class TestEmptyTree:
    def test_inorder_empty(self):
        assert inorder(BSTSet()) == []

    def test_preorder_empty(self):
        assert preorder(BSTSet()) == []

    def test_postorder_empty(self):
        assert postorder(BSTSet()) == []

    @pytest.mark.parametrize("method", TRAVERSAL_METHODS)
    def test_traversals_do_not_raise_on_empty(self, method):
        tree = BSTSet()
        _to_list(getattr(tree, method)())  # must not raise

    def test_empty_tree_traversal_is_repeatable(self):
        tree = BSTSet()
        assert inorder(tree) == []
        assert inorder(tree) == []

    def test_iteration_empty(self):
        tree = BSTSet()
        if not _has(tree, "__iter__"):
            pytest.skip("BSTSet does not support iteration (A5)")
        assert list(tree) == []

    def test_two_empty_trees_are_independent(self):
        a, b = BSTSet(), BSTSet()
        a.put(1)
        assert inorder(a) == [1]
        assert inorder(b) == []


# ---------------------------------------------------------------------------
# Single node
# ---------------------------------------------------------------------------

class TestSingleNode:
    @pytest.mark.parametrize("key", [0, 1, -1, 42, -42, 10**9, -(10**9)])
    @pytest.mark.parametrize("method", TRAVERSAL_METHODS)
    def test_single_key_all_traversals(self, key, method):
        tree = build([key])
        assert _to_list(getattr(tree, method)()) == [key]

    def test_single_key_iteration(self):
        tree = build([7])
        if not _has(tree, "__iter__"):
            pytest.skip("BSTSet does not support iteration (A5)")
        assert list(tree) == [7]

    def test_insert_into_empty_then_traverse_twice(self):
        tree = build([5])
        assert inorder(tree) == [5]
        assert inorder(tree) == [5]


# ---------------------------------------------------------------------------
# Normal balanced tree with all three traversal orders
#
#            8
#          /   \
#         3     10
#        / \      \
#       1   6      14
#          / \    /
#         4   7  13
# ---------------------------------------------------------------------------

CLASSIC_INSERT_ORDER = [8, 3, 10, 1, 6, 14, 4, 7, 13]


class TestClassicTree:
    def test_inorder_is_sorted(self):
        tree = build(CLASSIC_INSERT_ORDER)
        assert inorder(tree) == [1, 3, 4, 6, 7, 8, 10, 13, 14]

    def test_preorder(self):
        tree = build(CLASSIC_INSERT_ORDER)
        assert preorder(tree) == [8, 3, 1, 6, 4, 7, 10, 14, 13]

    def test_postorder(self):
        tree = build(CLASSIC_INSERT_ORDER)
        assert postorder(tree) == [1, 4, 7, 6, 3, 13, 14, 10, 8]

    def test_all_traversals_contain_same_elements(self):
        tree = build(CLASSIC_INSERT_ORDER)
        expected = sorted(CLASSIC_INSERT_ORDER)
        assert sorted(inorder(tree)) == expected
        assert sorted(preorder(tree)) == expected
        assert sorted(postorder(tree)) == expected

    def test_traversal_lengths_match(self):
        tree = build(CLASSIC_INSERT_ORDER)
        n = len(CLASSIC_INSERT_ORDER)
        assert len(inorder(tree)) == n
        assert len(preorder(tree)) == n
        assert len(postorder(tree)) == n

    def test_root_is_first_in_preorder_and_last_in_postorder(self):
        tree = build(CLASSIC_INSERT_ORDER)
        assert preorder(tree)[0] == 8
        assert postorder(tree)[-1] == 8

    def test_traversals_do_not_mutate_tree(self):
        tree = build(CLASSIC_INSERT_ORDER)
        before = (inorder(tree), preorder(tree), postorder(tree))
        # Call them again in a different order
        _ = postorder(tree)
        _ = preorder(tree)
        _ = inorder(tree)
        after = (inorder(tree), preorder(tree), postorder(tree))
        assert before == after

    def test_iteration_matches_inorder(self):
        tree = build(CLASSIC_INSERT_ORDER)
        if not _has(tree, "__iter__"):
            pytest.skip("BSTSet does not support iteration (A5)")
        assert list(tree) == inorder(tree)
        assert list(tree) == [1, 3, 4, 6, 7, 8, 10, 13, 14]


# ---------------------------------------------------------------------------
# Small trees: left/right of root, missing children
# ---------------------------------------------------------------------------

class TestSmallTrees:
    def test_root_with_only_left_child(self):
        tree = build([5, 2])
        assert inorder(tree) == [2, 5]
        assert preorder(tree) == [5, 2]
        assert postorder(tree) == [2, 5]

    def test_root_with_only_right_child(self):
        tree = build([5, 9])
        assert inorder(tree) == [5, 9]
        assert preorder(tree) == [5, 9]
        assert postorder(tree) == [9, 5]

    def test_root_with_both_children(self):
        tree = build([5, 2, 9])
        assert inorder(tree) == [2, 5, 9]
        assert preorder(tree) == [5, 2, 9]
        assert postorder(tree) == [2, 9, 5]

    def test_both_children_inserted_right_first(self):
        # Insertion order of siblings must not change the shape.
        tree = build([5, 9, 2])
        assert inorder(tree) == [2, 5, 9]
        assert preorder(tree) == [5, 2, 9]
        assert postorder(tree) == [2, 9, 5]

    def test_left_child_has_only_right_child(self):
        #     5
        #    /
        #   2
        #    \
        #     4
        tree = build([5, 2, 4])
        assert inorder(tree) == [2, 4, 5]
        assert preorder(tree) == [5, 2, 4]
        assert postorder(tree) == [4, 2, 5]

    def test_right_child_has_only_left_child(self):
        #   5
        #    \
        #     9
        #    /
        #   7
        tree = build([5, 9, 7])
        assert inorder(tree) == [5, 7, 9]
        assert preorder(tree) == [5, 9, 7]
        assert postorder(tree) == [7, 9, 5]

    def test_left_subtree_only_deep(self):
        #       10
        #      /
        #     5
        #    / \
        #   3   7
        tree = build([10, 5, 3, 7])
        assert inorder(tree) == [3, 5, 7, 10]
        assert preorder(tree) == [10, 5, 3, 7]
        assert postorder(tree) == [3, 7, 5, 10]

    def test_right_subtree_only_deep(self):
        #   10
        #     \
        #      15
        #     /  \
        #   12    20
        tree = build([10, 15, 12, 20])
        assert inorder(tree) == [10, 12, 15, 20]
        assert preorder(tree) == [10, 15, 12, 20]
        assert postorder(tree) == [12, 20, 15, 10]

    def test_zigzag_left_right_left(self):
        #   10
        #   /
        #  5
        #   \
        #    8
        #   /
        #  6
        tree = build([10, 5, 8, 6])
        assert inorder(tree) == [5, 6, 8, 10]
        assert preorder(tree) == [10, 5, 8, 6]
        assert postorder(tree) == [6, 8, 5, 10]

    def test_zigzag_right_left_right(self):
        #  10
        #    \
        #     20
        #    /
        #  15
        #    \
        #     17
        tree = build([10, 20, 15, 17])
        assert inorder(tree) == [10, 15, 17, 20]
        assert preorder(tree) == [10, 20, 15, 17]
        assert postorder(tree) == [17, 15, 20, 10]


# ---------------------------------------------------------------------------
# Degenerate (skewed) trees
# ---------------------------------------------------------------------------

class TestSkewedTrees:
    def test_ascending_insertion_right_skewed(self):
        keys = [1, 2, 3, 4, 5]
        tree = build(keys)
        assert inorder(tree) == [1, 2, 3, 4, 5]
        assert preorder(tree) == [1, 2, 3, 4, 5]
        assert postorder(tree) == [5, 4, 3, 2, 1]

    def test_descending_insertion_left_skewed(self):
        keys = [5, 4, 3, 2, 1]
        tree = build(keys)
        assert inorder(tree) == [1, 2, 3, 4, 5]
        assert preorder(tree) == [5, 4, 3, 2, 1]
        assert postorder(tree) == [1, 2, 3, 4, 5]

    def test_large_ascending_sequence(self):
        keys = list(range(200))
        tree = build(keys)
        assert inorder(tree) == keys
        assert preorder(tree) == keys
        assert postorder(tree) == list(reversed(keys))

    def test_large_descending_sequence(self):
        keys = list(range(200, 0, -1))
        tree = build(keys)
        assert inorder(tree) == sorted(keys)
        assert preorder(tree) == keys
        assert postorder(tree) == sorted(keys)

    def test_deep_skewed_tree_does_not_crash(self):
        # Depth 500 stays below CPython's default recursion limit (1000) even
        # for a recursive implementation, while still stressing deep trees.
        # NOTE: Behavior for much deeper trees is unspecified (A12).
        keys = list(range(500))
        tree = build(keys)
        assert inorder(tree) == keys

    def test_alternating_extremes(self):
        # 1, 10, 2, 9, 3, 8 ... produces a zigzag-shaped tree
        keys = [1, 10, 2, 9, 3, 8]
        tree = build(keys)
        assert inorder(tree) == [1, 2, 3, 8, 9, 10]
        assert preorder(tree) == [1, 10, 2, 9, 3, 8]
        assert postorder(tree) == [8, 3, 9, 2, 10, 1]


# ---------------------------------------------------------------------------
# Inserting smaller / larger than the root
# ---------------------------------------------------------------------------

class TestRelativeToRoot:
    def test_insert_smaller_than_root_goes_left(self):
        tree = build([10, 1])
        assert preorder(tree) == [10, 1]  # root first, then left subtree
        assert postorder(tree) == [1, 10]

    def test_insert_larger_than_root_goes_right(self):
        tree = build([10, 100])
        assert preorder(tree) == [10, 100]
        assert postorder(tree) == [100, 10]

    def test_all_keys_smaller_than_root(self):
        tree = build([100, 50, 25, 75, 10])
        assert inorder(tree) == [10, 25, 50, 75, 100]
        assert preorder(tree)[0] == 100
        assert postorder(tree)[-1] == 100

    def test_all_keys_larger_than_root(self):
        tree = build([1, 50, 25, 75, 100])
        assert inorder(tree) == [1, 25, 50, 75, 100]
        assert preorder(tree)[0] == 1
        assert postorder(tree)[-1] == 1

    def test_left_subtree_keys_all_less_than_root(self):
        root = 50
        keys = [root, 20, 80, 10, 30, 70, 90, 25, 35]
        tree = build(keys)
        pre = preorder(tree)
        assert pre[0] == root
        # In preorder, the left subtree is the block immediately after the
        # root; its keys must all be < root. The right subtree is the rest.
        left_count = len([k for k in keys if k < root])
        left_block = pre[1:1 + left_count]
        right_block = pre[1 + left_count:]
        assert all(k < root for k in left_block)
        assert all(k > root for k in right_block)

    def test_bst_property_via_inorder_sorted_strictly(self):
        keys = [50, 30, 70, 20, 40, 60, 80, 35, 45, 65]
        tree = build(keys)
        result = inorder(tree)
        assert result == sorted(set(keys))
        assert all(a < b for a, b in zip(result, result[1:]))


# ---------------------------------------------------------------------------
# Duplicates / set uniqueness
# ---------------------------------------------------------------------------

class TestDuplicates:
    def test_duplicate_root_ignored(self):
        tree = build([5, 5])
        assert inorder(tree) == [5]
        assert preorder(tree) == [5]
        assert postorder(tree) == [5]

    def test_duplicate_root_many_times(self):
        tree = build([5] * 20)
        assert inorder(tree) == [5]

    def test_duplicate_left_child_ignored(self):
        tree = build([5, 2, 2])
        assert inorder(tree) == [2, 5]
        assert preorder(tree) == [5, 2]
        assert postorder(tree) == [2, 5]

    def test_duplicate_right_child_ignored(self):
        tree = build([5, 9, 9])
        assert inorder(tree) == [5, 9]
        assert preorder(tree) == [5, 9]
        assert postorder(tree) == [9, 5]

    def test_duplicate_deep_in_tree_ignored(self):
        tree = build(CLASSIC_INSERT_ORDER + [7, 13, 1, 14])
        assert inorder(tree) == [1, 3, 4, 6, 7, 8, 10, 13, 14]

    def test_duplicate_insert_does_not_change_structure(self):
        base = build(CLASSIC_INSERT_ORDER)
        dup = build(CLASSIC_INSERT_ORDER + CLASSIC_INSERT_ORDER)
        assert preorder(base) == preorder(dup)
        assert postorder(base) == postorder(dup)
        assert inorder(base) == inorder(dup)

    def test_duplicate_insert_of_every_key_in_reverse(self):
        keys = [4, 2, 6, 1, 3, 5, 7]
        tree = build(keys + list(reversed(keys)))
        assert inorder(tree) == [1, 2, 3, 4, 5, 6, 7]
        assert preorder(tree) == [4, 2, 1, 3, 6, 5, 7]

    def test_duplicate_zero(self):
        tree = build([0, 0, 0])
        assert inorder(tree) == [0]

    def test_duplicate_negative(self):
        tree = build([-3, -3, -3])
        assert inorder(tree) == [-3]

    def test_duplicate_insert_does_not_raise(self):
        tree = build([1])
        tree.put(1)  # A10: must not raise

    def test_uniqueness_with_interleaved_duplicates(self):
        tree = build([3, 1, 3, 2, 1, 2, 3, 4, 4])
        assert inorder(tree) == [1, 2, 3, 4]

    def test_set_size_via_len_if_supported(self):
        tree = build([3, 1, 3, 2, 1, 2])
        if not _has(tree, "__len__"):
            pytest.skip("BSTSet does not support len() (A6)")
        assert len(tree) == 3


# ---------------------------------------------------------------------------
# Negative numbers, zero, mixed signs
# ---------------------------------------------------------------------------

class TestIntegerRange:
    def test_negative_integers_only(self):
        tree = build([-5, -10, -1, -7, -3])
        assert inorder(tree) == [-10, -7, -5, -3, -1]
        assert preorder(tree) == [-5, -10, -7, -1, -3]
        assert postorder(tree) == [-7, -10, -3, -1, -5]

    def test_zero_only(self):
        tree = build([0])
        assert inorder(tree) == [0]

    def test_zero_as_root_with_negative_and_positive(self):
        tree = build([0, -1, 1])
        assert inorder(tree) == [-1, 0, 1]
        assert preorder(tree) == [0, -1, 1]
        assert postorder(tree) == [-1, 1, 0]

    def test_zero_inserted_after_negatives_and_positives(self):
        tree = build([-1, 1, 0])
        # root -1; 1 goes right; 0 goes right then left of 1
        assert inorder(tree) == [-1, 0, 1]
        assert preorder(tree) == [-1, 1, 0]
        assert postorder(tree) == [0, 1, -1]

    def test_negative_root_with_positive_keys(self):
        tree = build([-10, 5, 0, -5, 10])
        assert inorder(tree) == [-10, -5, 0, 5, 10]

    def test_positive_root_with_negative_keys(self):
        tree = build([10, -5, 0, -10, 5])
        assert inorder(tree) == [-10, -5, 0, 5, 10]

    def test_mixed_sign_ordering_is_numeric_not_lexicographic(self):
        # Guards against string-comparison bugs ("10" < "9" lexicographically).
        tree = build([9, 10, 100, 2, 20, -1, -10])
        assert inorder(tree) == [-10, -1, 2, 9, 10, 20, 100]

    def test_adjacent_negative_and_zero(self):
        tree = build([0, -1])
        assert inorder(tree) == [-1, 0]
        assert preorder(tree) == [0, -1]

    def test_large_magnitude_integers(self):
        keys = [10**12, -(10**12), 0, 10**12 - 1, -(10**12) + 1]
        tree = build(keys)
        assert inorder(tree) == sorted(keys)

    def test_minus_zero_equivalence(self):
        # -0 == 0 for integers, so this should be a duplicate.
        tree = build([0, -0])
        assert inorder(tree) == [0]


# ---------------------------------------------------------------------------
# Insertion-order independence of the in-order result
# ---------------------------------------------------------------------------

class TestInsertionOrder:
    @pytest.mark.parametrize(
        "order",
        [
            [1, 2, 3, 4, 5, 6, 7],
            [7, 6, 5, 4, 3, 2, 1],
            [4, 2, 6, 1, 3, 5, 7],
            [4, 6, 2, 7, 5, 3, 1],
            [1, 7, 2, 6, 3, 5, 4],
            [3, 1, 2, 7, 5, 6, 4],
        ],
    )
    def test_inorder_independent_of_insertion_order(self, order):
        tree = build(order)
        assert inorder(tree) == [1, 2, 3, 4, 5, 6, 7]

    def test_preorder_depends_on_insertion_order(self):
        a = build([2, 1, 3])
        b = build([1, 2, 3])
        assert inorder(a) == inorder(b) == [1, 2, 3]
        assert preorder(a) == [2, 1, 3]
        assert preorder(b) == [1, 2, 3]

    def test_first_inserted_key_is_root(self):
        for first in [1, 5, 9]:
            others = [k for k in [1, 5, 9] if k != first]
            tree = build([first] + others)
            assert preorder(tree)[0] == first
            assert postorder(tree)[-1] == first

    def test_insertion_after_traversal_is_reflected(self):
        tree = build([5, 3])
        assert inorder(tree) == [3, 5]
        tree.put(4)
        assert inorder(tree) == [3, 4, 5]
        tree.put(8)
        assert inorder(tree) == [3, 4, 5, 8]

    def test_incremental_insert_matches_batch_insert(self):
        keys = [8, 3, 10, 1, 6, 14, 4, 7, 13]
        incremental = BSTSet()
        for k in keys:
            incremental.put(k)
            assert inorder(incremental) == sorted(keys[: keys.index(k) + 1])
        assert preorder(incremental) == preorder(build(keys))


# ---------------------------------------------------------------------------
# Traversal-specific invariants
# ---------------------------------------------------------------------------

class TestTraversalInvariants:
    @pytest.mark.parametrize("method", TRAVERSAL_METHODS)
    def test_traversal_returns_new_sequence_each_call(self, method):
        tree = build([2, 1, 3])
        first = _to_list(getattr(tree, method)())
        second = _to_list(getattr(tree, method)())
        assert first == second

    @pytest.mark.parametrize("method", TRAVERSAL_METHODS)
    def test_mutating_returned_list_does_not_affect_tree(self, method):
        tree = build([2, 1, 3])
        result = getattr(tree, method)()
        if not isinstance(result, list):
            pytest.skip("Traversal does not return a list (A4)")
        expected = list(result)
        result.append(999)
        result.clear()
        assert _to_list(getattr(tree, method)()) == expected

    @pytest.mark.parametrize("method", TRAVERSAL_METHODS)
    def test_traversal_contains_no_duplicates(self, method):
        tree = build([4, 2, 6, 2, 4, 6, 1, 1])
        result = _to_list(getattr(tree, method)())
        assert len(result) == len(set(result))

    def test_preorder_and_postorder_are_reverses_for_mirror_symmetric_case(self):
        # For a single node both are identical.
        tree = build([1])
        assert preorder(tree) == postorder(tree) == [1]

    def test_postorder_of_right_skew_is_reverse_of_preorder(self):
        tree = build([1, 2, 3, 4])
        assert postorder(tree) == list(reversed(preorder(tree)))

    def test_preorder_reconstructs_same_tree(self):
        # Inserting a tree's preorder sequence into a fresh set must yield an
        # identical tree (a known BST property).
        original = build([8, 3, 10, 1, 6, 14, 4, 7, 13])
        rebuilt = build(preorder(original))
        assert preorder(rebuilt) == preorder(original)
        assert postorder(rebuilt) == postorder(original)
        assert inorder(rebuilt) == inorder(original)


# ---------------------------------------------------------------------------
# Iteration (A5)
# ---------------------------------------------------------------------------

class TestIteration:
    def _require_iter(self, tree):
        if not _has(tree, "__iter__"):
            pytest.skip("BSTSet does not support iteration (A5)")

    def test_iteration_yields_sorted_keys(self):
        tree = build([5, 3, 8, 1, 4, 7, 9])
        self._require_iter(tree)
        assert list(tree) == [1, 3, 4, 5, 7, 8, 9]

    def test_iteration_with_duplicates(self):
        tree = build([2, 2, 1, 1, 3, 3])
        self._require_iter(tree)
        assert list(tree) == [1, 2, 3]

    def test_iteration_with_negatives_and_zero(self):
        tree = build([0, -2, 2, -1, 1])
        self._require_iter(tree)
        assert list(tree) == [-2, -1, 0, 1, 2]

    def test_iteration_can_be_repeated(self):
        tree = build([3, 1, 2])
        self._require_iter(tree)
        assert list(tree) == [1, 2, 3]
        assert list(tree) == [1, 2, 3]

    def test_iteration_in_for_loop(self):
        tree = build([3, 1, 2])
        self._require_iter(tree)
        seen = []
        for key in tree:
            seen.append(key)
        assert seen == [1, 2, 3]

    def test_iteration_with_sorted_builtin(self):
        tree = build([9, 1, 5])
        self._require_iter(tree)
        assert sorted(tree) == [1, 5, 9]

    def test_iteration_with_min_max_sum(self):
        tree = build([9, 1, 5, 5])
        self._require_iter(tree)
        assert min(tree) == 1
        assert max(tree) == 9
        assert sum(tree) == 15

    def test_iteration_reflects_later_insertions(self):
        tree = build([2])
        self._require_iter(tree)
        assert list(tree) == [2]
        tree.put(1)
        assert list(tree) == [1, 2]

    def test_iteration_skewed_tree(self):
        tree = build(range(50, 0, -1))
        self._require_iter(tree)
        assert list(tree) == list(range(1, 51))

    def test_independent_iterators(self):
        tree = build([1, 2, 3])
        self._require_iter(tree)
        it1, it2 = iter(tree), iter(tree)
        assert next(it1) == 1
        assert next(it2) == 1
        assert next(it1) == 2
        assert next(it2) == 2


# ---------------------------------------------------------------------------
# Membership / len (only if supported, A6)
# ---------------------------------------------------------------------------

class TestOptionalContainerProtocol:
    def test_contains_present_and_absent(self):
        tree = build([5, 3, 8])
        if not _has(tree, "__contains__"):
            pytest.skip("BSTSet does not support `in` (A6)")
        assert 5 in tree
        assert 3 in tree
        assert 8 in tree
        assert 4 not in tree
        assert 0 not in tree

    def test_contains_on_empty(self):
        tree = BSTSet()
        if not _has(tree, "__contains__"):
            pytest.skip("BSTSet does not support `in` (A6)")
        assert 1 not in tree

    def test_len_empty_and_after_inserts(self):
        tree = BSTSet()
        if not _has(tree, "__len__"):
            pytest.skip("BSTSet does not support len() (A6)")
        assert len(tree) == 0
        tree.put(1)
        assert len(tree) == 1
        tree.put(1)
        assert len(tree) == 1
        tree.put(2)
        assert len(tree) == 2


# ---------------------------------------------------------------------------
# BSTNode-level tests (A7, A8)
# ---------------------------------------------------------------------------

class TestBSTNode:
    def test_node_stores_key(self):
        node = BSTNode(10)
        if not _has(node, "key"):
            pytest.skip("BSTNode has no `.key` attribute (A7)")
        assert node.key == 10

    def test_new_node_has_no_children(self):
        node = BSTNode(10)
        if not (_has(node, "left") and _has(node, "right")):
            pytest.skip("BSTNode has no `.left`/`.right` attributes (A7)")
        assert node.left is None
        assert node.right is None

    def test_node_put_smaller_goes_left(self):
        node = BSTNode(10)
        if not (_has(node, "put") and _has(node, "left")):
            pytest.skip("BSTNode API differs from assumptions (A7/A8)")
        node.put(5)
        assert node.left is not None
        assert node.left.key == 5
        assert node.right is None

    def test_node_put_larger_goes_right(self):
        node = BSTNode(10)
        if not (_has(node, "put") and _has(node, "right")):
            pytest.skip("BSTNode API differs from assumptions (A7/A8)")
        node.put(15)
        assert node.right is not None
        assert node.right.key == 15
        assert node.left is None

    def test_node_put_duplicate_creates_no_child(self):
        node = BSTNode(10)
        if not (_has(node, "put") and _has(node, "left")):
            pytest.skip("BSTNode API differs from assumptions (A7/A8)")
        node.put(10)
        assert node.left is None
        assert node.right is None

    def test_node_put_duplicate_of_child_creates_no_extra_node(self):
        node = BSTNode(10)
        if not (_has(node, "put") and _has(node, "left")):
            pytest.skip("BSTNode API differs from assumptions (A7/A8)")
        node.put(5)
        node.put(5)
        assert node.left.key == 5
        assert node.left.left is None
        assert node.left.right is None

    def test_node_put_builds_deeper_levels(self):
        node = BSTNode(10)
        if not (_has(node, "put") and _has(node, "left")):
            pytest.skip("BSTNode API differs from assumptions (A7/A8)")
        for k in [5, 15, 3, 7, 12, 20]:
            node.put(k)
        assert node.left.key == 5
        assert node.right.key == 15
        assert node.left.left.key == 3
        assert node.left.right.key == 7
        assert node.right.left.key == 12
        assert node.right.right.key == 20

    def test_node_negative_and_zero_keys(self):
        node = BSTNode(0)
        if not (_has(node, "put") and _has(node, "left")):
            pytest.skip("BSTNode API differs from assumptions (A7/A8)")
        node.put(-1)
        node.put(1)
        assert node.left.key == -1
        assert node.right.key == 1

    @pytest.mark.parametrize("method", TRAVERSAL_METHODS)
    def test_node_single_traversal(self, method):
        node = BSTNode(3)
        if not _has(node, method):
            pytest.skip(f"BSTNode has no `{method}` method (A8)")
        assert _to_list(getattr(node, method)()) == [3]

    def test_node_traversals_after_inserts(self):
        node = BSTNode(8)
        if not all(_has(node, m) for m in ["put"] + TRAVERSAL_METHODS):
            pytest.skip("BSTNode traversal API differs from assumptions (A8)")
        for k in [3, 10, 1, 6, 14, 4, 7, 13]:
            node.put(k)
        assert _to_list(node.in_order()) == [1, 3, 4, 6, 7, 8, 10, 13, 14]
        assert _to_list(node.pre_order()) == [8, 3, 1, 6, 4, 7, 10, 14, 13]
        assert _to_list(node.post_order()) == [1, 4, 7, 6, 3, 13, 14, 10, 8]

    def test_node_traversal_only_left_children(self):
        node = BSTNode(3)
        if not all(_has(node, m) for m in ["put"] + TRAVERSAL_METHODS):
            pytest.skip("BSTNode traversal API differs from assumptions (A8)")
        node.put(2)
        node.put(1)
        assert _to_list(node.in_order()) == [1, 2, 3]
        assert _to_list(node.pre_order()) == [3, 2, 1]
        assert _to_list(node.post_order()) == [1, 2, 3]

    def test_node_traversal_only_right_children(self):
        node = BSTNode(1)
        if not all(_has(node, m) for m in ["put"] + TRAVERSAL_METHODS):
            pytest.skip("BSTNode traversal API differs from assumptions (A8)")
        node.put(2)
        node.put(3)
        assert _to_list(node.in_order()) == [1, 2, 3]
        assert _to_list(node.pre_order()) == [1, 2, 3]
        assert _to_list(node.post_order()) == [3, 2, 1]


# ---------------------------------------------------------------------------
# Structural BST-property check (uses only public traversals)
# ---------------------------------------------------------------------------

def _is_valid_bst_from_preorder(seq, lo=None, hi=None):
    """
    Verify the BST property using only a preorder sequence: consuming the
    sequence recursively must succeed with strict bounds on every key.
    """
    it = iter(seq)
    sentinel = object()
    state = {"cur": next(it, sentinel)}

    def parse(lo, hi):
        cur = state["cur"]
        if cur is sentinel:
            return True
        if (lo is not None and cur <= lo) or (hi is not None and cur >= hi):
            return True  # belongs to an ancestor's other subtree
        state["cur"] = next(it, sentinel)
        return parse(lo, cur) and parse(cur, hi)

    ok = parse(lo, hi)
    return ok and state["cur"] is sentinel


class TestBSTPropertyPreservation:
    @pytest.mark.parametrize(
        "keys",
        [
            [],
            [1],
            [2, 1, 3],
            [8, 3, 10, 1, 6, 14, 4, 7, 13],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [0, -1, 1, -2, 2],
            [3, 3, 1, 1, 2, 2],
            [50, 25, 75, 12, 37, 62, 87, 6, 18, 31, 43],
        ],
    )
    def test_preorder_is_consistent_with_bst_property(self, keys):
        tree = build(keys)
        assert _is_valid_bst_from_preorder(preorder(tree))

    @pytest.mark.parametrize(
        "keys",
        [
            [8, 3, 10, 1, 6, 14, 4, 7, 13],
            [0, -1, 1, -2, 2],
            [50, 25, 75, 12, 37, 62, 87],
        ],
    )
    def test_inorder_strictly_increasing(self, keys):
        result = inorder(build(keys))
        assert all(a < b for a, b in zip(result, result[1:]))

    def test_bst_property_after_each_insert(self):
        keys = [8, 3, 10, 1, 6, 14, 4, 7, 13, 3, 8, 14]
        tree = BSTSet()
        for k in keys:
            tree.put(k)
            result = inorder(tree)
            assert result == sorted(result)
            assert len(result) == len(set(result))
            assert _is_valid_bst_from_preorder(preorder(tree))

    def test_randomized_inserts_against_reference_model(self):
        import random

        rng = random.Random(12345)  # fixed seed for reproducibility
        for _ in range(50):
            keys = [rng.randint(-50, 50) for _ in range(rng.randint(0, 60))]
            tree = build(keys)
            expected = sorted(set(keys))
            assert inorder(tree) == expected
            assert sorted(preorder(tree)) == expected
            assert sorted(postorder(tree)) == expected
            assert _is_valid_bst_from_preorder(preorder(tree))


# ---------------------------------------------------------------------------
# Independence of instances
# ---------------------------------------------------------------------------

class TestInstanceIsolation:
    def test_separate_sets_do_not_share_state(self):
        a = build([1, 2, 3])
        b = build([10, 20])
        assert inorder(a) == [1, 2, 3]
        assert inorder(b) == [10, 20]

    def test_inserting_into_one_does_not_affect_other(self):
        a = BSTSet()
        b = BSTSet()
        a.put(5)
        assert inorder(b) == []
        b.put(7)
        assert inorder(a) == [5]
        assert inorder(b) == [7]