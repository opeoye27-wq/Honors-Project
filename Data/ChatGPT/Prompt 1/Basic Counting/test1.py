import unittest
from unittest.mock import patch
import math

# Replace main with the name of the Python file containing the program.
import basic_counting


class TestGenerateLists(unittest.TestCase):

    def test_zero_size(self):
        list1, list2 = basic_counting.generate_lists(0)
        self.assertEqual(list1, [])
        self.assertEqual(list2, [])

    def test_size_one(self):
        list1, list2 = basic_counting.generate_lists(1)
        self.assertEqual(len(list1), 1)
        self.assertEqual(len(list2), 1)
        self.assertTrue(0 <= list1[0] < 2)
        self.assertTrue(0 <= list2[0] < 2)

    def test_normal_size(self):
        size = 100
        list1, list2 = basic_counting.generate_lists(size)

        self.assertEqual(len(list1), size)
        self.assertEqual(len(list2), size)
        self.assertEqual(len(set(list1)), size)
        self.assertEqual(len(set(list2)), size)

        self.assertTrue(all(0 <= x < size * 2 for x in list1))
        self.assertTrue(all(0 <= x < size * 2 for x in list2))

    def test_lists_are_independently_generated(self):
        with patch("basic_counting.random.sample", side_effect=[
            [0, 1, 2], [3, 4, 5]
        ]):
            list1, list2 = basic_counting.generate_lists(3)

        self.assertEqual(list1, [0, 1, 2])
        self.assertEqual(list2, [3, 4, 5])

    def test_negative_size_raises_value_error(self):
        with self.assertRaises(ValueError):
            basic_counting.generate_lists(-1)

    def test_size_larger_than_population_raises_value_error(self):
        with self.assertRaises(ValueError):
            basic_counting.generate_lists(3) if False else basic_counting.generate_lists(7)

    def test_non_integer_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            basic_counting.generate_lists(2.5)

    def test_string_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            basic_counting.generate_lists("5")


class TestFindCommon(unittest.TestCase):

    def test_both_lists_empty(self):
        self.assertEqual(basic_counting.find_common([], []), 0)

    def test_one_list_empty(self):
        self.assertEqual(basic_counting.find_common([], [1, 2, 3]), 0)
        self.assertEqual(basic_counting.find_common([1, 2, 3], []), 0)

    def test_no_common_elements(self):
        self.assertEqual(basic_counting.find_common([1, 2], [3, 4]), 0)

    def test_all_elements_common(self):
        self.assertEqual(basic_counting.find_common([1, 2, 3], [3, 2, 1]), 3)

    def test_partial_overlap(self):
        self.assertEqual(basic_counting.find_common([1, 2, 3], [2, 3, 4]), 2)

    def test_negative_and_zero_values(self):
        self.assertEqual(
            basic_counting.find_common([-2, -1, 0, 1], [-1, 0, 2]), 2
        )

    def test_duplicate_elements_in_first_list(self):
        self.assertEqual(basic_counting.find_common([1, 1, 2], [1, 2]), 3)

    def test_duplicate_elements_in_second_list(self):
        self.assertEqual(basic_counting.find_common([1, 2], [1, 1, 2]), 3)

    def test_duplicates_in_both_lists(self):
        self.assertEqual(basic_counting.find_common([1, 1, 2], [1, 1, 2]), 5)

    def test_repeated_matches_count_every_pair(self):
        self.assertEqual(basic_counting.find_common([7, 7], [7, 7, 7]), 6)

    def test_different_numeric_types(self):
        self.assertEqual(basic_counting.find_common([1, 2.0], [1.0, 2]), 2)

    def test_boolean_and_integer_equality(self):
        self.assertEqual(basic_counting.find_common([True, False], [1, 0]), 2)

    def test_strings(self):
        self.assertEqual(basic_counting.find_common(["a", "b"], ["b", "c"]), 1)

    def test_mixed_types(self):
        self.assertEqual(basic_counting.find_common([1, "a", None], ["a", None, 2]), 2)

    def test_none_inputs_raise_type_error(self):
        with self.assertRaises(TypeError):
            basic_counting.find_common(None, [1, 2])

        with self.assertRaises(TypeError):
            basic_counting.find_common([1, 2], None)

    def test_non_iterable_inputs_raise_type_error(self):
        with self.assertRaises(TypeError):
            basic_counting.find_common(10, [1, 2])

        with self.assertRaises(TypeError):
            basic_counting.find_common([1, 2], 10)

    def test_generators_are_supported(self):
        self.assertEqual(
            basic_counting.find_common((x for x in [1, 2, 3]), [2, 3]), 2
        )

    def test_generator_second_argument_is_not_reusable(self):
        self.assertEqual(
            basic_counting.find_common([1, 2], (x for x in [1, 2])), 1
        )

    def test_large_lists(self):
        list1 = list(range(500))
        list2 = list(range(250, 750))
        self.assertEqual(basic_counting.find_common(list1, list2), 250)


