import unittest

from BST import BSTNode, BSTSet


class TestBSTNodeAndSet(unittest.TestCase):

    def test_node_init_and_repr(self):
        node = BSTNode(10)
        self.assertEqual(node.key, 10)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
        self.assertEqual(repr(node), "BSTNode(key=10)")

    def test_single_node_put_and_traversals(self):
        node = BSTNode(5)
        self.assertEqual(list(node.in_order()), [5])
        self.assertEqual(list(node.pre_order()), [5])
        self.assertEqual(list(node.post_order()), [5])
        self.assertEqual(list(iter(node)), [5])

    def test_bst_node_put_and_traversals(self):
        root = BSTNode(10)
        root.put(5)
        root.put(15)
        root.put(3)
        root.put(7)

        # In-order should be sorted: 3, 5, 7, 10, 15
        self.assertEqual(list(root.in_order()), [3, 5, 7, 10, 15])
        # Pre-order: root, left subtree, right subtree
        self.assertEqual(list(root.pre_order()), [10, 5, 3, 7, 15])
        # Post-order: left subtree, right subtree, root
        self.assertEqual(list(root.post_order()), [3, 7, 5, 15, 10])

    def test_duplicate_keys(self):
        root = BSTNode(10)
        root.put(10)
        root.put(5)
        root.put(5)
        self.assertEqual(list(root.in_order()), [5, 10])

    def test_skewed_tree(self):
        root = BSTNode(1)
        root.put(2)
        root.put(3)
        root.put(4)
        self.assertEqual(list(root.in_order()), [1, 2, 3, 4])
        self.assertEqual(list(root.pre_order()), [1, 2, 3, 4])
        self.assertEqual(list(root.post_order()), [4, 3, 2, 1])

    def test_bst_node_iterator_exhaustion(self):
        root = BSTNode(2)
        root.put(1)
        root.put(3)
        iterator = iter(root)
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 2)
        self.assertEqual(next(iterator), 3)
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_bst_set_operations(self):
        bst_set = BSTSet()
        bst_set.put(20)
        bst_set.put(10)
        bst_set.put(30)
        bst_set.put(5)

        self.assertEqual(list(bst_set.in_order()), [5, 10, 20, 30])
        self.assertEqual(list(bst_set.pre_order()), [20, 10, 5, 30])
        self.assertEqual(list(bst_set.post_order()), [5, 10, 30, 20])
        self.assertEqual(list(iter(bst_set)), [5, 10, 20, 30])

    def test_bst_set_empty_graceful_and_edge_cases(self):
        bst_set = BSTSet()
        # pre_order and post_order handle empty set gracefully via check
        self.assertEqual(list(bst_set.pre_order()), [])
        self.assertEqual(list(bst_set.post_order()), [])

        # in_order and __iter__ on an empty BSTSet raise AttributeError/TypeError
        # because self._head is None (highlighting potential implementation bugs)
        with self.assertRaises((AttributeError, TypeError)):
            list(bst_set.in_order())
        with self.assertRaises((AttributeError, TypeError)):
            list(iter(bst_set))

    def test_unusual_inputs_negative_and_floats(self):
        root = BSTNode(0)
        root.put(-5)
        root.put(5.5)
        root.put(-2.1)
        self.assertEqual(list(root.in_order()), [-5, -2.1, 0, 5.5])


if __name__ == '__main__':
    unittest.main()