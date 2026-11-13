import unittest

# Change this import to match the module name that contains the program.
from BST import BSTNode, BSTSet, BSTNode_Iterator


STANDARD_KEYS = [8, 3, 10, 1, 6, 14, 4, 7, 13]
STANDARD_IN_ORDER = [1, 3, 4, 6, 7, 8, 10, 13, 14]
STANDARD_PRE_ORDER = [8, 3, 1, 6, 4, 7, 10, 14, 13]
STANDARD_POST_ORDER = [1, 4, 7, 6, 3, 13, 14, 10, 8]


def build_node(keys):
    node = BSTNode(keys[0])
    for k in keys[1:]:
        node.put(k)
    return node


def build_set(keys):
    s = BSTSet()
    for k in keys:
        s.put(k)
    return s


# ---------------------------------------------------------------------------
# BSTNode: construction and repr
# ---------------------------------------------------------------------------
class TestBSTNodeConstruction(unittest.TestCase):
    def test_defaults_children_none(self):
        n = BSTNode(5)
        self.assertEqual(n.key, 5)
        self.assertIsNone(n.left)
        self.assertIsNone(n.right)

    def test_children_can_be_supplied(self):
        l, r = BSTNode(1), BSTNode(9)
        n = BSTNode(5, l, r)
        self.assertIs(n.left, l)
        self.assertIs(n.right, r)

    def test_repr_int(self):
        self.assertEqual(repr(BSTNode(5)), "BSTNode(key=5)")

    def test_repr_string_key(self):
        self.assertEqual(repr(BSTNode("a")), "BSTNode(key=a)")

    def test_repr_negative_and_float(self):
        self.assertEqual(repr(BSTNode(-3)), "BSTNode(key=-3)")
        self.assertEqual(repr(BSTNode(2.5)), "BSTNode(key=2.5)")


# ---------------------------------------------------------------------------
# BSTNode.put
# ---------------------------------------------------------------------------
class TestBSTNodePut(unittest.TestCase):
    def test_smaller_goes_left(self):
        n = BSTNode(5)
        n.put(2)
        self.assertEqual(n.left.key, 2)
        self.assertIsNone(n.right)

    def test_bigger_goes_right(self):
        n = BSTNode(5)
        n.put(8)
        self.assertEqual(n.right.key, 8)
        self.assertIsNone(n.left)

    def test_duplicate_of_root_ignored(self):
        n = BSTNode(5)
        n.put(5)
        self.assertIsNone(n.left)
        self.assertIsNone(n.right)

    def test_duplicate_deep_ignored(self):
        n = build_node(STANDARD_KEYS)
        n.put(7)
        n.put(13)
        n.put(1)
        self.assertEqual(list(n.in_order()), STANDARD_IN_ORDER)

    def test_deeper_structure(self):
        n = build_node(STANDARD_KEYS)
        self.assertEqual(n.left.key, 3)
        self.assertEqual(n.right.key, 10)
        self.assertEqual(n.left.left.key, 1)
        self.assertEqual(n.left.right.key, 6)
        self.assertEqual(n.left.right.left.key, 4)
        self.assertEqual(n.left.right.right.key, 7)
        self.assertEqual(n.right.right.key, 14)
        self.assertEqual(n.right.right.left.key, 13)
        self.assertIsNone(n.right.left)

    def test_existing_child_not_replaced(self):
        n = BSTNode(5)
        n.put(2)
        original_left = n.left
        n.put(1)
        n.put(3)
        self.assertIs(n.left, original_left)

    def test_negative_and_zero_keys(self):
        n = build_node([0, -5, 5, -10, 10])
        self.assertEqual(list(n.in_order()), [-10, -5, 0, 5, 10])

    def test_float_keys(self):
        n = build_node([1.5, 0.5, 2.5])
        self.assertEqual(list(n.in_order()), [0.5, 1.5, 2.5])

    def test_mixed_int_float_equal_values_deduplicated(self):
        n = BSTNode(1)
        n.put(1.0)
        self.assertEqual(list(n.in_order()), [1])

    def test_bool_equals_int_deduplicated(self):
        n = BSTNode(1)
        n.put(True)
        self.assertEqual(list(n.in_order()), [1])

    def test_string_keys(self):
        n = build_node(["m", "c", "x", "a"])
        self.assertEqual(list(n.in_order()), ["a", "c", "m", "x"])

    def test_empty_string_key(self):
        n = build_node(["b", ""])
        self.assertEqual(list(n.in_order()), ["", "b"])

    def test_tuple_keys(self):
        n = build_node([(2, 1), (1, 5), (2, 0)])
        self.assertEqual(list(n.in_order()), [(1, 5), (2, 0), (2, 1)])

    def test_incomparable_types_raise_type_error(self):
        n = BSTNode(5)
        with self.assertRaises(TypeError):
            n.put("a")

    def test_none_key_against_int_raises_type_error(self):
        n = BSTNode(5)
        with self.assertRaises(TypeError):
            n.put(None)

    def test_nan_is_not_silently_dropped(self):
        # POTENTIAL BUG: nan == x, nan < x and nan > x are all False, so put()
        # falls through every branch and silently discards the key.
        n = BSTNode(5)
        n.put(float("nan"))
        self.assertEqual(len(list(n.in_order())), 2)

    def test_nan_root_does_not_swallow_all_inserts(self):
        # POTENTIAL BUG: with a nan root, every comparison is False,
        # so every later insert is silently dropped.
        n = BSTNode(float("nan"))
        n.put(1)
        n.put(2)
        self.assertEqual(len(list(n.in_order())), 3)

    def test_sorted_insertion_deep_tree(self):
        # POTENTIAL BUG: put() is recursive, so a degenerate (sorted-input)
        # tree deeper than the recursion limit raises RecursionError.
        n = BSTNode(0)
        for k in range(1, 1500):
            n.put(k)
        self.assertEqual(list(n.in_order()), list(range(1500)))


