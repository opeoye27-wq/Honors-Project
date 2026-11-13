import unittest
from BST import BSTSet, BSTNode


class TestBSTSet(unittest.TestCase):

    def setUp(self):
        self.bst = BSTSet()

    # -------------------------------
    # PUT: NORMAL INPUTS
    # -------------------------------

    def test_put_single_node(self):
        self.bst.put(10)
        self.assertEqual(list(self.bst.in_order()), [10])

    def test_put_multiple_nodes(self):
        for key in [10, 5, 15, 3, 7, 12, 20]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [3, 5, 7, 10, 12, 15, 20])

    def test_put_sorted_values(self):
        for key in [1, 2, 3, 4, 5]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [1, 2, 3, 4, 5])

    def test_put_reverse_sorted_values(self):
        for key in [5, 4, 3, 2, 1]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [1, 2, 3, 4, 5])

    def test_put_negative_values(self):
        for key in [-10, -5, -15, -20, -1]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [-20, -15, -10, -5, -1])

    def test_put_mixed_positive_and_negative(self):
        for key in [0, -10, 10, -5, 5]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [-10, -5, 0, 5, 10])

    # -------------------------------
    # PUT: DUPLICATES
    # -------------------------------

    def test_put_duplicate_root(self):
        self.bst.put(10)
        self.bst.put(10)

        self.assertEqual(list(self.bst.in_order()), [10])

    def test_put_duplicate_left_child(self):
        for key in [10, 5, 5]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [5, 10])

    def test_put_duplicate_right_child(self):
        for key in [10, 15, 15]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [10, 15])

    def test_put_multiple_duplicates(self):
        for key in [10, 5, 15, 5, 10, 15, 5, 10]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [5, 10, 15])

    # -------------------------------
    # IN-ORDER TRAVERSAL
    # -------------------------------

    def test_in_order_empty_tree(self):
        # Expected behavior: empty tree should produce no values.
        self.assertEqual(list(self.bst.in_order()), [])

    def test_in_order_single_node(self):
        self.bst.put(10)
        self.assertEqual(list(self.bst.in_order()), [10])

    def test_in_order_balanced_tree(self):
        for key in [10, 5, 15, 3, 7, 12, 20]:
            self.bst.put(key)

        self.assertEqual(
            list(self.bst.in_order()),
            [3, 5, 7, 10, 12, 15, 20]
        )

    def test_in_order_left_skewed_tree(self):
        for key in [5, 4, 3, 2, 1]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [1, 2, 3, 4, 5])

    def test_in_order_right_skewed_tree(self):
        for key in [1, 2, 3, 4, 5]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [1, 2, 3, 4, 5])

    # -------------------------------
    # PRE-ORDER TRAVERSAL
    # -------------------------------

    def test_pre_order_empty_tree(self):
        self.assertEqual(list(self.bst.pre_order()), [])

    def test_pre_order_single_node(self):
        self.bst.put(10)
        self.assertEqual(list(self.bst.pre_order()), [10])

    def test_pre_order_balanced_tree(self):
        for key in [10, 5, 15, 3, 7, 12, 20]:
            self.bst.put(key)

        self.assertEqual(
            list(self.bst.pre_order()),
            [10, 5, 3, 7, 15, 12, 20]
        )

    def test_pre_order_left_skewed_tree(self):
        for key in [5, 4, 3, 2, 1]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.pre_order()), [5, 4, 3, 2, 1])

    def test_pre_order_right_skewed_tree(self):
        for key in [1, 2, 3, 4, 5]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.pre_order()), [1, 2, 3, 4, 5])

    # -------------------------------
    # POST-ORDER TRAVERSAL
    # -------------------------------

    def test_post_order_empty_tree(self):
        self.assertEqual(list(self.bst.post_order()), [])

    def test_post_order_single_node(self):
        self.bst.put(10)
        self.assertEqual(list(self.bst.post_order()), [10])

    def test_post_order_balanced_tree(self):
        for key in [10, 5, 15, 3, 7, 12, 20]:
            self.bst.put(key)

        self.assertEqual(
            list(self.bst.post_order()),
            [3, 7, 5, 12, 20, 15, 10]
        )

    def test_post_order_left_skewed_tree(self):
        for key in [5, 4, 3, 2, 1]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.post_order()), [1, 2, 3, 4, 5])

    def test_post_order_right_skewed_tree(self):
        for key in [1, 2, 3, 4, 5]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.post_order()), [5, 4, 3, 2, 1])

    # -------------------------------
    # CLASSICAL ITERATION
    # -------------------------------

    def test_classical_iteration_single_node(self):
        self.bst.put(10)
        self.assertEqual(list(self.bst), [10])

    def test_classical_iteration_multiple_nodes(self):
        for key in [10, 5, 15, 3, 7]:
            self.bst.put(key)

        self.assertEqual(list(self.bst), [3, 5, 7, 10, 15])

    def test_classical_iteration_empty_tree(self):
        # Potential bug: BSTSet.__iter__ passes None to iter().
        with self.assertRaises((TypeError, AttributeError)):
            list(self.bst)

    def test_classical_iterator_can_be_used_multiple_times(self):
        for key in [10, 5, 15]:
            self.bst.put(key)

        self.assertEqual(list(self.bst), [5, 10, 15])
        self.assertEqual(list(self.bst), [5, 10, 15])

    def test_classical_iterator_independent_instances(self):
        for key in [10, 5, 15]:
            self.bst.put(key)

        iterator1 = iter(self.bst)
        iterator2 = iter(self.bst)

        self.assertEqual(next(iterator1), 5)
        self.assertEqual(next(iterator1), 10)
        self.assertEqual(next(iterator2), 5)

    def test_classical_iterator_stop_iteration(self):
        self.bst.put(10)

        iterator = iter(self.bst)

        self.assertEqual(next(iterator), 10)

        with self.assertRaises(StopIteration):
            next(iterator)

    # -------------------------------
    # ITERATOR BEHAVIOR
    # -------------------------------

    def test_iterator_returns_keys_not_nodes(self):
        self.bst.put(10)

        result = next(iter(self.bst))

        self.assertEqual(result, 10)
        self.assertNotIsInstance(result, BSTNode)

    def test_iterator_after_tree_modification(self):
        self.bst.put(10)
        self.bst.put(5)

        iterator = iter(self.bst)

        self.bst.put(15)

        # The classical iterator builds its queue when created.
        self.assertEqual(list(iterator), [5, 10])

    # -------------------------------
    # DIFFERENT DATA TYPES
    # -------------------------------

    def test_put_string_keys(self):
        for key in ["banana", "apple", "cherry"]:
            self.bst.put(key)

        self.assertEqual(
            list(self.bst.in_order()),
            ["apple", "banana", "cherry"]
        )

    def test_put_float_keys(self):
        for key in [3.5, 1.5, 2.5, 4.5]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [1.5, 2.5, 3.5, 4.5])

    def test_put_mixed_numeric_types(self):
        for key in [10, 5.5, 15, 2, 7.5]:
            self.bst.put(key)

        self.assertEqual(list(self.bst.in_order()), [2, 5.5, 10, 15])

    def test_put_none_as_root(self):
        self.bst.put(None)
        self.assertEqual(list(self.bst.in_order()), [None])

    def test_put_none_with_integer_root(self):
        self.bst.put(10)

        with self.assertRaises(TypeError):
            self.bst.put(None)

    def test_put_incompatible_types(self):
        self.bst.put(10)

        with self.assertRaises(TypeError):
            self.bst.put("hello")

    # -------------------------------
    # GENERATOR BEHAVIOR
    # -------------------------------

    def test_in_order_returns_generator(self):
        self.bst.put(10)

        result = self.bst.in_order()

        self.assertTrue(hasattr(result, "__next__"))

    def test_pre_order_returns_generator(self):
        self.bst.put(10)

        result = self.bst.pre_order()

        self.assertTrue(hasattr(result, "__next__"))

    def test_post_order_returns_generator(self):
        self.bst.put(10)

        result = self.bst.post_order()

        self.assertTrue(hasattr(result, "__next__"))

    def test_partial_in_order_iteration(self):
        for key in [10, 5, 15]:
            self.bst.put(key)

        iterator = self.bst.in_order()

        self.assertEqual(next(iterator), 5)
        self.assertEqual(next(iterator), 10)

    def test_partial_pre_order_iteration(self):
        for key in [10, 5, 15]:
            self.bst.put(key)

        iterator = self.bst.pre_order()

        self.assertEqual(next(iterator), 10)
        self.assertEqual(next(iterator), 5)

    def test_partial_post_order_iteration(self):
        for key in [10, 5, 15]:
            self.bst.put(key)

        iterator = self.bst.post_order()

        self.assertEqual(next(iterator), 5)
        self.assertEqual(next(iterator), 15)

    def test_generator_stop_iteration(self):
        self.bst.put(10)

        iterator = self.bst.in_order()

        self.assertEqual(next(iterator), 10)

        with self.assertRaises(StopIteration):
            next(iterator)

    # -------------------------------
    # CONSISTENCY BETWEEN TRAVERSALS
    # -------------------------------

    def test_all_traversals_contain_same_keys(self):
        for key in [10, 5, 15, 3, 7, 12, 20]:
            self.bst.put(key)

        in_order = list(self.bst.in_order())
        pre_order = list(self.bst.pre_order())
        post_order = list(self.bst.post_order())

        self.assertEqual(sorted(in_order), sorted(pre_order))
        self.assertEqual(sorted(in_order), sorted(post_order))

    def test_all_traversals_have_same_length(self):
        for key in [10, 5, 15, 3, 7, 12, 20]:
            self.bst.put(key)

        self.assertEqual(
            len(list(self.bst.in_order())),
            len(list(self.bst.pre_order()))
        )

        self.assertEqual(
            len(list(self.bst.in_order())),
            len(list(self.bst.post_order()))
        )

    # -------------------------------
    # LARGE INPUTS
    # -------------------------------

    def test_large_number_of_nodes(self):
        for key in range(1000):
            self.bst.put(key)

        result = list(self.bst.in_order())

        self.assertEqual(len(result), 1000)
        self.assertEqual(result, list(range(1000)))

    def test_large_number_of_duplicate_nodes(self):
        for _ in range(100):
            self.bst.put(10)

        self.assertEqual(list(self.bst.in_order()), [10])

    # -------------------------------
    # NODE REPRESENTATION
    # -------------------------------

    def test_node_repr(self):
        node = BSTNode(10)

        self.assertEqual(repr(node), "BSTNode(key=10)")

    def test_node_repr_with_string(self):
        node = BSTNode("hello")

        self.assertEqual(repr(node), "BSTNode(key=hello)")


if __name__ == "__main__":
    unittest.main()