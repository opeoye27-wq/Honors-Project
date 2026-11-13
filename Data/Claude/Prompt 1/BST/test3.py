# test_bst.py
# Assumes the program is saved as bst.py next to this file; change the import if not.
# Run with:  python -m unittest test_bst -v    (or: pytest test_bst.py)
#
# Tests marked "BUG:" assert the correct behavior and currently FAIL against the
# given code, which exposes the defect described in the comment.

import random
import sys
import unittest

from BST import BSTNode, BSTNode_Iterator, BSTSet


def build_node(keys):
    """Helper: build a BSTNode tree by inserting keys in order (keys[0] is the root)."""
    root = BSTNode(keys[0])
    for k in keys[1:]:
        root.put(k)
    return root


def build_set(keys):
    s = BSTSet()
    for k in keys:
        s.put(k)
    return s


# Shape used in several tests:
#           8
#         /   \
#        3     10
#       / \      \
#      1   6      14
#         / \     /
#        4   7   13
SAMPLE_KEYS = [8, 3, 10, 1, 6, 14, 4, 7, 13]
SAMPLE_IN_ORDER = [1, 3, 4, 6, 7, 8, 10, 13, 14]
SAMPLE_PRE_ORDER = [8, 3, 1, 6, 4, 7, 10, 14, 13]
SAMPLE_POST_ORDER = [1, 4, 7, 6, 3, 13, 14, 10, 8]


class TestBSTNodeConstruction(unittest.TestCase):
    def test_defaults(self):
        n = BSTNode(5)
        self.assertEqual(n.key, 5)
        self.assertIsNone(n.left)
        self.assertIsNone(n.right)

    def test_explicit_children(self):
        left, right = BSTNode(1), BSTNode(9)
        n = BSTNode(5, left, right)
        self.assertIs(n.left, left)
        self.assertIs(n.right, right)

    def test_keyword_children(self):
        right = BSTNode(9)
        n = BSTNode(5, right=right)
        self.assertIsNone(n.left)
        self.assertIs(n.right, right)

    def test_manually_built_tree_traverses_correctly(self):
        n = BSTNode(2, BSTNode(1), BSTNode(3))
        self.assertEqual(list(n.in_order()), [1, 2, 3])
        self.assertEqual(list(n.pre_order()), [2, 1, 3])
        self.assertEqual(list(n.post_order()), [1, 3, 2])

    def test_non_numeric_key_types_stored(self):
        self.assertEqual(BSTNode("a").key, "a")
        self.assertEqual(BSTNode((1, 2)).key, (1, 2))
        self.assertIsNone(BSTNode(None).key)


class TestBSTNodeRepr(unittest.TestCase):
    def test_repr_int(self):
        self.assertEqual(repr(BSTNode(5)), "BSTNode(key=5)")

    def test_repr_negative(self):
        self.assertEqual(repr(BSTNode(-3)), "BSTNode(key=-3)")

    def test_repr_string_key_uses_str_format(self):
        # The f-string uses {self.key} (not !r), so no quotes around strings.
        self.assertEqual(repr(BSTNode("abc")), "BSTNode(key=abc)")

    def test_repr_none_key(self):
        self.assertEqual(repr(BSTNode(None)), "BSTNode(key=None)")

    def test_repr_ignores_children(self):
        self.assertEqual(repr(BSTNode(2, BSTNode(1), BSTNode(3))), "BSTNode(key=2)")

    def test_str_falls_back_to_repr(self):
        self.assertEqual(str(BSTNode(7)), "BSTNode(key=7)")


