"""
Unit tests for a Binary Search Tree set (pytest).

ASSUMPTIONS (the description does not specify these, so they are made explicit
and isolated in the ADAPTER section; edit that section if your program differs):

 A1. Module is `BST` and the class is `BSTSet`, constructed with no args.
 A2. `put(key)` adds a key. Its return value is NOT asserted.
 A3. Traversals are methods `in_order()`, `pre_order()`, `post_order()`
     returning a list of keys (not generators/printing).
     If your methods return iterators, the `_to_list` helper handles it.
 A4. Set semantics: inserting a duplicate key is silently ignored
     (no exception, no second copy in any traversal).
 A5. Smaller keys go in the left subtree, larger keys in the right subtree.
 A6. Traversal of an empty tree returns an empty list.
 A7. Keys must be mutually comparable. Inserting None or a key that cannot
     be compared to existing keys raises TypeError (tested as an assumption).
 A8. Optional features (`__len__`, `__contains__`) are tested only if present;
     otherwise those tests are skipped.
 A9. Traversing does not mutate the tree, and each call returns a fresh list.
"""

import random
import pytest

# ----------------------------- ADAPTER --------------------------------------
from BST import BSTSet  # A1


def _to_list(result):
    return list(result)  # A3: tolerate generators/iterators


def build(keys=()):
    t = BSTSet()
    for k in keys:
        t.put(k)
    return t


def inorder(t):
    return _to_list(t.in_order())


def preorder(t):
    return _to_list(t.pre_order())


def postorder(t):
    return _to_list(t.post_order())


# ------------------------ REFERENCE MODEL ------------------------------------
class _Node:
    def __init__(self, k):
        self.k, self.l, self.r = k, None, None


def _ref_insert(root, k):
    if root is None:
        return _Node(k)
    if k < root.k:
        root.l = _ref_insert(root.l, k)
    elif k > root.k:
        root.r = _ref_insert(root.r, k)
    return root


def _ref_build(keys):
    root = None
    for k in keys:
        root = _ref_insert(root, k)
    return root


def _ref_in(n):
    return [] if n is None else _ref_in(n.l) + [n.k] + _ref_in(n.r)


def _ref_pre(n):
    return [] if n is None else [n.k] + _ref_pre(n.l) + _ref_pre(n.r)


def _ref_post(n):
    return [] if n is None else _ref_post(n.l) + _ref_post(n.r) + [n.k]


# ------------------------------ EMPTY TREE -----------------------------------
class TestEmptyTree:
    def test_inorder_empty(self):
        assert inorder(build()) == []

    def test_preorder_empty(self):
        assert preorder(build()) == []

    def test_postorder_empty(self):
        assert postorder(build()) == []

    def test_empty_len_if_supported(self):
        t = build()
        if not hasattr(t, "__len__"):
            pytest.skip("__len__ not provided (A8)")
        assert len(t) == 0

    def test_empty_contains_if_supported(self):
        t = build()
        if not hasattr(t, "__contains__"):
            pytest.skip("__contains__ not provided (A8)")
        assert 1 not in t

    def test_independent_instances(self):
        a, b = build([1]), build()
        assert inorder(a) == [1]
        assert inorder(b) == []


# ---------------------------- SINGLE ELEMENT ---------------------------------
class TestSingleElement:
    @pytest.mark.parametrize("key", [0, 1, -1, 10**18, -(10**18)])
    def test_single_int_all_orders(self, key):
        t = build([key])
        assert inorder(t) == [key]
        assert preorder(t) == [key]
        assert postorder(t) == [key]

    def test_single_duplicate_inserted_many_times(self):
        t = build([5] * 10)
        assert inorder(t) == [5]
        assert preorder(t) == [5]
        assert postorder(t) == [5]


