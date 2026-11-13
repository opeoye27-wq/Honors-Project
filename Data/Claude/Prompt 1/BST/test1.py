import random
import sys
import unittest

# Import the actual implementation.
from BST import BSTNode, BSTNode_Iterator, BSTSet


def build_set(keys):
    s = BSTSet()
    for k in keys:
        s.put(k)
    return s


def build_node(keys):
    node = BSTNode(keys[0])
    for k in keys[1:]:
        node.put(k)
    return node


#          8
#        /   \
#       3     10
#      / \      \
#     1   6      14
#        / \     /
#       4   7   13
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
        l, r = BSTNode(1), BSTNode(9)
        n = BSTNode(5, l, r)
        self.assertIs(n.left, l)
        self.assertIs(n.right, r)

    def test_repr(self):
        self.assertEqual(repr(BSTNode(5)), "BSTNode(key=5)")
        self.assertEqual(repr(BSTNode("a")), "BSTNode(key=a)")
        self.assertEqual(repr(BSTNode(None)), "BSTNode(key=None)")

    def test_repr_used_by_str(self):
        self.assertEqual(str(BSTNode(7)), "BSTNode(key=7)")

    def test_children_independent_between_instances(self):
        a, b = BSTNode(1), BSTNode(2)
        a.put(0)
        self.assertIsNone(b.left)


class TestBSTNodePut(unittest.TestCase):
    def test_put_smaller_goes_left(self):
        n = BSTNode(5)
        n.put(3)
        self.assertEqual(n.left.key, 3)
        self.assertIsNone(n.right)

    def test_put_larger_goes_right(self):
        n = BSTNode(5)
        n.put(8)
        self.assertEqual(n.right.key, 8)
        self.assertIsNone(n.left)

    def test_put_duplicate_root_ignored(self):
        n = BSTNode(5)
        n.put(5)
        self.assertIsNone(n.left)
        self.assertIsNone(n.right)

    def test_put_duplicate_deep_ignored(self):
        n = build_node(SAMPLE_KEYS)
        n.put(7)
        n.put(1)
        self.assertEqual(list(n.in_order()), SAMPLE_IN_ORDER)

    def test_put_recurses_to_correct_depth(self):
        n = BSTNode(10)
        for k in (5, 2, 1):
            n.put(k)
        self.assertEqual(n.left.left.left.key, 1)

    def test_structure_matches_expected_tree(self):
        n = build_node(SAMPLE_KEYS)
        self.assertEqual(n.left.key, 3)
        self.assertEqual(n.right.key, 10)
        self.assertEqual(n.left.left.key, 1)
        self.assertEqual(n.left.right.key, 6)
        self.assertEqual(n.left.right.left.key, 4)
        self.assertEqual(n.left.right.right.key, 7)
        self.assertIsNone(n.right.left)
        self.assertEqual(n.right.right.key, 14)
        self.assertEqual(n.right.right.left.key, 13)

    def test_put_negative_and_zero(self):
        n = build_node([0, -5, 5, -1])
        self.assertEqual(list(n.in_order()), [-5, -1, 0, 5])

    def test_put_floats_and_mixed_int_float(self):
        n = build_node([1.5, 1, 2, 1.25])
        self.assertEqual(list(n.in_order()), [1, 1.25, 1.5, 2])

    def test_int_and_equal_float_treated_as_duplicate(self):
        n = BSTNode(1)
        n.put(1.0)
        self.assertIsNone(n.left)
        self.assertIsNone(n.right)

    def test_bool_equal_to_int_treated_as_duplicate(self):
        n = BSTNode(1)
        n.put(True)
        self.assertIsNone(n.left)
        self.assertIsNone(n.right)

    def test_string_keys(self):
        n = build_node(["m", "c", "x", "a", "z"])
        self.assertEqual(list(n.in_order()), ["a", "c", "m", "x", "z"])

    def test_string_keys_case_and_empty_string(self):
        n = build_node(["b", "", "B", "a"])
        self.assertEqual(list(n.in_order()), ["", "B", "a", "b"])

    def test_tuple_keys(self):
        n = build_node([(2, 1), (1, 9), (2, 0), (3, 3)])
        self.assertEqual(list(n.in_order()), [(1, 9), (2, 0), (2, 1), (3, 3)])

    def test_large_integers(self):
        big = 10 ** 30
        n = build_node([0, big, -big])
        self.assertEqual(list(n.in_order()), [-big, 0, big])

    def test_float_infinity(self):
        n = build_node([0, float("inf"), float("-inf")])
        self.assertEqual(list(n.in_order()), [float("-inf"), 0, float("inf")])

    def test_nan_key_is_silently_dropped(self):
        # NaN is neither <, >, nor == anything, so put() falls through.
        n = BSTNode(5)
        n.put(float("nan"))
        self.assertIsNone(n.left)
        self.assertIsNone(n.right)

    def test_incomparable_types_raise_type_error(self):
        n = BSTNode(5)
        with self.assertRaises(TypeError):
            n.put("five")

    def test_none_key_on_non_empty_node_raises(self):
        n = BSTNode(5)
        with self.assertRaises(TypeError):
            n.put(None)

    def test_put_returns_none(self):
        self.assertIsNone(BSTNode(1).put(2))
        self.assertIsNone(BSTNode(1).put(1))

    def test_failed_put_does_not_corrupt_tree(self):
        n = build_node([5, 3, 8])
        with self.assertRaises(TypeError):
            n.put("x")
        self.assertEqual(list(n.in_order()), [3, 5, 8])