class TestBSTNodePut(unittest.TestCase):
    def test_put_smaller_goes_left(self):
        n = BSTNode(5)
        n.put(2)
        self.assertEqual(n.left.key, 2)
        self.assertIsNone(n.right)

    def test_put_larger_goes_right(self):
        n = BSTNode(5)
        n.put(8)
        self.assertEqual(n.right.key, 8)
        self.assertIsNone(n.left)

    def test_put_duplicate_of_root_is_ignored(self):
        n = BSTNode(5)
        n.put(5)
        self.assertIsNone(n.left)
        self.assertIsNone(n.right)

    def test_put_duplicate_deeper_is_ignored(self):
        n = build_node([5, 3, 8])
        n.put(3)
        n.put(8)
        self.assertEqual(list(n.in_order()), [3, 5, 8])
        self.assertIsNone(n.left.left)
        self.assertIsNone(n.left.right)
        self.assertIsNone(n.right.left)
        self.assertIsNone(n.right.right)

    def test_put_returns_none(self):
        self.assertIsNone(BSTNode(1).put(2))
        self.assertIsNone(BSTNode(1).put(1))

    def test_put_recurses_to_correct_depth(self):
        n = build_node(SAMPLE_KEYS)
        self.assertEqual(n.left.right.left.key, 4)
        self.assertEqual(n.left.right.right.key, 7)
        self.assertEqual(n.right.right.left.key, 13)
        self.assertIsNone(n.right.left)

    def test_put_does_not_replace_existing_child_nodes(self):
        n = BSTNode(5)
        n.put(3)
        original_left = n.left
        n.put(1)
        self.assertIs(n.left, original_left)
        self.assertEqual(n.left.left.key, 1)

    def test_put_negative_and_zero(self):
        n = build_node([0, -5, 5, -1])
        self.assertEqual(list(n.in_order()), [-5, -1, 0, 5])

    def test_put_floats(self):
        n = build_node([1.5, 0.5, 2.5, 1.0])
        self.assertEqual(list(n.in_order()), [0.5, 1.0, 1.5, 2.5])

    def test_put_strings(self):
        n = build_node(["m", "c", "x", "a", "z"])
        self.assertEqual(list(n.in_order()), ["a", "c", "m", "x", "z"])

    def test_put_tuples(self):
        n = build_node([(2, 1), (1, 9), (2, 0), (3, 3)])
        self.assertEqual(list(n.in_order()), [(1, 9), (2, 0), (2, 1), (3, 3)])

    def test_equal_but_different_types_are_duplicates(self):
        # 1 == 1.0 == True, so they should be treated as the same key.
        n = BSTNode(1)
        n.put(1.0)
        n.put(True)
        self.assertEqual(list(n.in_order()), [1])

    def test_put_very_large_ints(self):
        n = build_node([10**30, -(10**30), 0])
        self.assertEqual(list(n.in_order()), [-(10**30), 0, 10**30])

    def test_put_infinity(self):
        n = build_node([0, float("inf"), float("-inf")])
        self.assertEqual(list(n.in_order()), [float("-inf"), 0, float("inf")])

    # ---- invalid / unusual inputs ----
    def test_put_incomparable_type_raises_type_error(self):
        n = BSTNode(5)
        with self.assertRaises(TypeError):
            n.put("five")

    def test_put_none_into_int_tree_raises_type_error(self):
        n = BSTNode(5)
        with self.assertRaises(TypeError):
            n.put(None)

    def test_failed_put_does_not_corrupt_tree(self):
        n = build_node([5, 3, 8])
        with self.assertRaises(TypeError):
            n.put("x")
        self.assertEqual(list(n.in_order()), [3, 5, 8])

    def test_put_nan_is_silently_dropped(self):
        # NaN != NaN and NaN is neither < nor > anything, so put() falls through
        # every branch. Documents the silent no-op (potential bug: no error raised).
        n = build_node([5, 3, 8])
        n.put(float("nan"))
        self.assertEqual(list(n.in_order()), [3, 5, 8])


