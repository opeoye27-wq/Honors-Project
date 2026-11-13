import unittest

# Assuming the provided code is saved in a module named 'basic_counting.py',
# import the functions to be tested:
from basic_counting import generate_lists, find_common, find_common_efficient

class TestGenerateLists(unittest.TestCase):
    
    def test_generate_lists_normal(self):
        """Test normal behavior with a standard positive size."""
        size = 5
        list1, list2 = generate_lists(size)
        self.assertEqual(len(list1), size)
        self.assertEqual(len(list2), size)
        # Verify elements are within the expected range [0, size * 2)
        for item in list1 + list2:
            self.assertTrue(0 <= item < size * 2)

    def test_generate_lists_zero_size(self):
        """Boundary condition: size is 0."""
        list1, list2 = generate_lists(0)
        self.assertEqual(list1, [])
        self.assertEqual(list2, [])

    def test_generate_lists_negative_size(self):
        """Invalid input: negative size should raise ValueError."""
        with self.assertRaises(ValueError):
            generate_lists(-5)

    def test_generate_lists_invalid_type(self):
        """Invalid input: non-integer size should raise TypeError."""
        with self.assertRaises(TypeError):
            generate_lists("10")


class TestFindCommon(unittest.TestCase):
    
    def test_find_common_normal(self):
        """Test normal input with standard overlapping elements."""
        self.assertEqual(find_common([1, 2, 3], [2, 3, 4]), 2)

    def test_find_common_no_overlap(self):
        """Boundary condition: lists with no common elements."""
        self.assertEqual(find_common([1, 2], [3, 4]), 0)

    def test_find_common_empty_lists(self):
        """Boundary conditions: empty lists combinations."""
        self.assertEqual(find_common([], []), 0)
        self.assertEqual(find_common([1, 2], []), 0)
        self.assertEqual(find_common([], [1, 2]), 0)

    def test_find_common_with_duplicates(self):
        """
        Unusual input/Edge case: Lists with duplicate values.
        Note: find_common uses nested loops, counting total matching pairs,
        so duplicates increase the count multi-fold.
        """
        self.assertEqual(find_common([1, 1, 2], [1, 1]), 4)

    def test_find_common_invalid_input(self):
        """Invalid input: passing non-iterable/None instead of a list."""
        with self.assertRaises(TypeError):
            find_common(None, [1, 2])


class TestFindCommonEfficient(unittest.TestCase):
    
    def test_find_common_efficient_normal(self):
        """Test normal input with standard overlapping elements."""
        self.assertEqual(find_common_efficient([1, 2, 3], [2, 3, 4]), 2)

    def test_find_common_efficient_no_overlap(self):
        """Boundary condition: lists with no common elements."""
        self.assertEqual(find_common_efficient([1, 2], [3, 4]), 0)

    def test_find_common_efficient_empty_lists(self):
        """Boundary conditions: empty lists combinations."""
        self.assertEqual(find_common_efficient([], []), 0)
        self.assertEqual(find_common_efficient([1, 2], []), 0)
        self.assertEqual(find_common_efficient([], [1, 2]), 0)

    def test_find_common_efficient_with_duplicates(self):
        """
        Potential Bug / Behavioral Difference Test:
        find_common_efficient uses sets, meaning duplicates are collapsed
        and it only returns the count of unique intersecting elements.
        Compare this to find_common which counts total occurrences.
        """
        self.assertEqual(find_common_efficient([1, 1, 2], [1, 1]), 1)

    def test_find_common_efficient_unhashable_elements(self):
        """
        Unusual/Invalid input: Sets require hashable elements.
        Passing lists containing unhashable types (like nested lists) should raise TypeError.
        """
        with self.assertRaises(TypeError):
            find_common_efficient([[1], 2], [[1], 3])

    def test_find_common_efficient_invalid_input(self):
        """Invalid input: passing non-iterable/integers instead of lists."""
        with self.assertRaises(TypeError):
            find_common_efficient(123, [1, 2])


if __name__ == '__main__':
    unittest.main()