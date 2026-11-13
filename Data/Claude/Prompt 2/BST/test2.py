"""
Unit tests for BSTSet / BSTNode (binary search tree set), written with pytest.

The description does not give exact names or signatures, so these ASSUMPTIONS are
made explicit. Most can be changed in the CONFIG block below.

A1. The classes live in a module named `BST` (`from BST import BSTNode, BSTSet`).
A2. `BSTSet()` takes no arguments and creates an empty set.
A3. `BSTSet.put(key)` adds a key. Its return value is NOT checked, and inserting a
    duplicate is assumed to be a silent no-op (it must not raise).
A4. Traversals are the methods `in_order()`, `pre_order()` and `post_order()` on
    `BSTSet`. They are assumed to return, or yield, the keys in visit order. Results
    are converted with `list()`, so a list or a generator both work.
A5. `iter(BSTSet)` is assumed to yield keys in ascending (in-order) order.
A6. `__len__` and `__contains__` are not mentioned in the description. Tests for them
    are skipped automatically if the class does not define them.
A7. The structural tests look for the root attribute (`_head`) and for node
    attributes `key`, `left` and `right`. An empty tree is assumed to have a root
    of `None`, and a missing child is assumed to be `None`.
A8. Keys are integers (negative, zero, positive). Behaviour for non-integer or
    otherwise invalid keys (None, strings, floats) is NOT specified, so it is not tested.
A9. Deep, degenerate trees are limited to 300 nodes so that a correct recursive
    implementation does not hit Python's default recursion limit.
A10. Direct BSTNode tests only check what the description implies: a node built from a
     key exposes that key and has no children. They are skipped if the attributes differ.
"""

import itertools
import random
import sys

import pytest

from BST import BSTNode, BSTSet

# --------------------------------------------------------------------------- #
# CONFIG: adjust here if the real names differ from the assumptions above.
# --------------------------------------------------------------------------- #
INSERT = "put"
INORDER = "in_order"
PREORDER = "pre_order"
POSTORDER = "post_order"

ROOT_ATTR_CANDIDATES = ("_head",)
KEY_ATTR_CANDIDATES = ("key",)
LEFT_ATTR = "left"
RIGHT_ATTR = "right"

TRAVERSALS = {"inorder": INORDER, "preorder": PREORDER, "postorder": POSTORDER}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def make(keys):
    """Build a BSTSet by inserting keys in the given order."""
    tree = BSTSet()
    for k in keys:
        getattr(tree, INSERT)(k)
    return tree


def traverse(tree, kind):
    """Run the traversal `kind` ('inorder'|'preorder'|'postorder') and return a list."""
    return list(getattr(tree, TRAVERSALS[kind])())


def _find_root(tree):
    for name in ROOT_ATTR_CANDIDATES:
        if hasattr(tree, name):
            return getattr(tree, name)
    pytest.skip("Cannot locate the root attribute (assumption A7).")


def _node_key(node):
    for name in KEY_ATTR_CANDIDATES:
        if hasattr(node, name):
            return getattr(node, name)
    pytest.skip("Cannot locate the node key attribute (assumption A7).")


def _validate_bst(node, lo=None, hi=None):
    """Check the strict BST property recursively; return the in-order key list."""
    if node is None:
        return []
    k = _node_key(node)
    if lo is not None:
        assert k > lo, f"key {k} violates lower bound {lo}"
    if hi is not None:
        assert k < hi, f"key {k} violates upper bound {hi}"
    left = _validate_bst(getattr(node, LEFT_ATTR), lo, k)
    right = _validate_bst(getattr(node, RIGHT_ATTR), k, hi)
    return left + [k] + right


