import unittest

from BST import BSTNode, BSTSet, BSTNode_Iterator


class TestBSTNodeAndSet(unittest.TestCase):

    def test_bst_set_empty(self):
        """Test boundary conditions and behavior of an empty BSTSet."""
        bst_set = BSTSet()
        self.assertIsNone(bst_set._head)

        # Traversals on an empty set should yield nothing without error
        self.assertEqual(list(bst_set.in_order()), [])
        self.assertEqual(list(bst_set.pre_order()), [])
        self.assertEqual(list(bst_set.post_order()), [])

        # Iteration on an empty set should raise TypeError due to iter(None)
        with self.assertRaises(TypeError):
            list(iter(bst_set))

    def test_single_node(self):
        """Test single node insertion and traversals."""
        bst_set = BSTSet()
        bst_set.put(10)

        self.assertEqual(list(bst_set.in_order()), [10])
        self.assertEqual(list(bst_set.pre_order()), [10])
        self.assertEqual(list(bst_set.post_order()), [10])
        self.assertEqual(list(iter(bst_set)), [10])

    def test_normal_tree_traversals(self):
        """Test normal inputs with multiple insertions and various traversal orders."""
        # Insert structure:
        #       5
        #      / \
        #     3   7
        #    / \   \
        #   2   4   8
        keys = [5, 3, 7, 2, 4, 8]
        bst_set = BSTSet()
        for k in keys:
            bst_set.put(k)

        # In-order: sorted order
        self.assertEqual(list(bst_set.in_order()), [2, 3, 4, 5, 7, 8])
        self.assertEqual(list(iter(bst_set)), [2, 3, 4, 5, 7, 8])

        # Pre-order: root, left, right
        self.assertEqual(list(bst_set.pre_order()), [5, 3, 2, 4, 7, 8])

        # Post-order: left, right, root
        self.assertEqual(list(bst_set.post_order()), [2, 4, 3, 8, 7, 5])

    def test_duplicate_keys(self):
        """Test edge condition with duplicate keys (duplicates should be ignored)."""
        bst_set = BSTSet()
        keys = [5, 3, 5, 7, 3, 2, 2]
        for k in keys:
            bst_set.put(k)

        self.assertEqual(list(bst_set.in_order()), [2, 3, 5, 7])

    def test_skewed_trees_left_and_right(self):
        """Test unusual/extreme boundary conditions like left-skewed and right-skewed trees."""
        # Right-skewed (ascending)
        bst_right = BSTSet()
        for i in range(1, 6):
            bst_right.put(i)
        self.assertEqual(list(bst_right.in_order()), [1, 2, 3, 4, 5])
        self.assertEqual(list(bst_right.pre_order()), [1, 2, 3, 4, 5])
        self.assertEqual(list(bst_right.post_order()), [5, 4, 3, 2, 1])

        # Left-skewed (descending)
        bst_left = BSTSet()
        for i in range(5, 0, -1):
            bst_left.put(i)
        self.assertEqual(list(bst_left.in_order()), [1, 2, 3, 4, 5])
        self.assertEqual(list(bst_left.pre_order()), [5, 4, 3, 2, 1])
        self.assertEqual(list(bst_left.post_order()), [1, 2, 3, 4, 5])

    def test_node_repr(self):
        """Test string representation of BSTNode."""
        node = BSTNode(42)
        self.assertEqual(repr(node), "BSTNode(key=42)")

    def test_iterator_stop_iteration(self):
        """Test invalid/boundary condition of iterating past the end of BSTNode_Iterator."""
        node = BSTNode(10, left=BSTNode(5), right=BSTNode(15))
        iterator = BSTNode_Iterator(node)

        self.assertEqual(next(iterator), 5)
        self.assertEqual(next(iterator), 10)
        self.assertEqual(next(iterator), 15)

        # Iterating past elements should raise StopIteration
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_negative_and_floating_point_keys(self):
        """Test unusual inputs containing negative numbers and floating-point values."""
        bst_set = BSTSet()
        keys = [0, -5.5, 3.14, -2, 10.1]
        for k in keys:
            bst_set.put(k)

        self.assertEqual(list(bst_set.in_order()), sorted(keys))

    def test_direct_node_methods(self):
        """Test calling traversal methods directly on a BSTNode instance."""
        root = BSTNode(10)
        root.put(5)
        root.put(15)

        self.assertEqual(list(root.in_order()), [5, 10, 15])
        self.assertEqual(list(root.pre_order()), [10, 5, 15])
        self.assertEqual(list(root.post_order()), [5, 15, 10])


if __name__ == '__main__':
    unittest.main()