class TestBSTNodeTraversals(unittest.TestCase):
    def setUp(self):
        self.node = build_node(SAMPLE_KEYS)

    def test_in_order(self):
        self.assertEqual(list(self.node.in_order()), SAMPLE_IN_ORDER)

    def test_pre_order(self):
        self.assertEqual(list(self.node.pre_order()), SAMPLE_PRE_ORDER)

    def test_post_order(self):
        self.assertEqual(list(self.node.post_order()), SAMPLE_POST_ORDER)

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

    def test_only_left_child(self):
        n = build_node([2, 1])
        self.assertEqual(list(n.pre_order()), [2, 1])
        self.assertEqual(list(n.post_order()), [1, 2])

    def test_only_right_child(self):
        n = build_node([2, 3])
        self.assertEqual(list(n.pre_order()), [2, 3])
        self.assertEqual(list(n.post_order()), [3, 2])

    def test_traversals_return_generators(self):
        for gen in (self.node.in_order(), self.node.pre_order(), self.node.post_order()):
            self.assertTrue(hasattr(gen, "__next__"))
            self.assertIs(iter(gen), gen)

    def test_in_order_is_lazy_and_yields_smallest_first(self):
        gen = self.node.in_order()
        self.assertEqual(next(gen), 1)
        self.assertEqual(next(gen), 3)

    def test_generator_exhaustion_raises_stop_iteration(self):
        gen = BSTNode(1).in_order()
        next(gen)
        with self.assertRaises(StopIteration):
            next(gen)

    def test_traversals_are_repeatable(self):
        self.assertEqual(list(self.node.in_order()), list(self.node.in_order()))
        self.assertEqual(list(self.node.pre_order()), list(self.node.pre_order()))
        self.assertEqual(list(self.node.post_order()), list(self.node.post_order()))

    def test_traversals_have_same_elements(self):
        expected = sorted(SAMPLE_KEYS)
        self.assertEqual(sorted(self.node.pre_order()), expected)
        self.assertEqual(sorted(self.node.post_order()), expected)

    def test_traversals_do_not_mutate_tree(self):
        list(self.node.in_order())
        list(self.node.pre_order())
        list(self.node.post_order())
        self.assertEqual(list(self.node.pre_order()), SAMPLE_PRE_ORDER)

    def test_manually_constructed_tree(self):
        n = BSTNode(2, BSTNode(1), BSTNode(3))
        self.assertEqual(list(n.in_order()), [1, 2, 3])
        self.assertEqual(list(n.pre_order()), [2, 1, 3])
        self.assertEqual(list(n.post_order()), [1, 3, 2])

    def test_insertion_order_changes_shape_not_in_order(self):
        a = build_node([1, 2, 3])
        b = build_node([2, 1, 3])
        self.assertEqual(list(a.in_order()), list(b.in_order()))
        self.assertNotEqual(list(a.pre_order()), list(b.pre_order()))