class TestBSTNodeTraversals(unittest.TestCase):
    def setUp(self):
        self.tree = build_node(SAMPLE_KEYS)

    def test_in_order_sample(self):
        self.assertEqual(list(self.tree.in_order()), SAMPLE_IN_ORDER)

    def test_pre_order_sample(self):
        self.assertEqual(list(self.tree.pre_order()), SAMPLE_PRE_ORDER)

    def test_post_order_sample(self):
        self.assertEqual(list(self.tree.post_order()), SAMPLE_POST_ORDER)

    def test_single_node_all_traversals(self):
        n = BSTNode(42)
        self.assertEqual(list(n.in_order()), [42])
        self.assertEqual(list(n.pre_order()), [42])
        self.assertEqual(list(n.post_order()), [42])

    def test_left_only_chain(self):
        n = build_node([5, 4, 3, 2, 1])
        self.assertEqual(list(n.in_order()), [1, 2, 3, 4, 5])
        self.assertEqual(list(n.pre_order()), [5, 4, 3, 2, 1])
        self.assertEqual(list(n.post_order()), [1, 2, 3, 4, 5])

    def test_right_only_chain(self):
        n = build_node([1, 2, 3, 4, 5])
        self.assertEqual(list(n.in_order()), [1, 2, 3, 4, 5])
        self.assertEqual(list(n.pre_order()), [1, 2, 3, 4, 5])
        self.assertEqual(list(n.post_order()), [5, 4, 3, 2, 1])

    def test_zigzag_chain(self):
        n = build_node([10, 2, 8, 4, 6, 5])
        self.assertEqual(list(n.in_order()), [2, 4, 5, 6, 8, 10])
        self.assertEqual(list(n.pre_order()), [10, 2, 8, 4, 6, 5])
        self.assertEqual(list(n.post_order()), [5, 6, 4, 8, 2, 10])

    def test_traversals_are_generators(self):
        for gen in (self.tree.in_order(), self.tree.pre_order(), self.tree.post_order()):
            self.assertTrue(hasattr(gen, "__next__"))
            self.assertIs(iter(gen), gen)

    def test_generators_are_lazy_and_yield_first_item_correctly(self):
        self.assertEqual(next(self.tree.in_order()), 1)
        self.assertEqual(next(self.tree.pre_order()), 8)
        self.assertEqual(next(self.tree.post_order()), 1)

    def test_generator_exhaustion_raises_stop_iteration(self):
        gen = BSTNode(1).in_order()
        next(gen)
        with self.assertRaises(StopIteration):
            next(gen)

    def test_generators_are_independent(self):
        g1, g2 = self.tree.in_order(), self.tree.in_order()
        self.assertEqual(next(g1), 1)
        self.assertEqual(next(g1), 3)
        self.assertEqual(next(g2), 1)

    def test_traversals_do_not_mutate_tree(self):
        list(self.tree.in_order())
        list(self.tree.pre_order())
        list(self.tree.post_order())
        self.assertEqual(list(self.tree.in_order()), SAMPLE_IN_ORDER)

    def test_traversal_lengths_match(self):
        n = len(SAMPLE_KEYS)
        self.assertEqual(len(list(self.tree.in_order())), n)
        self.assertEqual(len(list(self.tree.pre_order())), n)
        self.assertEqual(len(list(self.tree.post_order())), n)

    def test_pre_and_post_order_start_end_with_root(self):
        self.assertEqual(list(self.tree.pre_order())[0], self.tree.key)
        self.assertEqual(list(self.tree.post_order())[-1], self.tree.key)

    def test_string_keys_traversal(self):
        n = build_node(["m", "c", "x"])
        self.assertEqual(list(n.in_order()), ["c", "m", "x"])
        self.assertEqual(list(n.pre_order()), ["m", "c", "x"])
        self.assertEqual(list(n.post_order()), ["c", "x", "m"])


class TestBSTNodeClassicIteration(unittest.TestCase):
    def test_iter_returns_iterator_object(self):
        self.assertIsInstance(iter(BSTNode(1)), BSTNode_Iterator)

    def test_for_loop_matches_in_order(self):
        tree = build_node(SAMPLE_KEYS)
        self.assertEqual([k for k in tree], SAMPLE_IN_ORDER)

    def test_list_matches_in_order(self):
        tree = build_node(SAMPLE_KEYS)
        self.assertEqual(list(tree), list(tree.in_order()))

    def test_single_node(self):
        self.assertEqual(list(BSTNode(7)), [7])

    def test_can_iterate_multiple_times(self):
        tree = build_node(SAMPLE_KEYS)
        self.assertEqual(list(tree), SAMPLE_IN_ORDER)
        self.assertEqual(list(tree), SAMPLE_IN_ORDER)

    def test_iteration_sees_later_insertions(self):
        tree = build_node([2, 1])
        self.assertEqual(list(tree), [1, 2])
        tree.put(3)
        self.assertEqual(list(tree), [1, 2, 3])

    def test_sorted_and_builtins(self):
        tree = build_node(SAMPLE_KEYS)
        self.assertEqual(sorted(tree), SAMPLE_IN_ORDER)
        self.assertEqual(min(tree), 1)
        self.assertEqual(max(tree), 14)
        self.assertEqual(sum(tree), sum(SAMPLE_KEYS))

    def test_iterators_are_independent(self):
        tree = build_node(SAMPLE_KEYS)
        a, b = iter(tree), iter(tree)
        self.assertEqual(next(a), 1)
        self.assertEqual(next(a), 3)
        self.assertEqual(next(b), 1)

    def test_next_after_exhaustion_keeps_raising_stop_iteration(self):
        it = iter(BSTNode(1))
        self.assertEqual(next(it), 1)
        for _ in range(3):
            with self.assertRaises(StopIteration):
                next(it)

    def test_iterator_snapshot_does_not_see_inserts_after_creation(self):
        # The iterator queues the whole tree at construction time.
        tree = build_node([2, 1, 3])
        it = iter(tree)
        tree.put(4)
        self.assertEqual(list(it), [1, 2, 3])

    def test_iterator_direct_construction(self):
        it = BSTNode_Iterator(build_node([2, 1, 3]))
        self.assertEqual(next(it), 1)
        self.assertEqual(next(it), 2)
        self.assertEqual(next(it), 3)
        with self.assertRaises(StopIteration):
            next(it)

    def test_iterator_rejects_none_node(self):
        with self.assertRaises(AttributeError):
            BSTNode_Iterator(None)

    def test_iterator_returns_keys_not_nodes(self):
        it = iter(build_node([2, 1, 3]))
        self.assertNotIsInstance(next(it), BSTNode)

    def test_iterator_protocol_iter_returns_self(self):
        # BUG: BSTNode_Iterator defines __next__ but not __iter__, so it does not
        # fully implement the iterator protocol. iter(iterator) raises TypeError,
        # which breaks e.g. `for x in iter(tree)`, itertools helpers, etc.
        it = iter(build_node([2, 1, 3]))
        self.assertIs(iter(it), it)

    def test_for_loop_over_iter_of_tree(self):
        # BUG: same root cause as above.
        tree = build_node([2, 1, 3])
        self.assertEqual([k for k in iter(tree)], [1, 2, 3])


