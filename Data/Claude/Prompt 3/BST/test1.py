"""
Unit tests for a Binary Search Tree (BST) set, written with pytest.

ASSUMPTIONS (the description is brief, so these are made explicit; adjust the
CONFIG section if your program differs):

 A1. The class is `BSTSet`, importable from module `BST`, and takes no
     constructor arguments.
 A2. `put(key)` adds a key. Its return value is NOT tested (unspecified).
 A3. Set semantics: inserting a key that is already present (by `==`) leaves
     the tree unchanged, with no duplicates and no error.
 A4. Traversals are zero-argument methods `in_order()`, `pre_order()` and
     `post_order()`. Each returns a list or any iterable; the tests wrap the
     result in `list()`.
 A5. Standard definitions: inorder = left, node, right; preorder = node, left,
     right; postorder = left, right, node. Left subtree holds smaller keys.
 A6. Traversal of an empty set yields an empty sequence (no error).
 A7. Keys must be mutually comparable with `<`. Inserting an incomparable key
     into a non-empty set is assumed to raise TypeError.
 A8. Traversals do not mutate the set.
 A9. Optional features (`level_order()`, `len()`, `in`) are tested only if
     the class provides them; otherwise those tests are skipped.
 A10. Very deep (degenerate) trees may hit Python's recursion limit if the
     implementation is recursive. That is reported as xfail, not a hard failure.
"""

import random

import pytest

# ----------------------------- CONFIG ---------------------------------------
from BST import BSTSet  # noqa: E402  (adjust module/class name if needed)

INSERT = "put"
INORDER = "in_order"
PREORDER = "pre_order"
POSTORDER = "post_order"
LEVELORDER = "level_order"  # optional

TRAVERSALS = [INORDER, PREORDER, POSTORDER]
# ----------------------------------------------------------------------------


# ------------------------------ helpers -------------------------------------
def make(keys=()):
    tree = BSTSet()
    for k in keys:
        getattr(tree, INSERT)(k)
    return tree


def trav(tree, name):
    return list(getattr(tree, name)())


def ins(tree, key):
    return getattr(tree, INSERT)(key)


# Canonical balanced tree:
#            50
#          /    \
#        30      70
#       /  \    /  \
#     20   40  60   80
BALANCED_KEYS = [50, 30, 70, 20, 40, 60, 80]


# ============================ NORMAL CASES ===================================
class TestNormalCases:
    def test_inorder_balanced_tree(self):
        assert trav(make(BALANCED_KEYS), INORDER) == [20, 30, 40, 50, 60, 70, 80]

    def test_preorder_balanced_tree(self):
        assert trav(make(BALANCED_KEYS), PREORDER) == [50, 30, 20, 40, 70, 60, 80]

    def test_postorder_balanced_tree(self):
        assert trav(make(BALANCED_KEYS), POSTORDER) == [20, 40, 30, 60, 80, 70, 50]

    def test_unbalanced_mixed_tree_all_orders(self):
        #       5
        #      / \
        #     3   8
        #      \   \
        #       4   9
        tree = make([5, 3, 8, 4, 9])
        assert trav(tree, INORDER) == [3, 4, 5, 8, 9]
        assert trav(tree, PREORDER) == [5, 3, 4, 8, 9]
        assert trav(tree, POSTORDER) == [4, 3, 9, 8, 5]

    def test_inorder_is_sorted_regardless_of_insertion_order(self):
        keys = [8, 3, 10, 1, 6, 14, 4, 7, 13]
        assert trav(make(keys), INORDER) == sorted(keys)

    def test_different_insertion_orders_same_inorder_different_preorder(self):
        a = make([1, 2, 3])
        b = make([2, 1, 3])
        assert trav(a, INORDER) == trav(b, INORDER) == [1, 2, 3]
        assert trav(a, PREORDER) == [1, 2, 3]
        assert trav(b, PREORDER) == [2, 1, 3]

    def test_insert_after_traversal_is_reflected(self):
        tree = make([2, 1])
        assert trav(tree, INORDER) == [1, 2]
        ins(tree, 3)
        assert trav(tree, INORDER) == [1, 2, 3]

    def test_traversal_is_repeatable_and_non_mutating(self):
        tree = make(BALANCED_KEYS)
        first = [trav(tree, t) for t in TRAVERSALS]
        second = [trav(tree, t) for t in TRAVERSALS]
        assert first == second


