import unittest
import random

# Assuming the functions are imported from the module containing the source code (e.g., `basic_counting.py`)
from basic_counting import generate_lists, find_common, find_common_efficient, measure_time

class TestProgramFunctions(unittest.TestCase):

    def test_generate_lists_normal(self):
        size = 5
        list1, list2 = generate_lists(size)
        self.assertIsInstance(list1, list)
        self.assertIsInstance(list2, list)
        self.assertEqual(len(list1), size)
        self.assertEqual(len(list2), size)
        for val in list1:
            self.assertTrue(0 <= val < size * 2)
        for val in list2:
            self.assertTrue(0 <= val < size * 2)

    def test_generate_lists_zero_size(self):
        list1, list2 = generate_lists(0)
        self.assertEqual(list1, [])
        self.assertEqual(list2, [])

    def test_generate_lists_negative_size(self):
        with self.assertRaises(ValueError):
            generate_lists(-5)

    def test_generate_lists_invalid_type(self):
        with self.assertRaises(TypeError):
            generate_lists("10")
        with self.assertRaises(TypeError):
            generate_lists(5.5)

    def test_find_common_normal(self):
        list1 = [1, 2, 3, 4, 5]
        list2 = [4, 5, 6, 7, 8]
        self.assertEqual(find_common(list1, list2), 2)

    def test_find_common_disjoint(self):
        list1 = [1, 2, 3]
        list2 = [4, 5, 6]
        self.assertEqual(find_common(list1, list2), 0)

    def test_find_common_identical(self):
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]
        self.assertEqual(find_common(list1, list2), 3)

    def test_find_common_empty(self):
        self.assertEqual(find_common([], []), 0)
        self.assertEqual(find_common([1, 2, 3], []), 0)
        self.assertEqual(find_common([], [1, 2, 3]), 0)

    def test_find_common_with_duplicates(self):
        # find_common counts total matching pairs (nested loop behavior)
        list1 = [1, 1, 2]
        list2 = [1, 1, 3]
        self.assertEqual(find_common(list1, list2), 4)

    def test_find_common_efficient_normal(self):
        list1 = [1, 2, 3, 4, 5]
        list2 = [4, 5, 6, 7, 8]
        self.assertEqual(find_common_efficient(list1, list2), 2)

    def test_find_common_efficient_disjoint(self):
        list1 = [1, 2, 3]
        list2 = [4, 5, 6]
        self.assertEqual(find_common_efficient(list1, list2), 0)

    def test_find_common_efficient_identical(self):
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]
        self.assertEqual(find_common_efficient(list1, list2), 3)

    def test_find_common_efficient_empty(self):
        self.assertEqual(find_common_efficient([], []), 0)
        self.assertEqual(find_common_efficient([1, 2, 3], []), 0)
        self.assertEqual(find_common_efficient([], [1, 2, 3]), 0)

    def test_find_common_efficient_with_duplicates(self):
        # find_common_efficient uses sets, returning the count of unique common elements
        list1 = [1, 1, 2]
        list2 = [1, 1, 3]
        self.assertEqual(find_common_efficient(list1, list2), 1)

    def test_invalid_inputs_find_common(self):
        with self.assertRaises((TypeError, AttributeError)):
            find_common(None, [1, 2])
        with self.assertRaises((TypeError, AttributeError)):
            find_common([1, 2], 123)

    def test_invalid_inputs_find_common_efficient(self):
        with self.assertRaises((TypeError, AttributeError)):
            find_common_efficient(None, [1, 2])
        with self.assertRaises((TypeError, AttributeError)):
            find_common_efficient([1, 2], 123)

if __name__ == '__main__':
    unittest.main()