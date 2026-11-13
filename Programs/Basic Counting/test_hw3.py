import unittest
from hw3 import generate_lists, find_common, find_common_efficient, measure_time

class Testhw3(unittest.TestCase):
    def test_generate_lists(self):
        list1, list2 = generate_lists(4)
        self.assertEqual(4, len(list1))
        self.assertEqual(4, len(list2))

    def test_find_common(self):
        list1 = [1,2,3,4]
        list2 = [5,6,7,8]
        self.assertEqual(0, (find_common(list1, list2)))
        list3 = [1,2,5,7]
        list4 = [1,3,6,7]
        self.assertEqual(2, (find_common(list3, list4)))

    def test_find_common_efficient(self):
        list1 = [1,2,3,4]
        list2 = [5,6,7,8]
        self.assertEqual(0, (find_common_efficient(list1, list2)))
        list3 = [1,2,5,7]
        list4 = [1,3,6,7]
        self.assertEqual(2, (find_common_efficient(list3, list4)))
    def test_measure_time(self):
        try:
            measure_time()
        except Exception as e:
            self.fail(f"measure_time() raised an exception:, {e}")

if __name__ == "__main__":
    unittest.main()