class TestFindCommonEfficient(unittest.TestCase):

    def test_both_lists_empty(self):
        self.assertEqual(basic_counting.find_common_efficient([], []), 0)

    def test_one_list_empty(self):
        self.assertEqual(basic_counting.find_common_efficient([], [1, 2]), 0)
        self.assertEqual(basic_counting.find_common_efficient([1, 2], []), 0)

    def test_no_common_elements(self):
        self.assertEqual(basic_counting.find_common_efficient([1, 2], [3, 4]), 0)

    def test_all_elements_common(self):
        self.assertEqual(
            basic_counting.find_common_efficient([1, 2, 3], [3, 2, 1]), 3
        )

    def test_partial_overlap(self):
        self.assertEqual(
            basic_counting.find_common_efficient([1, 2, 3], [2, 3, 4]), 2
        )

    def test_negative_and_zero_values(self):
        self.assertEqual(
            basic_counting.find_common_efficient([-2, -1, 0, 1], [-1, 0, 2]), 2
        )

    def test_duplicates_in_first_list_count_once(self):
        self.assertEqual(
            basic_counting.find_common_efficient([1, 1, 2], [1, 2]), 2
        )

    def test_duplicates_in_second_list_count_once(self):
        self.assertEqual(
            basic_counting.find_common_efficient([1, 2], [1, 1, 2]), 2
        )

    def test_duplicates_in_both_lists_count_once(self):
        self.assertEqual(
            basic_counting.find_common_efficient([1, 1, 2], [1, 1, 2]), 2
        )

    def test_different_numeric_types(self):
        self.assertEqual(
            basic_counting.find_common_efficient([1, 2.0], [1.0, 2]), 2
        )

    def test_boolean_and_integer_equality(self):
        self.assertEqual(
            basic_counting.find_common_efficient([True, False], [1, 0]), 2
        )

    def test_strings(self):
        self.assertEqual(
            basic_counting.find_common_efficient(["a", "b"], ["b", "c"]), 1
        )

    def test_mixed_hashable_types(self):
        self.assertEqual(
            basic_counting.find_common_efficient([1, "a", None], ["a", None, 2]), 2
        )

    def test_none_inputs_raise_type_error(self):
        with self.assertRaises(TypeError):
            basic_counting.find_common_efficient(None, [1, 2])

        with self.assertRaises(TypeError):
            basic_counting.find_common_efficient([1, 2], None)

    def test_non_iterable_inputs_raise_type_error(self):
        with self.assertRaises(TypeError):
            basic_counting.find_common_efficient(10, [1, 2])

        with self.assertRaises(TypeError):
            basic_counting.find_common_efficient([1, 2], 10)

    def test_unhashable_elements_raise_type_error(self):
        with self.assertRaises(TypeError):
            basic_counting.find_common_efficient([[1], [2]], [[1], [2]])

    def test_generators_are_supported(self):
        self.assertEqual(
            basic_counting.find_common_efficient((x for x in [1, 2, 3]), [2, 3]), 2
        )

    def test_large_lists(self):
        list1 = list(range(10000))
        list2 = list(range(5000, 15000))
        self.assertEqual(basic_counting.find_common_efficient(list1, list2), 5000)


