import unittest

from BST import BSTNode, BSTSet, BSTNode_Iterator


class TestBinarySearchTree(unittest.TestCase):

    def test_empty_set_initialization(self):
        """Test boundary condition: Empty set initialization and attributes."""
        bst = BSTSet()
        self.assertIsNone(bst._head)

        # Traversing or iterating over an empty BSTSet raises AttributeError
        # because _head is None.
        with self.assertRaises(AttributeError):
            list(iter(bst))
        with self.assertRaises(AttributeError):
            list(bst.in_order())
        with self.assertRaises(AttributeError):
            list(bst.pre_order())
        with self.assertRaises(AttributeError):
            list(bst.post_order())

    def test_single_node(self):
        """Test boundary condition: Tree with exactly one node."""
        bst = BSTSet()
        bst.put(42)

        self.assertIsNotNone(bst._head)
        self.assertEqual(bst._head.key, 42)
        self.assertEqual(list(bst.in_order()), [42])
        self.assertEqual(list(bst.pre_order()), [42])
        self.assertEqual(list(bst.post_order()), [42])
        self.assertEqual(list(iter(bst)), [42])

    def test_normal_insertions_and_traversals(self):
        """Test normal inputs with a balanced-like multi-level tree structure."""
        bst = BSTSet()
        keys = [5, 3, 7, 2, 4, 6, 8]
        for k in keys:
            bst.put(k)

        # In-order traversal should return sorted keys
        self.assertEqual(list(bst.in_order()), [2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(list(iter(bst)), [2, 3, 4, 5, 6, 7, 8])

        # Pre-order traversal: Root -> Left Subtree -> Right Subtree
        self.assertEqual(list(bst.pre_order()), [5, 3, 2, 4, 7, 6, 8])

        # Post-order traversal: Left Subtree -> Right Subtree -> Root
        self.assertEqual(list(bst.post_order()), [2, 4, 3, 6, 8, 7, 5])

    def test_duplicate_keys(self):
        """Test edge condition: Inserting duplicate keys (should be ignored)."""
        bst = BSTSet()
        keys = [10, 10, 5, 5, 15, 15]
        for k in keys:
            bst.put(k)

        self.assertEqual(list(bst.in_order()), [5, 10, 15])

    def test_skewed_trees(self):
        """Test boundary/unusual conditions: Left-skewed and right-skewed trees."""
        # Left-skewed (descending inputs)
        bst_left = BSTSet()
        for k in [5, 4, 3, 2, 1]:
            bst_left.put(k)
        self.assertEqual(list(bst_left.in_order()), [1, 2, 3, 4, 5])
        self.assertEqual(list(bst_left.pre_order()), [5, 4, 3, 2, 1])

        # Right-skewed (ascending inputs)
        bst_right = BSTSet()
        for k in [1, 2, 3, 4, 5]:
            bst_right.put(k)
        self.assertEqual(list(bst_right.in_order()), [1, 2, 3, 4, 5])
        self.assertEqual(list(bst_right.pre_order()), [1, 2, 3, 4, 5])

    def test_unusual_inputs_types(self):
        """Test unusual inputs: Negative numbers, floating-point numbers, and strings."""
        # Negative numbers and floats
        bst_nums = BSTSet()
        for k in [0, -3.5, 3.5, -1, 2]:
            bst_nums.put(k)
        self.assertEqual(list(bst_nums.in_order()), [-3.5, -1, 0, 2, 3.5])

        # String keys
        bst_str = BSTSet()
        for s in ["banana", "apple", "cherry", "date"]:
            bst_str.put(s)
        self.assertEqual(list(bst_str.in_order()), ["apple", "banana", "cherry", "date"])

    def test_invalid_inputs_type_error(self):
        """Test invalid inputs: Mixing incompatible types during insertion raises TypeError."""
        bst = BSTSet()
        bst.put(100)

        with self.assertRaises(TypeError):
            bst.put("invalid_string_comparison")

    def test_node_representation(self):
        """Test the __repr__ method of BSTNode."""
        node = BSTNode(99)
        self.assertEqual(repr(node), "BSTNode(key=99)")


if __name__ == "__main__":
    unittest.main()