# --------------------------- SMALL KNOWN TREES -------------------------------
class TestKnownShapes:
    def test_balanced_three_nodes(self):
        #     2
        #    / \
        #   1   3
        t = build([2, 1, 3])
        assert inorder(t) == [1, 2, 3]
        assert preorder(t) == [2, 1, 3]
        assert postorder(t) == [1, 3, 2]

    def test_classic_seven_node_tree(self):
        #         8
        #       /   \
        #      3     10
        #     / \      \
        #    1   6      14
        #       / \    /
        #      4   7  13
        t = build([8, 3, 10, 1, 6, 14, 4, 7, 13])
        assert inorder(t) == [1, 3, 4, 6, 7, 8, 10, 13, 14]
        assert preorder(t) == [8, 3, 1, 6, 4, 7, 10, 14, 13]
        assert postorder(t) == [1, 4, 7, 6, 3, 13, 14, 10, 8]

    def test_left_child_only(self):
        t = build([5, 3])
        assert inorder(t) == [3, 5]
        assert preorder(t) == [5, 3]
        assert postorder(t) == [3, 5]

    def test_right_child_only(self):
        t = build([5, 8])
        assert inorder(t) == [5, 8]
        assert preorder(t) == [5, 8]
        assert postorder(t) == [8, 5]

    def test_root_with_left_grandchild_on_right_of_left(self):
        #   5
        #  /
        # 2
        #  \
        #   4
        t = build([5, 2, 4])
        assert inorder(t) == [2, 4, 5]
        assert preorder(t) == [5, 2, 4]
        assert postorder(t) == [4, 2, 5]

    def test_root_with_right_grandchild_on_left_of_right(self):
        #   5
        #    \
        #     9
        #    /
        #   7
        t = build([5, 9, 7])
        assert inorder(t) == [5, 7, 9]
        assert preorder(t) == [5, 9, 7]
        assert postorder(t) == [7, 9, 5]


# ------------------------- DEGENERATE (SKEWED) TREES --------------------------
class TestSkewedTrees:
    def test_ascending_insertion_is_right_chain(self):
        keys = list(range(1, 9))
        t = build(keys)
        assert inorder(t) == keys
        assert preorder(t) == keys
        assert postorder(t) == keys[::-1]

    def test_descending_insertion_is_left_chain(self):
        keys = list(range(8, 0, -1))
        t = build(keys)
        assert inorder(t) == sorted(keys)
        assert preorder(t) == keys
        assert postorder(t) == sorted(keys)

    def test_zigzag_insertion(self):
        # 1, 10, 2, 9, 3, 8 -> alternating right/left spine
        t = build([1, 10, 2, 9, 3, 8])
        assert inorder(t) == [1, 2, 3, 8, 9, 10]
        assert preorder(t) == [1, 10, 2, 9, 3, 8]
        assert postorder(t) == [8, 3, 9, 2, 10, 1]

    def test_deep_chain_does_not_break(self):
        # Boundary: deep tree. Kept below the default recursion limit (1000)
        # so a recursive implementation is not unfairly penalised.
        n = 400
        t = build(range(n))
        assert inorder(t) == list(range(n))
        assert preorder(t) == list(range(n))
        assert postorder(t) == list(range(n - 1, -1, -1))


# ------------------------------- DUPLICATES (A4) ------------------------------
class TestDuplicates:
    def test_duplicate_root_ignored(self):
        t = build([2, 1, 3, 2])
        assert inorder(t) == [1, 2, 3]
        assert preorder(t) == [2, 1, 3]
        assert postorder(t) == [1, 3, 2]

    def test_duplicate_leaf_ignored(self):
        t = build([2, 1, 3, 1, 3])
        assert inorder(t) == [1, 2, 3]

    def test_duplicates_do_not_change_structure(self):
        base = build([8, 3, 10, 1, 6])
        dup = build([8, 3, 8, 10, 3, 1, 6, 10, 1, 6])
        assert preorder(base) == preorder(dup)
        assert postorder(base) == postorder(dup)
        assert inorder(base) == inorder(dup)

    def test_insert_same_key_does_not_raise(self):
        t = build([1])
        t.put(1)  # must not raise (A4)
        assert inorder(t) == [1]

    def test_all_equal_keys(self):
        t = build([7] * 100)
        assert inorder(t) == [7]