# ---------------------------------------------------------------------------
# BSTNode traversals
# ---------------------------------------------------------------------------
class TestBSTNodeTraversals(unittest.TestCase):
    def setUp(self):
        self.tree = build_node(STANDARD_KEYS)

    def test_in_order_sorted(self):
        self.assertEqual(list(self.tree.in_order()), STANDARD_IN_ORDER)

    def test_pre_order(self):
        self.assertEqual(list(self.tree.pre_order()), STANDARD_PRE_ORDER)

    def test_post_order(self):
        self.assertEqual(list(self.tree.post_order()), STANDARD_POST_ORDER)

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

    def test_two_nodes_left(self):
        n = build_node([2, 1])
        self.assertEqual(list(n.pre_order()), [2, 1])
        self.assertEqual(list(n.post_order()), [1, 2])

    def test_two_nodes_right(self):
        n = build_node([1, 2])
        self.assertEqual(list(n.pre_order()), [1, 2])
        self.assertEqual(list(n.post_order()), [2, 1])

    def test_traversals_are_generators(self):
        for gen in (self.tree.in_order(), self.tree.pre_order(), self.tree.post_order()):
            self.assertTrue(hasattr(gen, "__next__"))

    def test_generator_is_lazy(self):
        g = self.tree.in_order()
        self.assertEqual(next(g), 1)
        self.assertEqual(next(g), 3)

    def test_generator_exhaustion(self):
        g = BSTNode(1).in_order()
        next(g)
        with self.assertRaises(StopIteration):
            next(g)

    def test_traversals_repeatable(self):
        self.assertEqual(list(self.tree.in_order()), list(self.tree.in_order()))
        self.assertEqual(list(self.tree.pre_order()), list(self.tree.pre_order()))
        self.assertEqual(list(self.tree.post_order()), list(self.tree.post_order()))

    def test_traversals_contain_same_elements(self):
        expected = sorted(STANDARD_KEYS)
        self.assertEqual(sorted(self.tree.pre_order()), expected)
        self.assertEqual(sorted(self.tree.post_order()), expected)

    def test_insertion_order_independence_for_in_order(self):
        a = build_node([5, 3, 8, 1, 4])
        b = build_node([1, 3, 4, 5, 8])
        self.assertEqual(list(a.in_order()), list(b.in_order()))
        self.assertNotEqual(list(a.pre_order()), list(b.pre_order()))

    def test_in_order_deep_tree_within_recursion_limit(self):
        n = BSTNode(0)
        for k in range(1, 300):
            n.put(k)
        self.assertEqual(list(n.in_order()), list(range(300)))
        self.assertEqual(list(n.pre_order()), list(range(300)))
        self.assertEqual(list(n.post_order()), list(range(299, -1, -1)))