# ============================= EDGE CASES ====================================
class TestEdgeCases:
    @pytest.mark.parametrize("name", TRAVERSALS)
    def test_empty_tree_traversal_is_empty(self, name):
        assert trav(make(), name) == []

    @pytest.mark.parametrize("name", TRAVERSALS)
    def test_single_element(self, name):
        assert trav(make([42]), name) == [42]

    @pytest.mark.parametrize("name", TRAVERSALS)
    def test_two_elements_left_child(self, name):
        expected = {INORDER: [1, 2], PREORDER: [2, 1], POSTORDER: [1, 2]}[name]
        assert trav(make([2, 1]), name) == expected

    @pytest.mark.parametrize("name", TRAVERSALS)
    def test_two_elements_right_child(self, name):
        expected = {INORDER: [1, 2], PREORDER: [1, 2], POSTORDER: [2, 1]}[name]
        assert trav(make([1, 2]), name) == expected

    def test_ascending_insertion_right_skewed(self):
        tree = make([1, 2, 3, 4, 5])
        assert trav(tree, INORDER) == [1, 2, 3, 4, 5]
        assert trav(tree, PREORDER) == [1, 2, 3, 4, 5]
        assert trav(tree, POSTORDER) == [5, 4, 3, 2, 1]

    def test_descending_insertion_left_skewed(self):
        tree = make([5, 4, 3, 2, 1])
        assert trav(tree, INORDER) == [1, 2, 3, 4, 5]
        assert trav(tree, PREORDER) == [5, 4, 3, 2, 1]
        assert trav(tree, POSTORDER) == [1, 2, 3, 4, 5]

    def test_zig_zag_insertion(self):
        # 1 -> right 5 -> left 2 -> right 4 -> left 3
        tree = make([1, 5, 2, 4, 3])
        assert trav(tree, INORDER) == [1, 2, 3, 4, 5]
        assert trav(tree, PREORDER) == [1, 5, 2, 4, 3]
        assert trav(tree, POSTORDER) == [3, 4, 2, 5, 1]

    def test_root_is_first_in_preorder_and_last_in_postorder(self):
        tree = make([10, 5, 15, 3, 7])
        assert trav(tree, PREORDER)[0] == 10
        assert trav(tree, POSTORDER)[-1] == 10

    def test_min_and_max_positions(self):
        tree = make(BALANCED_KEYS)
        assert trav(tree, INORDER)[0] == 20
        assert trav(tree, INORDER)[-1] == 80

    def test_negative_zero_and_positive_keys(self):
        tree = make([0, -5, 5, -10, 10])
        assert trav(tree, INORDER) == [-10, -5, 0, 5, 10]
        assert trav(tree, PREORDER) == [0, -5, -10, 5, 10]
        assert trav(tree, POSTORDER) == [-10, -5, 10, 5, 0]

    def test_very_large_and_small_integers(self):
        big, small = 10**30, -(10**30)
        tree = make([0, big, small])
        assert trav(tree, INORDER) == [small, 0, big]

    def test_leaf_only_right_chain_then_left_branch(self):
        tree = make([10, 20, 15])
        assert trav(tree, INORDER) == [10, 15, 20]
        assert trav(tree, PREORDER) == [10, 20, 15]
        assert trav(tree, POSTORDER) == [15, 20, 10]


# ========================== SET SEMANTICS (DUPLICATES) =======================
class TestDuplicates:
    @pytest.mark.parametrize("name", TRAVERSALS)
    def test_duplicate_insert_into_single_node(self, name):
        assert trav(make([7, 7]), name) == [7]

    def test_duplicate_of_root_ignored(self):
        tree = make(BALANCED_KEYS + [50])
        assert trav(tree, INORDER) == [20, 30, 40, 50, 60, 70, 80]
        assert trav(tree, PREORDER) == [50, 30, 20, 40, 70, 60, 80]

    def test_duplicate_of_leaf_ignored(self):
        tree = make(BALANCED_KEYS + [20, 80])
        assert trav(tree, INORDER) == [20, 30, 40, 50, 60, 70, 80]

    def test_many_duplicates_of_same_key(self):
        assert trav(make([3] * 100), INORDER) == [3]

    def test_duplicates_do_not_change_structure(self):
        base = make([5, 3, 8])
        dup = make([5, 3, 8, 3, 5, 8, 3])
        for name in TRAVERSALS:
            assert trav(base, name) == trav(dup, name)

    def test_repeated_reinsertion_is_idempotent(self):
        tree = make([2, 1, 3])
        before = [trav(tree, t) for t in TRAVERSALS]
        for k in (1, 2, 3):
            ins(tree, k)
        after = [trav(tree, t) for t in TRAVERSALS]
        assert before == after

    def test_int_and_equal_float_treated_as_same_key(self):
        # ASSUMPTION: equality-based set semantics, so 1 == 1.0 is a duplicate.
        tree = make([1, 1.0])
        assert len(trav(tree, INORDER)) == 1