# --------------------------------------------------------------------------- #
# Table of hand-computed expected results.
# (id, insertion order, expected inorder, expected preorder, expected postorder)
# --------------------------------------------------------------------------- #
CASES = [
    ("empty", [], [], [], []),
    ("single_positive", [42], [42], [42], [42]),
    ("single_zero", [0], [0], [0], [0]),
    ("single_negative", [-7], [-7], [-7], [-7]),
    # Root with only a left child
    ("only_left_child", [5, 3], [3, 5], [5, 3], [3, 5]),
    # Root with only a right child
    ("only_right_child", [5, 7], [5, 7], [5, 7], [7, 5]),
    # Perfect tree of three nodes (smaller and larger than root)
    ("three_node_balanced", [2, 1, 3], [1, 2, 3], [2, 1, 3], [1, 3, 2]),
    ("three_node_balanced_other_order", [2, 3, 1], [1, 2, 3], [2, 1, 3], [1, 3, 2]),
    # Missing children at inner nodes
    ("left_child_with_right_grandchild", [10, 5, 7], [5, 7, 10], [10, 5, 7], [7, 5, 10]),
    ("right_child_with_left_grandchild", [10, 15, 12], [10, 12, 15], [10, 15, 12], [12, 15, 10]),
    # Degenerate (linked-list shaped) trees
    ("ascending_chain", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
    ("descending_chain", [5, 4, 3, 2, 1], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    # Zig-zag: 1 -> right 5 -> left 2 -> right 4 -> left 3
    ("zigzag", [1, 5, 2, 4, 3], [1, 2, 3, 4, 5], [1, 5, 2, 4, 3], [3, 4, 2, 5, 1]),
    # Larger, uneven tree:
    #          8
    #       3     10
    #     1   6      14
    #        4 7    13
    (
        "larger_uneven",
        [8, 3, 10, 1, 6, 14, 4, 7, 13],
        [1, 3, 4, 6, 7, 8, 10, 13, 14],
        [8, 3, 1, 6, 4, 7, 10, 14, 13],
        [1, 4, 7, 6, 3, 13, 14, 10, 8],
    ),
    # Negative, zero and positive keys:
    #            0
    #        -5     5
    #     -10 -1   3 10
    (
        "negative_zero_positive",
        [0, -5, 5, -10, -1, 3, 10],
        [-10, -5, -1, 0, 3, 5, 10],
        [0, -5, -10, -1, 5, 3, 10],
        [-10, -1, -5, 3, 10, 5, 0],
    ),
    ("all_negative", [-1, -3, -2, -5], [-5, -3, -2, -1], [-1, -3, -5, -2], [-5, -2, -3, -1]),
    # Duplicates must be ignored: resulting tree is 5(3, 8)
    ("duplicates_mixed", [5, 3, 5, 3, 8, 8], [3, 5, 8], [5, 3, 8], [3, 8, 5]),
    ("duplicates_only_root", [5, 5, 5, 5], [5], [5], [5]),
    ("duplicate_leaf_reinserted", [2, 1, 3, 1, 3], [1, 2, 3], [2, 1, 3], [1, 3, 2]),
    # Very large magnitudes
    (
        "extreme_integers",
        [0, sys.maxsize, -sys.maxsize - 1, 10**18, -(10**18)],
        [-sys.maxsize - 1, -(10**18), 0, 10**18, sys.maxsize],
        [0, -sys.maxsize - 1, -(10**18), sys.maxsize, 10**18],
        [-(10**18), -sys.maxsize - 1, 10**18, sys.maxsize, 0],
    ),
]
CASE_IDS = [c[0] for c in CASES]


# --------------------------------------------------------------------------- #
# Traversal order tests
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name,keys,expected_in,expected_pre,expected_post", CASES, ids=CASE_IDS)
def test_inorder_traversal(name, keys, expected_in, expected_pre, expected_post):
    assert traverse(make(keys), "inorder") == expected_in


@pytest.mark.parametrize("name,keys,expected_in,expected_pre,expected_post", CASES, ids=CASE_IDS)
def test_preorder_traversal(name, keys, expected_in, expected_pre, expected_post):
    assert traverse(make(keys), "preorder") == expected_pre


@pytest.mark.parametrize("name,keys,expected_in,expected_pre,expected_post", CASES, ids=CASE_IDS)
def test_postorder_traversal(name, keys, expected_in, expected_pre, expected_post):
    assert traverse(make(keys), "postorder") == expected_post


# --------------------------------------------------------------------------- #
# Empty tree
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("kind", ["inorder", "preorder", "postorder"])
def test_empty_tree_traversals_are_empty(kind):
    assert traverse(BSTSet(), kind) == []


def test_empty_tree_iteration_is_empty():
    assert list(BSTSet()) == []


def test_empty_tree_root_is_none():
    # Assumption A7: an empty tree's root is None.
    assert _find_root(BSTSet()) is None


@pytest.mark.skipif(not hasattr(BSTSet, "__len__"), reason="__len__ not defined (A6)")
def test_empty_tree_len_is_zero():
    assert len(BSTSet()) == 0


@pytest.mark.skipif(not hasattr(BSTSet, "__contains__"), reason="__contains__ not defined (A6)")
@pytest.mark.parametrize("key", [-1, 0, 1])
def test_empty_tree_contains_nothing(key):
    assert key not in BSTSet()


# --------------------------------------------------------------------------- #
# Single node
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("key", [-100, 0, 100])
def test_single_node_all_traversals_and_iteration(key):
    tree = make([key])
    for kind in TRAVERSALS:
        assert traverse(tree, kind) == [key]
    assert list(tree) == [key]


def test_single_node_has_no_children():
    root = _find_root(make([9]))
    assert _node_key(root) == 9
    assert getattr(root, LEFT_ATTR) is None
    assert getattr(root, RIGHT_ATTR) is None


# --------------------------------------------------------------------------- #
# Smaller / larger than root and the resulting structure
# --------------------------------------------------------------------------- #
def test_smaller_key_goes_to_left_subtree():
    root = _find_root(make([10, 4]))
    left = getattr(root, LEFT_ATTR)
    assert left is not None and _node_key(left) == 4
    assert getattr(root, RIGHT_ATTR) is None


def test_larger_key_goes_to_right_subtree():
    root = _find_root(make([10, 20]))
    right = getattr(root, RIGHT_ATTR)
    assert right is not None and _node_key(right) == 20
    assert getattr(root, LEFT_ATTR) is None


def test_first_inserted_key_is_root():
    for keys in ([5, 1, 9], [1, 5, 9], [9, 5, 1]):
        assert _node_key(_find_root(make(keys))) == keys[0]


def test_ascending_insertion_builds_right_chain():
    node = _find_root(make([1, 2, 3, 4]))
    for expected in (1, 2, 3, 4):
        assert node is not None
        assert _node_key(node) == expected
        assert getattr(node, LEFT_ATTR) is None
        node = getattr(node, RIGHT_ATTR)
    assert node is None


def test_descending_insertion_builds_left_chain():
    node = _find_root(make([4, 3, 2, 1]))
    for expected in (4, 3, 2, 1):
        assert node is not None
        assert _node_key(node) == expected
        assert getattr(node, RIGHT_ATTR) is None
        node = getattr(node, LEFT_ATTR)
    assert node is None


def test_bst_property_holds_for_larger_tree():
    tree = make([8, 3, 10, 1, 6, 14, 4, 7, 13])
    assert _validate_bst(_find_root(tree)) == [1, 3, 4, 6, 7, 8, 10, 13, 14]


# --------------------------------------------------------------------------- #
# Duplicates / uniqueness
# --------------------------------------------------------------------------- #
def test_duplicate_insert_does_not_raise():
    tree = make([5])
    getattr(tree, INSERT)(5)  # A3: silent no-op


def test_duplicate_insert_does_not_create_duplicate_in_any_traversal():
    tree = make([5, 3, 8])
    for dup in (5, 3, 8, 5, 3, 8):
        getattr(tree, INSERT)(dup)
    assert traverse(tree, "inorder") == [3, 5, 8]
    assert traverse(tree, "preorder") == [5, 3, 8]
    assert traverse(tree, "postorder") == [3, 8, 5]
    assert list(tree) == [3, 5, 8]


def test_duplicate_insert_does_not_change_structure():
    tree = make([5, 3, 8])
    before = traverse(tree, "preorder")
    getattr(tree, INSERT)(3)
    assert traverse(tree, "preorder") == before


def test_many_duplicates_of_same_key_yield_single_key():
    tree = make([7] * 50)
    assert traverse(tree, "inorder") == [7]
    assert list(tree) == [7]


def test_zero_is_treated_as_a_regular_unique_key():
    # Guards against falsy-value bugs such as `if not key` or `if not node`.
    tree = make([0, 0, -1, 1, 0])
    assert traverse(tree, "inorder") == [-1, 0, 1]
    assert traverse(tree, "preorder") == [0, -1, 1]
    assert traverse(tree, "postorder") == [-1, 1, 0]


@pytest.mark.skipif(not hasattr(BSTSet, "__len__"), reason="__len__ not defined (A6)")
def test_len_counts_unique_keys_only():
    assert len(make([4, 2, 4, 6, 2, 6, 4])) == 3


@pytest.mark.skipif(not hasattr(BSTSet, "__len__"), reason="__len__ not defined (A6)")
def test_len_grows_by_one_per_new_key():
    tree = BSTSet()
    for i, k in enumerate([3, 1, 2, 5, 4], start=1):
        getattr(tree, INSERT)(k)
        assert len(tree) == i


@pytest.mark.skipif(not hasattr(BSTSet, "__contains__"), reason="__contains__ not defined (A6)")
def test_contains_reports_inserted_and_missing_keys():
    tree = make([5, 3, 8, -2, 0])
    for k in (5, 3, 8, -2, 0):
        assert k in tree
    for k in (-3, 1, 4, 6, 100):
        assert k not in tree


# --------------------------------------------------------------------------- #
# Insertion order independence and ordering invariants
# --------------------------------------------------------------------------- #
def test_inorder_is_ascending_for_every_permutation_of_small_set():
    keys = [-3, 0, 2, 5, 9]
    for perm in itertools.permutations(keys):
        assert traverse(make(perm), "inorder") == sorted(keys), f"failed for {perm}"


def test_every_permutation_yields_the_same_key_set_in_all_traversals():
    keys = [4, 1, 7, 3]
    for perm in itertools.permutations(keys):
        tree = make(perm)
        for kind in TRAVERSALS:
            assert sorted(traverse(tree, kind)) == sorted(keys)
            assert len(traverse(tree, kind)) == len(keys)


def test_root_first_in_preorder_and_last_in_postorder():
    for perm in itertools.permutations([2, 4, 6, 8]):
        tree = make(perm)
        assert traverse(tree, "preorder")[0] == perm[0]
        assert traverse(tree, "postorder")[-1] == perm[0]


def test_randomized_inserts_with_duplicates_match_sorted_unique():
    rng = random.Random(12345)  # fixed seed -> deterministic
    for _ in range(25):
        keys = [rng.randint(-50, 50) for _ in range(rng.randint(0, 80))]
        tree = make(keys)
        expected = sorted(set(keys))
        assert traverse(tree, "inorder") == expected
        assert list(tree) == expected
        assert sorted(traverse(tree, "preorder")) == expected
        assert sorted(traverse(tree, "postorder")) == expected
        assert len(traverse(tree, "preorder")) == len(expected)
        assert len(traverse(tree, "postorder")) == len(expected)


def test_randomized_trees_satisfy_bst_property_structurally():
    rng = random.Random(2024)
    for _ in range(25):
        keys = [rng.randint(-100, 100) for _ in range(rng.randint(0, 60))]
        tree = make(keys)
        assert _validate_bst(_find_root(tree)) == sorted(set(keys))


def test_rebuilding_from_preorder_reproduces_identical_tree():
    # In a BST, inserting the preorder sequence into a new tree gives the same shape.
    rng = random.Random(7)
    keys = [rng.randint(-30, 30) for _ in range(40)]
    original = make(keys)
    rebuilt = make(traverse(original, "preorder"))
    for kind in TRAVERSALS:
        assert traverse(rebuilt, kind) == traverse(original, kind)


def test_negative_zero_and_positive_keys_are_ordered_numerically():
    tree = make([3, -3, 0, -10, 10, 2, -2])
    assert traverse(tree, "inorder") == [-10, -3, -2, 0, 2, 3, 10]


def test_multi_digit_keys_are_not_ordered_as_strings():
    # Guards against lexicographic comparison bugs (e.g. "10" < "9").
    assert traverse(make([9, 10, 100, 2, 11]), "inorder") == [2, 9, 10, 11, 100]


# --------------------------------------------------------------------------- #
# Iteration
# --------------------------------------------------------------------------- #
def test_iteration_yields_keys_in_ascending_order():
    assert list(make([8, 3, 10, 1, 6, 14, 4, 7, 13])) == [1, 3, 4, 6, 7, 8, 10, 13, 14]


def test_iteration_matches_inorder_traversal():
    tree = make([5, -1, 9, 0, 7, 12, -8])
    assert list(tree) == traverse(tree, "inorder")


def test_iteration_can_be_repeated():
    tree = make([3, 1, 2])
    assert list(tree) == [1, 2, 3]
    assert list(tree) == [1, 2, 3]


def test_iteration_reflects_later_inserts():
    tree = make([5, 1])
    assert list(tree) == [1, 5]
    getattr(tree, INSERT)(3)
    assert list(tree) == [1, 3, 5]


def test_iteration_supports_for_loop_and_sorted_builtin():
    tree = make([4, 2, 6, 1, 3])
    collected = []
    for k in tree:
        collected.append(k)
    assert collected == [1, 2, 3, 4, 6]
    assert sorted(tree) == collected


def test_iteration_does_not_modify_tree():
    tree = make([4, 2, 6])
    pre_before = traverse(tree, "preorder")
    _ = list(tree)
    assert traverse(tree, "preorder") == pre_before


# --------------------------------------------------------------------------- #
# State, repeatability, independence
# --------------------------------------------------------------------------- #
def test_traversals_are_repeatable_and_do_not_mutate():
    tree = make([8, 3, 10, 1, 6])
    for kind in TRAVERSALS:
        first = traverse(tree, kind)
        second = traverse(tree, kind)
        assert first == second


def test_insert_after_traversal_is_reflected():
    tree = make([5])
    assert traverse(tree, "inorder") == [5]
    getattr(tree, INSERT)(2)
    getattr(tree, INSERT)(8)
    assert traverse(tree, "inorder") == [2, 5, 8]
    assert traverse(tree, "preorder") == [5, 2, 8]
    assert traverse(tree, "postorder") == [2, 8, 5]


def test_incremental_inserts_keep_inorder_sorted_after_each_step():
    tree = BSTSet()
    seen = set()
    for k in [5, 2, 8, 2, 9, 1, 5, 7, 0, -1]:
        getattr(tree, INSERT)(k)
        seen.add(k)
        assert traverse(tree, "inorder") == sorted(seen)


def test_separate_instances_do_not_share_state():
    a = make([1, 2, 3])
    b = BSTSet()
    assert traverse(b, "inorder") == []
    getattr(b, INSERT)(99)
    assert traverse(a, "inorder") == [1, 2, 3]
    assert traverse(b, "inorder") == [99]


def test_new_instance_is_empty_even_after_another_was_populated():
    make([1, 2, 3])
    assert traverse(BSTSet(), "inorder") == []


# --------------------------------------------------------------------------- #
# Larger / stress-style inputs
# --------------------------------------------------------------------------- #
def test_long_ascending_sequence():
    keys = list(range(300))  # A9: stay below recursion limits
    tree = make(keys)
    assert traverse(tree, "inorder") == keys
    assert traverse(tree, "preorder") == keys
    assert traverse(tree, "postorder") == keys[::-1]


def test_long_descending_sequence():
    keys = list(range(300, 0, -1))
    tree = make(keys)
    assert traverse(tree, "inorder") == sorted(keys)
    assert traverse(tree, "preorder") == keys
    assert traverse(tree, "postorder") == sorted(keys)


def test_balanced_insertion_order_of_fifteen_keys():
    # Median-first insertion gives a perfect tree of height 4 (keys 1..15).
    order = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    tree = make(order)
    assert traverse(tree, "inorder") == list(range(1, 16))
    assert traverse(tree, "preorder") == order
    assert traverse(tree, "postorder") == [1, 3, 2, 5, 7, 6, 4, 9, 11, 10, 13, 15, 14, 12, 8]


# --------------------------------------------------------------------------- #
# BSTNode (minimal, assumption A10)
# --------------------------------------------------------------------------- #
def test_bstnode_stores_key_and_starts_without_children():
    node = BSTNode(5)
    assert _node_key(node) == 5
    assert getattr(node, LEFT_ATTR) is None
    assert getattr(node, RIGHT_ATTR) is None


@pytest.mark.parametrize("key", [-1, 0, 1])
def test_bstnode_accepts_negative_zero_and_positive_keys(key):
    assert _node_key(BSTNode(key)) == key