# ---------------------------------------------------------------------------
# BSTNode.__iter__ and BSTNode_Iterator
# ---------------------------------------------------------------------------
class TestBSTNodeIterator(unittest.TestCase):
    def setUp(self):
        self.tree = build_node(STANDARD_KEYS)

    def test_iter_returns_iterator_object(self):
        self.assertIsInstance(iter(self.tree), BSTNode_Iterator)

    def test_for_loop_in_order(self):
        self.assertEqual([k for k in self.tree], STANDARD_IN_ORDER)

    def test_list_conversion(self):
        self.assertEqual(list(self.tree), STANDARD_IN_ORDER)

    def test_matches_generator_in_order(self):
        self.assertEqual(list(self.tree), list(self.tree.in_order()))

    def test_can_iterate_multiple_times(self):
        self.assertEqual(list(self.tree), list(self.tree))

    def test_single_node(self):
        self.assertEqual(list(BSTNode(7)), [7])

    def test_next_manual_then_stop_iteration(self):
        it = iter(BSTNode(7))
        self.assertEqual(next(it), 7)
        with self.assertRaises(StopIteration):
            next(it)

    def test_stop_iteration_is_repeatable(self):
        it = iter(BSTNode(7))
        next(it)
        for _ in range(3):
            with self.assertRaises(StopIteration):
                next(it)

    def test_iterator_returns_keys_not_nodes(self):
        for item in self.tree:
            self.assertNotIsInstance(item, BSTNode)

    def test_iterator_is_snapshot_of_tree_at_creation(self):
        it = iter(self.tree)
        self.tree.put(100)
        self.assertEqual(list(it), STANDARD_IN_ORDER)

    def test_iterator_counter_starts_at_zero(self):
        it = BSTNode_Iterator(self.tree)
        self.assertEqual(it.counter, 0)
        self.assertEqual(len(it.queue), len(STANDARD_KEYS))

    def test_iterator_is_itself_iterable(self):
        # POTENTIAL BUG: BSTNode_Iterator defines __next__ but not __iter__,
        # so it violates the iterator protocol (iter(iter(x)) raises TypeError).
        it = iter(self.tree)
        self.assertEqual(list(iter(it)), STANDARD_IN_ORDER)

    def test_iterator_usable_in_itertools(self):
        # Same protocol issue: many stdlib helpers call iter() on their input.
        import itertools
        it = iter(self.tree)
        self.assertEqual(list(itertools.islice(it, 3)), [1, 3, 4])


# ---------------------------------------------------------------------------
# BSTSet
# ---------------------------------------------------------------------------
class TestBSTSetBasics(unittest.TestCase):
    def test_new_set_has_no_head(self):
        self.assertIsNone(BSTSet()._head)

    def test_first_put_creates_head(self):
        s = BSTSet()
        s.put(5)
        self.assertIsNotNone(s._head)
        self.assertEqual(s._head.key, 5)

    def test_put_after_head_delegates_to_node(self):
        s = BSTSet()
        s.put(5)
        s.put(3)
        s.put(8)
        self.assertEqual(s._head.left.key, 3)
        self.assertEqual(s._head.right.key, 8)

    def test_duplicate_put_ignored(self):
        s = build_set([5, 5, 5])
        self.assertEqual(list(s.in_order()), [5])

    def test_duplicates_in_larger_set(self):
        s = build_set(STANDARD_KEYS + STANDARD_KEYS)
        self.assertEqual(list(s.in_order()), STANDARD_IN_ORDER)

    def test_head_never_changes_after_first_put(self):
        s = build_set(STANDARD_KEYS)
        self.assertEqual(s._head.key, 8)

    def test_put_incomparable_type_raises(self):
        s = build_set([1, 2, 3])
        with self.assertRaises(TypeError):
            s.put("x")

    def test_put_none_first_then_other_raises(self):
        s = BSTSet()
        s.put(None)  # allowed for the first key
        with self.assertRaises(TypeError):
            s.put(1)

    def test_sets_are_independent(self):
        a, b = build_set([1, 2]), build_set([9])
        self.assertEqual(list(a.in_order()), [1, 2])
        self.assertEqual(list(b.in_order()), [9])