# ============================ UNUSUAL INPUTS =================================
class TestUnusualInputs:
    def test_string_keys(self):
        tree = make(["m", "c", "x", "a", "d"])
        assert trav(tree, INORDER) == ["a", "c", "d", "m", "x"]
        assert trav(tree, PREORDER) == ["m", "c", "a", "d", "x"]
        assert trav(tree, POSTORDER) == ["a", "d", "c", "x", "m"]

    def test_string_keys_are_case_sensitive(self):
        tree = make(["b", "B", "a", "A"])
        assert trav(tree, INORDER) == sorted(["b", "B", "a", "A"])

    def test_empty_string_key(self):
        assert trav(make(["", "a"]), INORDER) == ["", "a"]

    def test_float_keys(self):
        tree = make([2.5, 1.5, 3.5, -0.5])
        assert trav(tree, INORDER) == [-0.5, 1.5, 2.5, 3.5]

    def test_mixed_int_and_float_keys(self):
        tree = make([2, 1.5, 3, 2.5])
        assert trav(tree, INORDER) == [1.5, 2, 2.5, 3]

    def test_tuple_keys(self):
        tree = make([(2, "b"), (1, "z"), (2, "a")])
        assert trav(tree, INORDER) == [(1, "z"), (2, "a"), (2, "b")]

    def test_negative_zero_float_equals_zero(self):
        # 0.0 == -0.0, so under set semantics this is one element.
        assert len(trav(make([0.0, -0.0]), INORDER)) == 1

    def test_infinite_float_keys(self):
        inf = float("inf")
        tree = make([0, inf, -inf])
        assert trav(tree, INORDER) == [-inf, 0, inf]

    def test_unicode_string_keys(self):
        keys = ["é", "a", "z", "ñ"]
        assert trav(make(keys), INORDER) == sorted(keys)

    def test_bool_keys_behave_as_ints(self):
        # ASSUMPTION: bool is an int subclass, so True == 1.
        tree = make([True, 0])
        assert trav(tree, INORDER) == [0, True]


# ============================ INVALID INPUTS =================================
class TestInvalidInputs:
    def test_insert_incomparable_type_into_int_tree_raises_type_error(self):
        tree = make([1, 2, 3])
        with pytest.raises(TypeError):
            ins(tree, "a")

    def test_insert_int_into_string_tree_raises_type_error(self):
        tree = make(["a", "b"])
        with pytest.raises(TypeError):
            ins(tree, 5)

    def test_insert_none_into_non_empty_int_tree_raises(self):
        # ASSUMPTION: None is not orderable against ints -> TypeError.
        # ValueError is also accepted in case the implementation validates input.
        tree = make([1, 2])
        with pytest.raises((TypeError, ValueError)):
            ins(tree, None)

    def test_insert_list_key_into_int_tree_raises_type_error(self):
        tree = make([1])
        with pytest.raises(TypeError):
            ins(tree, [1, 2])

    def test_insert_with_no_argument_raises_type_error(self):
        tree = make()
        with pytest.raises(TypeError):
            getattr(tree, INSERT)()

    def test_failed_insert_leaves_tree_unchanged(self):
        tree = make([2, 1, 3])
        before = [trav(tree, t) for t in TRAVERSALS]
        with pytest.raises(TypeError):
            ins(tree, "bad")
        after = [trav(tree, t) for t in TRAVERSALS]
        assert before == after

    def test_nan_key_does_not_corrupt_existing_keys(self):
        # ASSUMPTION: NaN behavior is unspecified. We only require that the
        # implementation does not lose the previously inserted keys or crash
        # with something other than a normal exception.
        tree = make([1, 2, 3])
        try:
            ins(tree, float("nan"))
        except (TypeError, ValueError):
            return
        result = trav(tree, INORDER)
        assert {1, 2, 3}.issubset(set(result))