# ------------------------------ KEY TYPES -------------------------------------
class TestKeyTypes:
    def test_negative_and_zero_and_positive(self):
        t = build([0, -5, 5, -10, 10])
        assert inorder(t) == [-10, -5, 0, 5, 10]
        assert preorder(t) == [0, -5, -10, 5, 10]
        assert postorder(t) == [-10, -5, 10, 5, 0]

    def test_floats(self):
        t = build([0.5, -1.5, 2.25, 0.0])
        assert inorder(t) == [-1.5, 0.0, 0.5, 2.25]

    def test_mixed_int_and_float_are_comparable(self):
        t = build([1, 2.5, 0, 1.0])  # 1 == 1.0 -> duplicate under set semantics
        assert inorder(t) == [0, 1, 2.5]

    def test_strings_lexicographic(self):
        t = build(["m", "c", "x", "a", "d"])
        assert inorder(t) == ["a", "c", "d", "m", "x"]
        assert preorder(t) == ["m", "c", "a", "d", "x"]
        assert postorder(t) == ["a", "d", "c", "x", "m"]

    def test_strings_case_sensitive(self):
        t = build(["b", "B", "a", "A"])
        assert inorder(t) == sorted(["b", "B", "a", "A"])

    def test_empty_string_key(self):
        t = build(["", "a"])
        assert inorder(t) == ["", "a"]

    def test_tuples(self):
        t = build([(1, 2), (1, 1), (0, 9)])
        assert inorder(t) == [(0, 9), (1, 1), (1, 2)]

    def test_extreme_ints(self):
        big = 2**200
        t = build([0, big, -big])
        assert inorder(t) == [-big, 0, big]

    def test_float_infinities(self):
        inf = float("inf")
        t = build([0, inf, -inf])
        assert inorder(t) == [-inf, 0, inf]

    def test_bool_keys_behave_as_ints(self):
        # Assumption: bool is an int subclass; True == 1, False == 0.
        t = build([True, False, 1, 0])
        assert inorder(t) == [False, True]


# --------------------------- INVALID INPUTS (A7) ------------------------------
class TestInvalidInputs:
    def test_none_into_empty_tree(self):
        # A7: ambiguous for the first insert (a tree might accept anything
        # when no comparison happens). Assumed to raise TypeError.
        t = build()
        with pytest.raises(TypeError):
            t.put(None)

    def test_none_into_nonempty_tree(self):
        t = build([1, 2, 3])
        with pytest.raises(TypeError):
            t.put(None)
        assert inorder(t) == [1, 2, 3]  # tree unchanged after failure

    def test_incomparable_types_raise(self):
        t = build([1, 2, 3])
        with pytest.raises(TypeError):
            t.put("a")
        assert inorder(t) == [1, 2, 3]

    def test_incomparable_collection_key(self):
        t = build([1])
        with pytest.raises(TypeError):
            t.put([1, 2])

    def test_nan_does_not_corrupt_tree(self):
        # NaN compares False to everything; behaviour is unspecified.
        # We only assert that previously stored keys remain intact and
        # ordered, and that no unexpected exception type escapes.
        t = build([1, 2, 3])
        try:
            t.put(float("nan"))
        except (TypeError, ValueError):
            pass
        remaining = [k for k in inorder(t) if k == k]  # drop NaN
        assert remaining == [1, 2, 3]

    def test_insert_without_argument_raises(self):
        t = build()
        with pytest.raises(TypeError):
            t.put()