class TestBSTSetTraversals(unittest.TestCase):
    def setUp(self):
        self.s = build_set(STANDARD_KEYS)

    def test_in_order(self):
        self.assertEqual(list(self.s.in_order()), STANDARD_IN_ORDER)

    def test_pre_order(self):
        self.assertEqual(list(self.s.pre_order()), STANDARD_PRE_ORDER)

    def test_post_order(self):
        self.assertEqual(list(self.s.post_order()), STANDARD_POST_ORDER)

    def test_iter_classic(self):
        self.assertEqual(list(self.s), STANDARD_IN_ORDER)

    def test_for_loop(self):
        self.assertEqual([k for k in self.s], STANDARD_IN_ORDER)

    def test_membership_via_iteration(self):
        self.assertIn(13, self.s)
        self.assertNotIn(99, self.s)

    def test_sorted_and_len_work(self):
        self.assertEqual(sorted(self.s), STANDARD_IN_ORDER)
        self.assertEqual(len(list(self.s)), len(STANDARD_KEYS))

    def test_single_element(self):
        s = build_set([1])
        self.assertEqual(list(s.in_order()), [1])
        self.assertEqual(list(s.pre_order()), [1])
        self.assertEqual(list(s.post_order()), [1])
        self.assertEqual(list(s), [1])

    def test_traversals_repeatable(self):
        self.assertEqual(list(self.s.pre_order()), list(self.s.pre_order()))
        self.assertEqual(list(self.s.post_order()), list(self.s.post_order()))

    def test_put_after_traversal_is_reflected(self):
        list(self.s.in_order())
        self.s.put(2)
        self.assertEqual(list(self.s.in_order()), [1, 2, 3, 4, 6, 7, 8, 10, 13, 14])

    def test_string_set(self):
        s = build_set(["pear", "apple", "fig", "apple"])
        self.assertEqual(list(s.in_order()), ["apple", "fig", "pear"])

    def test_sorted_input_moderate_size(self):
        s = build_set(range(500))
        self.assertEqual(list(s.in_order()), list(range(500)))

    def test_reverse_sorted_input_moderate_size(self):
        s = build_set(range(500, 0, -1))
        self.assertEqual(list(s.in_order()), list(range(1, 501)))

    def test_large_sorted_input_exceeds_recursion_limit(self):
        # POTENTIAL BUG: unbalanced tree plus recursive put()/traversals
        # raises RecursionError for ~1000+ sorted keys.
        s = build_set(range(1500))
        self.assertEqual(list(s.in_order()), list(range(1500)))


class TestBSTSetEmpty(unittest.TestCase):
    def test_pre_order_empty(self):
        self.assertEqual(list(BSTSet().pre_order()), [])

    def test_post_order_empty(self):
        self.assertEqual(list(BSTSet().post_order()), [])

    def test_in_order_empty_yields_nothing(self):
        # POTENTIAL BUG: BSTSet.in_order() has no empty-tree guard (unlike
        # pre_order/post_order), so it raises AttributeError on None.
        self.assertEqual(list(BSTSet().in_order()), [])

    def test_iter_empty_yields_nothing(self):
        # POTENTIAL BUG: BSTSet.__iter__ calls iter(None) on an empty set,
        # raising TypeError instead of producing an empty iteration.
        self.assertEqual(list(BSTSet()), [])

    def test_for_loop_on_empty_set(self):
        # Same bug as above, via a plain for loop.
        count = 0
        for _ in BSTSet():
            count += 1
        self.assertEqual(count, 0)

    def test_consistent_empty_behavior_across_traversals(self):
        # Inconsistency check: all three traversals should agree on empty sets.
        s = BSTSet()
        results = []
        for method in (s.in_order, s.pre_order, s.post_order):
            try:
                results.append(list(method()))
            except Exception as e:
                results.append(type(e).__name__)
        self.assertEqual(results, [[], [], []])


if __name__ == "__main__":
    unittest.main()