class TestFunctionConsistency(unittest.TestCase):

    def test_both_functions_agree_for_unique_integer_lists(self):
        test_cases = [
            ([], []),
            ([1], [1]),
            ([1, 2, 3], [3, 4, 5]),
            ([-5, 0, 5], [0, 5, 10]),
            (list(range(20)), list(range(10, 30))),
        ]

        for list1, list2 in test_cases:
            with self.subTest(list1=list1, list2=list2):
                self.assertEqual(
                    basic_counting.find_common(list1, list2),
                    basic_counting.find_common_efficient(list1, list2),
                )

    def test_functions_differ_when_duplicates_exist(self):
        list1 = [1, 1, 2]
        list2 = [1, 2]

        self.assertEqual(basic_counting.find_common(list1, list2), 3)
        self.assertEqual(basic_counting.find_common_efficient(list1, list2), 2)


class TestMeasureTime(unittest.TestCase):

    @patch("builtins.print")
    @patch("basic_counting.time.perf_counter", side_effect=[
        1.0, 1.1, 2.0, 2.1,
        3.0, 3.1, 4.0, 4.1,
        5.0, 5.1, 6.0, 6.1,
        7.0, 7.1, 8.0, 8.1,
    ])
    @patch("basic_counting.generate_lists")
    def test_measure_time_runs_for_all_sizes(
        self, mock_generate_lists, mock_perf_counter, mock_print
    ):
        mock_generate_lists.side_effect = [
            ([1] * size, [1] * size)
            for size in [10, 100, 1000, 10000]
        ]

        basic_counting.measure_time()

        self.assertEqual(mock_generate_lists.call_count, 4)
        self.assertEqual(mock_print.call_count, 5)

    @patch("builtins.print")
    @patch("basic_counting.time.perf_counter", side_effect=[
        1.0, 1.1, 2.0, 2.1,
        3.0, 3.1, 4.0, 4.1,
        5.0, 5.1, 6.0, 6.1,
        7.0, 7.1, 8.0, 8.1,
    ])
    @patch("basic_counting.generate_lists", return_value=([1], [1]))
    def test_measure_time_prints_header_and_results(
        self, mock_generate_lists, mock_perf_counter, mock_print
    ):
        basic_counting.measure_time()

        first_output = mock_print.call_args_list[0].args[0]
        self.assertIn("List Size", first_output)
        self.assertIn("find_common Time", first_output)
        self.assertEqual(mock_print.call_count, 5)

    @patch("builtins.print")
    @patch("basic_counting.time.perf_counter", side_effect=[
        1.0, 1.1, 2.0, 2.1,
        3.0, 3.1, 4.0, 4.1,
        5.0, 5.1, 6.0, 6.1,
        7.0, 7.1, 8.0, 8.1,
    ])
    @patch("basic_counting.generate_lists", return_value=([1], [1]))
    def test_measure_time_outputs_formatted_times(
        self, mock_generate_lists, mock_perf_counter, mock_print
    ):
        basic_counting.measure_time()

        for call in mock_print.call_args_list[1:]:
            output = call.args[0]
            self.assertTrue(output.strip())
            self.assertIn(".", output)

    def test_measure_time_does_not_return_value(self):
        with patch("builtins.print"), patch(
            "basic_counting.generate_lists", return_value=([1], [1])
        ), patch("basic_counting.time.perf_counter", side_effect=[
            1.0, 1.1, 2.0, 2.1,
            3.0, 3.1, 4.0, 4.1,
            5.0, 5.1, 6.0, 6.1,
            7.0, 7.1, 8.0, 8.1,
        ]):
            self.assertIsNone(basic_counting.measure_time())


if __name__ == "__main__":
    unittest.main()