class TestBSTNodeClassicIteration(unittest.TestCase):
    def setUp(self):
        self.node = build_node(SAMPLE_KEYS)

    def test_iter_returns_iterator_object(self):
        self.assertIsInstance(iter(self.node), BSTNode_Iterator)

    def test_for_loop_matches_in_order(self):
        self.assertEqual([k for k in self.node], SAMPLE_IN_ORDER)

    def test_list_matches_in_order(self):
        self.assertEqual(list(self.node), list(self.node.in_order()))

    def test_sorted_and_sum_work(self):
        self.assertEqual(sum(self.node), sum(SAMPLE_KEYS))
        self.assertEqual(min(self.node), 1)
        self.assertEqual(max(self.node), 14)

    def test_multiple_independent_iterators(self):
        it1, it2 = iter(self.node), iter(self.node)
        self.assertEqual(next(it1), 1)
        self.assertEqual(next(it1), 3)
        self.assertEqual(next(it2), 1)

    def test_iterate_twice_gives_same_result(self):
        self.assertEqual(list(self.node), list(self.node))

    def test_single_node_iteration(self):
        self.assertEqual(list(BSTNode(1)), [1])

    def test_next_yields_keys_not_nodes(self):
        self.assertEqual(next(iter(self.node)), 1)

    def test_exhausted_iterator_keeps_raising_stop_iteration(self):
        it = iter(BSTNode(1))
        self.assertEqual(next(it), 1)
        for _ in range(3):
            with self.assertRaises(StopIteration):
                next(it)

    def test_iterator_is_snapshot_of_tree(self):
        it = iter(self.node)
        self.node.put(100)
        self.assertNotIn(100, list(it))

    def test_iterator_constructor_rejects_none(self):
        with self.assertRaises(AttributeError):
            BSTNode_Iterator(None)

    @unittest.expectedFailure
    def test_iterator_is_itself_iterable(self):
        # BUG: BSTNode_Iterator defines __next__ but not __iter__, so it
        # violates the iterator protocol (iter(it) raises TypeError).
        it = iter(self.node)
        self.assertEqual(list(iter(it)), SAMPLE_IN_ORDER)


class TestBSTSetEmpty(unittest.TestCase):
    def test_new_set_has_no_head(self):
        self.assertIsNone(BSTSet()._head)

    def test_pre_order_empty(self):
        self.assertEqual(list(BSTSet().pre_order()), [])

    def test_post_order_empty(self):
        self.assertEqual(list(BSTSet().post_order()), [])

    @unittest.expectedFailure
    def test_in_order_empty_should_yield_nothing(self):
        # BUG: in_order() dereferences None and raises AttributeError.
        self.assertEqual(list(BSTSet().in_order()), [])

    @unittest.expectedFailure
    def test_iter_empty_should_yield_nothing(self):
        # BUG: iter(None) raises TypeError for an empty set.
        self.assertEqual(list(BSTSet()), [])

    def test_in_order_empty_currently_raises(self):
        with self.assertRaises(AttributeError):
            list(BSTSet().in_order())

    def test_iter_empty_currently_raises(self):
        with self.assertRaises(TypeError):
            iter(BSTSet())