# ------------------------------ ORDER PROPERTIES ------------------------------
class TestProperties:
    def test_inorder_sorted_and_unique(self):
        rng = random.Random(1234)
        keys = [rng.randint(-50, 50) for _ in range(200)]
        t = build(keys)
        assert inorder(t) == sorted(set(keys))

    def test_traversals_have_same_elements(self):
        rng = random.Random(99)
        keys = [rng.randint(0, 1000) for _ in range(150)]
        t = build(keys)
        expected = sorted(set(keys))
        assert sorted(preorder(t)) == expected
        assert sorted(postorder(t)) == expected

    def test_preorder_first_is_first_inserted(self):
        t = build([42, 7, 99, 1])
        assert preorder(t)[0] == 42

    def test_postorder_last_is_first_inserted(self):
        t = build([42, 7, 99, 1])
        assert postorder(t)[-1] == 42

    def test_traversal_lengths_equal(self):
        t = build([5, 3, 8, 3, 5, 1, 9])
        n = len(inorder(t))
        assert len(preorder(t)) == n
        assert len(postorder(t)) == n
        assert n == 5

    def test_insertion_order_changes_shape_not_inorder(self):
        a = build([1, 2, 3])
        b = build([3, 2, 1])
        assert inorder(a) == inorder(b) == [1, 2, 3]
        assert preorder(a) != preorder(b)

    @pytest.mark.parametrize("seed", range(20))
    def test_matches_reference_model(self, seed):
        rng = random.Random(seed)
        keys = [rng.randint(-30, 30) for _ in range(rng.randint(0, 60))]
        t = build(keys)
        root = _ref_build(keys)
        assert inorder(t) == _ref_in(root)
        assert preorder(t) == _ref_pre(root)
        assert postorder(t) == _ref_post(root)

    def test_large_random_matches_reference(self):
        rng = random.Random(2024)
        keys = [rng.randint(0, 10**6) for _ in range(2000)]
        t = build(keys)
        root = _ref_build(keys)
        assert inorder(t) == _ref_in(root)
        assert preorder(t) == _ref_pre(root)
        assert postorder(t) == _ref_post(root)


# ------------------------ STATE / IDEMPOTENCE (A9) ----------------------------
class TestStateBehavior:
    def test_traversal_is_repeatable(self):
        t = build([4, 2, 6, 1, 3])
        assert inorder(t) == inorder(t)
        assert preorder(t) == preorder(t)
        assert postorder(t) == postorder(t)

    def test_traversal_does_not_mutate_tree(self):
        t = build([4, 2, 6])
        before = (inorder(t), preorder(t), postorder(t))
        inorder(t), preorder(t), postorder(t)
        assert (inorder(t), preorder(t), postorder(t)) == before

    def test_mutating_returned_list_does_not_affect_tree(self):
        t = build([2, 1, 3])
        out = t.in_order()
        if not isinstance(out, list):
            pytest.skip("traversal does not return a list (A3)")
        out.append(999)
        out.clear()
        assert inorder(t) == [1, 2, 3]

    def test_insert_after_traversal(self):
        t = build([2, 1, 3])
        assert inorder(t) == [1, 2, 3]
        t.put(0)
        t.put(4)
        assert inorder(t) == [0, 1, 2, 3, 4]
        assert preorder(t) == [2, 1, 0, 3, 4]
        assert postorder(t) == [0, 1, 4, 3, 2]

    def test_interleaved_inserts_and_traversals(self):
        t = build()
        expected = []
        for k in [5, 2, 8, 2, 9, 1]:
            t.put(k)
            if k not in expected:
                expected.append(k)
            assert inorder(t) == sorted(expected)

    def test_failed_insert_does_not_change_tree(self):
        t = build([2, 1, 3])
        before = (inorder(t), preorder(t), postorder(t))
        with pytest.raises(TypeError):
            t.put(None)
        assert (inorder(t), preorder(t), postorder(t)) == before


# ------------------------ OPTIONAL FEATURES (A8) ------------------------------
class TestOptionalFeatures:
    def test_len_counts_unique_keys(self):
        t = build([3, 1, 2, 3, 1])
        if not hasattr(t, "__len__"):
            pytest.skip("__len__ not provided (A8)")
        assert len(t) == 3

    def test_len_updates_after_insert(self):
        t = build()
        if not hasattr(t, "__len__"):
            pytest.skip("__len__ not provided (A8)")
        for i, k in enumerate([10, 20, 30], start=1):
            t.put(k)
            assert len(t) == i

    def test_contains(self):
        t = build([5, 3, 8])
        if not hasattr(t, "__contains__"):
            pytest.skip("__contains__ not provided (A8)")
        assert 5 in t and 3 in t and 8 in t
        assert 4 not in t
        assert 0 not in t

    def test_iteration_if_supported(self):
        t = build([3, 1, 2])
        if not hasattr(t, "__iter__"):
            pytest.skip("__iter__ not provided (A8)")
        # Assumption: iteration yields keys in sorted (in-order) sequence.
        assert list(t) == [1, 2, 3]