class TestBSTSetEmpty(unittest.TestCase):
    def setUp(self):
        self.s = BSTSet()

    def test_new_set_has_no_head(self):
        self.assertIsNone(self.s._head)

    def test_pre_order_empty_yields_nothing(self):
        self.assertEqual(list(self.s.pre_order()), [])

    def test_post_order_empty_yields_nothing(self):
        self.assertEqual(list(self.s.post_order()), [])

    def test_in_order_empty_yields_nothing(self):
        # BUG: BSTSet.in_order has no empty-check (unlike pre_order/post_order),
        # so it raises AttributeError: 'NoneType' has no attribute 'in_order'.
        self.assertEqual(list(self.s.in_order()), [])

    def test_iter_empty_yields_nothing(self):
        # BUG: BSTSet.__iter__ calls iter(None) on an empty set -> TypeError.
        self.assertEqual(list(self.s), [])

    def test_for_loop_over_empty_set(self):
        # BUG: same root cause as above.
        seen = [k for k in self.s]
        self.assertEqual(seen, [])


class TestBSTSetPut(unittest.TestCase):
    def test_first_put_creates_head(self):
        s = BSTSet()
        s.put(5)
        self.assertIsInstance(s._head, BSTNode)
        self.assertEqual(s._head.key, 5)

    def test_second_put_does_not_replace_head(self):
        s = BSTSet()
        s.put(5)
        head = s._head
        s.put(3)
        s.put(9)
        self.assertIs(s._head, head)

    def test_put_returns_none(self):
        s = BSTSet()
        self.assertIsNone(s.put(1))
        self.assertIsNone(s.put(1))

    def test_duplicates_not_stored(self):
        s = build_set([4, 4, 4, 2, 2, 6, 6])
        self.assertEqual(list(s.in_order()), [2, 4, 6])

    def test_single_element(self):
        s = build_set([1])
        self.assertEqual(list(s.in_order()), [1])
        self.assertEqual(list(s.pre_order()), [1])
        self.assertEqual(list(s.post_order()), [1])
        self.assertEqual(list(s), [1])

    def test_insertion_order_does_not_change_in_order_result(self):
        a = build_set([1, 2, 3, 4, 5])
        b = build_set([5, 4, 3, 2, 1])
        c = build_set([3, 1, 5, 2, 4])
        self.assertEqual(list(a.in_order()), [1, 2, 3, 4, 5])
        self.assertEqual(list(b.in_order()), [1, 2, 3, 4, 5])
        self.assertEqual(list(c.in_order()), [1, 2, 3, 4, 5])

    def test_insertion_order_changes_pre_and_post_order(self):
        a = build_set([1, 2, 3])
        b = build_set([3, 2, 1])
        self.assertEqual(list(a.pre_order()), [1, 2, 3])
        self.assertEqual(list(b.pre_order()), [3, 2, 1])
        self.assertEqual(list(a.post_order()), [3, 2, 1])
        self.assertEqual(list(b.post_order()), [1, 2, 3])

    def test_none_as_first_key_then_comparable_key_raises(self):
        s = BSTSet()
        s.put(None)
        with self.assertRaises(TypeError):
            s.put(1)

    def test_mixed_types_raise(self):
        s = build_set([1, 2])
        with self.assertRaises(TypeError):
            s.put("a")
        self.assertEqual(list(s.in_order()), [1, 2])

    def test_falsy_keys_are_not_confused_with_missing(self):
        s = BSTSet()
        s.put(0)
        s.put(0)
        s.put(-1)
        self.assertEqual(list(s.in_order()), [-1, 0])

    def test_empty_string_key(self):
        s = build_set(["b", "", "a"])
        self.assertEqual(list(s.in_order()), ["", "a", "b"])

    def test_sets_are_independent(self):
        a, b = BSTSet(), BSTSet()
        a.put(1)
        self.assertEqual(list(b.pre_order()), [])
        self.assertIsNone(b._head)