class TestBSTSetPut(unittest.TestCase):
    def test_first_put_creates_head(self):
        s = BSTSet()
        s.put(5)
        self.assertIsInstance(s._head, BSTNode)
        self.assertEqual(s._head.key, 5)

    def test_head_unchanged_by_later_puts(self):
        s = build_set([5, 1, 9])
        self.assertEqual(s._head.key, 5)

    def test_duplicate_head_ignored(self):
        s = build_set([5, 5, 5])
        self.assertEqual(list(s.in_order()), [5])

    def test_duplicates_ignored(self):
        s = build_set([3, 1, 2, 3, 1, 2, 3])
        self.assertEqual(list(s.in_order()), [1, 2, 3])

    def test_put_returns_none(self):
        s = BSTSet()
        self.assertIsNone(s.put(1))
        self.assertIsNone(s.put(1))

    def test_none_as_first_key_then_second_key_raises(self):
        s = BSTSet()
        s.put(None)
        with self.assertRaises(TypeError):
            s.put(1)

    def test_mixed_types_raise(self):
        s = build_set([1, 2])
        with self.assertRaises(TypeError):
            s.put("a")

    def test_sets_are_independent(self):
        a, b = BSTSet(), BSTSet()
        a.put(1)
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

    def test_classic_iteration(self):
        self.assertEqual(list(self.s), SAMPLE_IN_ORDER)
        self.assertEqual([k for k in self.s], SAMPLE_IN_ORDER)

    def test_single_element(self):
        s = build_set([1])
        self.assertEqual(list(s.in_order()), [1])
        self.assertEqual(list(s.pre_order()), [1])
        self.assertEqual(list(s.post_order()), [1])
        self.assertEqual(list(s), [1])

    def test_traversals_are_repeatable(self):
        self.assertEqual(list(self.s.pre_order()), list(self.s.pre_order()))
        self.assertEqual(list(self.s), list(self.s))

    def test_traversal_reflects_later_insertions(self):
        self.s.put(0)
        self.s.put(99)
        self.assertEqual(list(self.s.in_order()), [0] + SAMPLE_IN_ORDER + [99])
        self.assertEqual(list(self.s.pre_order())[0], 8)
        self.assertEqual(list(self.s.post_order())[-1], 8)

    def test_pre_and_post_order_are_generators(self):
        self.assertTrue(hasattr(self.s.pre_order(), "__next__"))
        self.assertTrue(hasattr(self.s.post_order(), "__next__"))

    def test_string_set(self):
        s = build_set(["pear", "apple", "fig", "apple"])
        self.assertEqual(list(s.in_order()), ["apple", "fig", "pear"])

    def test_negative_numbers(self):
        s = build_set([-3, -1, -2, 0, 2])
        self.assertEqual(list(s.in_order()), [-3, -2, -1, 0, 2])

    def test_next_on_traversal_generators(self):
        self.assertEqual(next(self.s.in_order()), 1)
        self.assertEqual(next(self.s.pre_order()), 8)
        self.assertEqual(next(self.s.post_order()), 1)


class TestBSTSetPropertyStyle(unittest.TestCase):
    def test_random_inputs_match_sorted_set(self):
        rng = random.Random(1234)
        for _ in range(50):
            keys = [rng.randint(-50, 50) for _ in range(rng.randint(1, 60))]
            s = build_set(keys)
            expected = sorted(set(keys))
            self.assertEqual(list(s.in_order()), expected)
            self.assertEqual(list(s), expected)
            self.assertEqual(sorted(s.pre_order()), expected)
            self.assertEqual(sorted(s.post_order()), expected)
            self.assertEqual(next(s.pre_order()), keys[0])
            self.assertEqual(list(s.post_order())[-1], keys[0])

    def test_all_insertion_permutations_of_small_set(self):
        from itertools import permutations
        for perm in permutations([1, 2, 3, 4]):
            s = build_set(perm)
            self.assertEqual(list(s.in_order()), [1, 2, 3, 4])
            self.assertEqual(next(s.pre_order()), perm[0])

    def test_moderately_large_balanced_input(self):
        keys = list(range(200))
        random.Random(7).shuffle(keys)
        s = build_set(keys)
        self.assertEqual(list(s.in_order()), list(range(200)))


class TestBSTSetDeepTrees(unittest.TestCase):
    def test_deep_chain_below_recursion_limit(self):
        n = 300
        s = build_set(range(n))
        self.assertEqual(list(s.in_order()), list(range(n)))
        self.assertEqual(list(s.pre_order()), list(range(n)))
        self.assertEqual(list(s.post_order()), list(range(n - 1, -1, -1)))

    @unittest.expectedFailure
    def test_degenerate_tree_beyond_recursion_limit(self):
        # BUG/limitation: put() and the traversals are recursive, so
        # inserting sorted keys deeper than the interpreter's recursion
        # limit raises RecursionError.
        n = sys.getrecursionlimit() * 3
        s = build_set(range(n))
        self.assertEqual(len(list(s.in_order())), n)


if __name__ == "__main__":
    unittest.main()