# ============================= PROPERTY / SCALE ==============================
class TestPropertiesAndScale:
    @pytest.mark.parametrize("name", TRAVERSALS)
    def test_each_traversal_is_permutation_of_distinct_keys(self, name):
        keys = [5, 3, 5, 8, 3, 1, 9, 1]
        result = trav(make(keys), name)
        assert sorted(result) == sorted(set(keys))
        assert len(result) == len(set(result))

    def test_random_keys_inorder_sorted_and_unique(self):
        rng = random.Random(12345)
        keys = [rng.randint(-500, 500) for _ in range(500)]
        assert trav(make(keys), INORDER) == sorted(set(keys))

    @pytest.mark.parametrize("seed", [0, 1, 2, 3, 4])
    def test_random_shuffles_same_inorder(self, seed):
        rng = random.Random(seed)
        keys = list(range(100))
        rng.shuffle(keys)
        assert trav(make(keys), INORDER) == list(range(100))

    def test_rebuilding_from_preorder_reproduces_same_tree(self):
        rng = random.Random(99)
        keys = rng.sample(range(1000), 200)
        original = make(keys)
        rebuilt = make(trav(original, PREORDER))
        for name in TRAVERSALS:
            assert trav(original, name) == trav(rebuilt, name)

    def test_rebuilding_from_reversed_postorder_reproduces_same_preorder(self):
        # Reversed postorder visits root first, then right subtree, then left
        # subtree; inserting in that order reproduces the same tree.
        rng = random.Random(7)
        keys = rng.sample(range(1000), 100)
        original = make(keys)
        rebuilt = make(list(reversed(trav(original, POSTORDER))))
        assert trav(original, PREORDER) == trav(rebuilt, PREORDER)

    def test_large_balanced_insertion(self):
        # Midpoint-first insertion keeps the tree shallow.
        def midpoints(lo, hi):
            if lo > hi:
                return
            mid = (lo + hi) // 2
            yield mid
            yield from midpoints(lo, mid - 1)
            yield from midpoints(mid + 1, hi)

        keys = list(midpoints(0, 9999))
        assert trav(make(keys), INORDER) == list(range(10000))

    def test_moderately_deep_degenerate_tree(self):
        n = 400
        tree = make(range(n))
        assert trav(tree, INORDER) == list(range(n))
        assert trav(tree, PREORDER) == list(range(n))
        assert trav(tree, POSTORDER) == list(range(n - 1, -1, -1))

    @pytest.mark.xfail(
        raises=RecursionError,
        strict=False,
        reason="A recursive implementation may exceed Python's recursion limit "
        "on a 5000-deep degenerate tree (assumption A10).",
    )
    def test_very_deep_degenerate_tree(self):
        n = 5000
        tree = make(range(n))
        assert trav(tree, INORDER) == list(range(n))

    def test_two_instances_do_not_share_state(self):
        a = make([1, 2, 3])
        b = make()
        assert trav(b, INORDER) == []
        ins(b, 99)
        assert trav(a, INORDER) == [1, 2, 3]
        assert trav(b, INORDER) == [99]

    def test_new_instance_after_use_starts_empty(self):
        make([1, 2, 3])
        assert trav(BSTSet(), INORDER) == []


# ========================= OPTIONAL FEATURES (A9) ============================
class TestOptionalFeatures:
    def test_level_order_if_available(self):
        tree = make(BALANCED_KEYS)
        if not hasattr(tree, LEVELORDER):
            pytest.skip("level_order not provided")
        assert trav(tree, LEVELORDER) == [50, 30, 70, 20, 40, 60, 80]

    def test_level_order_empty_if_available(self):
        tree = make()
        if not hasattr(tree, LEVELORDER):
            pytest.skip("level_order not provided")
        assert trav(tree, LEVELORDER) == []

    def test_len_counts_distinct_keys_if_available(self):
        tree = make([1, 2, 2, 3, 3, 3])
        try:
            size = len(tree)
        except TypeError:
            pytest.skip("__len__ not provided")
        assert size == 3

    def test_contains_if_available(self):
        tree = make([1, 2, 3])
        try:
            present = 2 in tree
            absent = 99 in tree
        except TypeError:
            pytest.skip("__contains__ not provided")
        assert present is True
        assert absent is False