class TestBSTSetTraversals(unittest.TestCase):
    def setUp(self):
        self.s = build_set(SAMPLE_KEYS)

    def test_in_order(self):
        self.assertEqual(list(self.s.in_order()), SAMPLE_IN_ORDER)

    def test_pre_order(self):
        self.assertEqual(list(self.s.pre_order()), SAMPLE_PRE_ORDER)

    def test_post_order(self):
        self.assertEqual(list(self.s.post_order()), SAMPLE_POST_ORDER)

    def test_classic_iteration_matches_in_order(self):
        self.assertEqual(list(self.s), SAMPLE_IN_ORDER)

    def test_traversals_are_generators(self):
        for gen in (self.s.in_order(), self.s.pre_order(), self.s.post_order()):
            self.assertTrue(hasattr(gen, "__next__"))

    def test_empty_set_pre_post_return_generators(self):
        e = BSTSet()
        self.assertTrue(hasattr(e.pre_order(), "__next__"))
        self.assertTrue(hasattr(e.post_order(), "__next__"))

    def test_repeatable_traversal(self):
        self.assertEqual(list(self.s.in_order()), list(self.s.in_order()))
        self.assertEqual(list(self.s.pre_order()), list(self.s.pre_order()))

    def test_traversal_reflects_later_insertions(self):
        self.s.put(0)
        self.s.put(100)
        self.assertEqual(list(self.s.in_order()), [0] + SAMPLE_IN_ORDER + [100])

    def test_in_order_is_sorted_and_unique(self):
        items = list(self.s.in_order())
        self.assertEqual(items, sorted(set(items)))

    def test_pre_order_and_post_order_are_permutations_of_in_order(self):
        self.assertEqual(sorted(self.s.pre_order()), SAMPLE_IN_ORDER)
        self.assertEqual(sorted(self.s.post_order()), SAMPLE_IN_ORDER)

    def test_lazy_in_order_on_set(self):
        gen = self.s.in_order()
        self.assertEqual(next(gen), 1)
        self.assertEqual(next(gen), 3)


class TestBSTSetRandomized(unittest.TestCase):
    def test_random_inserts_match_sorted_set(self):
        rng = random.Random(12345)
        for _ in range(50):
            keys = [rng.randint(-50, 50) for _ in range(rng.randint(1, 80))]
            s = build_set(keys)
            expected = sorted(set(keys))
            self.assertEqual(list(s.in_order()), expected)
            self.assertEqual(list(s), expected)
            self.assertEqual(sorted(s.pre_order()), expected)
            self.assertEqual(sorted(s.post_order()), expected)
            # root is first in pre-order, last in post-order
            self.assertEqual(next(s.pre_order()), keys[0])
            self.assertEqual(list(s.post_order())[-1], keys[0])

    def test_shuffled_unique_keys(self):
        rng = random.Random(7)
        keys = list(range(200))
        rng.shuffle(keys)
        s = build_set(keys)
        self.assertEqual(list(s.in_order()), list(range(200)))

    def test_all_identical_keys(self):
        s = build_set([7] * 100)
        self.assertEqual(list(s.in_order()), [7])
        self.assertIsNone(s._head.left)
        self.assertIsNone(s._head.right)


class TestBSTDepthLimits(unittest.TestCase):
    def test_moderately_deep_degenerate_tree_works(self):
        keys = list(range(300))  # sorted inserts -> linked-list-shaped tree
        s = build_set(keys)
        self.assertEqual(list(s.in_order()), keys)
        self.assertEqual(list(s), keys)
        self.assertEqual(list(s.pre_order()), keys)
        self.assertEqual(list(s.post_order()), keys[::-1])

    @unittest.expectedFailure
    def test_very_deep_degenerate_tree(self):
        # BUG / limitation: put(), the traversals, and BSTNode_Iterator.in_order are
        # all recursive, so a sorted insertion of more keys than the recursion limit
        # raises RecursionError. This test expects success, so it is marked as an
        # expected failure; remove the decorator once the code is made iterative.
        n = sys.getrecursionlimit() + 500
        s = build_set(range(n))
        self.assertEqual(len(list(s.in_order())), n)


if __name__ == "__main__":
    unittest.main()