import io
import itertools
import random
import unittest
from contextlib import redirect_stdout
from unittest import mock

# Change this import to match the filename of the module under test.
import basic_counting as cl


class TestGenerateLists(unittest.TestCase):
    # ---------- normal inputs ----------
    def test_returns_tuple_of_two_lists(self):
        result = cl.generate_lists(10)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[1], list)

    def test_lengths_match_size(self):
        for size in (1, 2, 10, 100, 1000):
            with self.subTest(size=size):
                l1, l2 = cl.generate_lists(size)
                self.assertEqual(len(l1), size)
                self.assertEqual(len(l2), size)

    def test_elements_unique_within_each_list(self):
        l1, l2 = cl.generate_lists(500)
        self.assertEqual(len(set(l1)), len(l1))
        self.assertEqual(len(set(l2)), len(l2))

    def test_elements_within_expected_range(self):
        size = 200
        l1, l2 = cl.generate_lists(size)
        for value in l1 + l2:
            self.assertIsInstance(value, int)
            self.assertGreaterEqual(value, 0)
            self.assertLess(value, size * 2)

    def test_lists_are_distinct_objects(self):
        l1, l2 = cl.generate_lists(10)
        self.assertIsNot(l1, l2)

    def test_two_lists_differ_for_large_size(self):
        # Probability of two independent samples of 1000 from 2000 being
        # identical (same order) is effectively zero.
        l1, l2 = cl.generate_lists(1000)
        self.assertNotEqual(l1, l2)

    def test_reproducible_with_same_seed(self):
        random.seed(42)
        first = cl.generate_lists(50)
        random.seed(42)
        second = cl.generate_lists(50)
        self.assertEqual(first, second)

    def test_different_seeds_give_different_results(self):
        random.seed(1)
        first = cl.generate_lists(100)
        random.seed(2)
        second = cl.generate_lists(100)
        self.assertNotEqual(first, second)

    # ---------- boundary conditions ----------
    def test_size_zero_returns_empty_lists(self):
        self.assertEqual(cl.generate_lists(0), ([], []))

    def test_size_one(self):
        l1, l2 = cl.generate_lists(1)
        self.assertEqual(len(l1), 1)
        self.assertEqual(len(l2), 1)
        self.assertIn(l1[0], (0, 1))
        self.assertIn(l2[0], (0, 1))

    def test_size_two_values_come_from_zero_to_three(self):
        l1, l2 = cl.generate_lists(2)
        self.assertTrue(set(l1) <= {0, 1, 2, 3})
        self.assertTrue(set(l2) <= {0, 1, 2, 3})

    # ---------- invalid inputs ----------
    def test_negative_size_raises_value_error(self):
        for size in (-1, -10):
            with self.subTest(size=size):
                with self.assertRaises(ValueError):
                    cl.generate_lists(size)

    def test_float_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.generate_lists(5.0)

    def test_none_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.generate_lists(None)

    def test_string_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.generate_lists("5")

    def test_list_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.generate_lists([5])


class TestFindCommon(unittest.TestCase):
    # ---------- normal inputs ----------
    def test_partial_overlap(self):
        self.assertEqual(cl.find_common([1, 2, 3, 4], [3, 4, 5, 6]), 2)

    def test_identical_lists(self):
        self.assertEqual(cl.find_common([1, 2, 3], [1, 2, 3]), 3)

    def test_no_overlap(self):
        self.assertEqual(cl.find_common([1, 2, 3], [4, 5, 6]), 0)

    def test_order_does_not_matter(self):
        self.assertEqual(cl.find_common([3, 1, 2], [2, 3, 1]), 3)

    def test_symmetric(self):
        a, b = [1, 2, 3, 7], [3, 7, 9]
        self.assertEqual(cl.find_common(a, b), cl.find_common(b, a))

    def test_returns_int(self):
        self.assertIsInstance(cl.find_common([1], [1]), int)

    def test_does_not_mutate_inputs(self):
        a, b = [3, 1, 2], [2, 5, 3]
        a_copy, b_copy = a[:], b[:]
        cl.find_common(a, b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)

    def test_values_from_generate_lists_bounded_by_size(self):
        random.seed(0)
        l1, l2 = cl.generate_lists(50)
        result = cl.find_common(l1, l2)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 50)

    # ---------- boundary conditions ----------
    def test_both_empty(self):
        self.assertEqual(cl.find_common([], []), 0)

    def test_first_empty(self):
        self.assertEqual(cl.find_common([], [1, 2, 3]), 0)

    def test_second_empty(self):
        self.assertEqual(cl.find_common([1, 2, 3], []), 0)

    def test_single_element_match(self):
        self.assertEqual(cl.find_common([5], [5]), 1)

    def test_single_element_no_match(self):
        self.assertEqual(cl.find_common([5], [6]), 0)

    def test_one_element_in_large_list(self):
        self.assertEqual(cl.find_common([299], list(range(300))), 1)

    def test_moderately_large_identical_lists(self):
        data = list(range(300))
        self.assertEqual(cl.find_common(data, data), 300)

    # ---------- unusual inputs ----------
    def test_negative_numbers_and_zero(self):
        self.assertEqual(cl.find_common([-1, 0, 1], [-1, 0, 2]), 2)

    def test_duplicates_in_first_list_counted_per_pair(self):
        # 1 appears twice in list1 and matches once in list2 -> 2 pairs, plus 2 -> 1 pair
        self.assertEqual(cl.find_common([1, 1, 2], [1, 2]), 3)

    def test_duplicates_in_both_lists_count_all_pairs(self):
        # 2 x 2 matching pairs
        self.assertEqual(cl.find_common([1, 1], [1, 1]), 4)

    def test_strings(self):
        self.assertEqual(cl.find_common(["a", "b", "c"], ["b", "c", "d"]), 2)

    def test_strings_as_iterables(self):
        self.assertEqual(cl.find_common("abc", "bcd"), 2)

    def test_case_sensitive_strings(self):
        self.assertEqual(cl.find_common(["A"], ["a"]), 0)

    def test_int_and_equal_float_match(self):
        self.assertEqual(cl.find_common([1], [1.0]), 1)

    def test_bool_matches_equal_int(self):
        self.assertEqual(cl.find_common([1], [True]), 1)

    def test_none_elements_match(self):
        self.assertEqual(cl.find_common([None], [None]), 1)

    def test_tuples_as_input(self):
        self.assertEqual(cl.find_common((1, 2, 3), (2, 3, 4)), 2)

    def test_sets_as_input(self):
        self.assertEqual(cl.find_common({1, 2, 3}, {2, 3, 4}), 2)

    def test_unhashable_elements_are_supported(self):
        self.assertEqual(cl.find_common([[1], [2]], [[2], [3]]), 1)

    def test_nan_is_never_equal_to_itself(self):
        nan = float("nan")
        self.assertEqual(cl.find_common([nan], [nan]), 0)

    def test_empty_first_list_with_invalid_second_does_not_raise(self):
        # Inner loop never runs, so an invalid list2 goes unnoticed.
        self.assertEqual(cl.find_common([], None), 0)

    # ---------- potential bug: single-use iterators ----------
    @unittest.expectedFailure
    def test_iterator_as_second_argument_is_fully_compared(self):
        # BUG: the inner loop exhausts the iterator on the first outer pass,
        # so only the first element of list1 is ever compared. Returns 1, not 2.
        self.assertEqual(cl.find_common([1, 2], iter([1, 2])), 2)

    # ---------- invalid inputs ----------
    def test_none_first_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.find_common(None, [1, 2])

    def test_none_second_argument_with_nonempty_first_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.find_common([1, 2], None)

    def test_int_first_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.find_common(5, [1, 2])

    def test_int_second_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.find_common([1, 2], 5)

    def test_missing_arguments_raise_type_error(self):
        with self.assertRaises(TypeError):
            cl.find_common([1, 2])


class TestFindCommonEfficient(unittest.TestCase):
    # ---------- normal inputs ----------
    def test_partial_overlap(self):
        self.assertEqual(cl.find_common_efficient([1, 2, 3, 4], [3, 4, 5, 6]), 2)

    def test_identical_lists(self):
        self.assertEqual(cl.find_common_efficient([1, 2, 3], [1, 2, 3]), 3)

    def test_no_overlap(self):
        self.assertEqual(cl.find_common_efficient([1, 2, 3], [4, 5, 6]), 0)

    def test_order_does_not_matter(self):
        self.assertEqual(cl.find_common_efficient([3, 1, 2], [2, 3, 1]), 3)

    def test_symmetric(self):
        a, b = [1, 2, 3, 7], [3, 7, 9]
        self.assertEqual(
            cl.find_common_efficient(a, b), cl.find_common_efficient(b, a)
        )

    def test_returns_int(self):
        self.assertIsInstance(cl.find_common_efficient([1], [1]), int)

    def test_does_not_mutate_inputs(self):
        a, b = [3, 1, 2], [2, 5, 3]
        a_copy, b_copy = a[:], b[:]
        cl.find_common_efficient(a, b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)

    # ---------- boundary conditions ----------
    def test_both_empty(self):
        self.assertEqual(cl.find_common_efficient([], []), 0)

    def test_first_empty(self):
        self.assertEqual(cl.find_common_efficient([], [1, 2, 3]), 0)

    def test_second_empty(self):
        self.assertEqual(cl.find_common_efficient([1, 2, 3], []), 0)

    def test_single_element_match(self):
        self.assertEqual(cl.find_common_efficient([5], [5]), 1)

    def test_single_element_no_match(self):
        self.assertEqual(cl.find_common_efficient([5], [6]), 0)

    def test_large_inputs(self):
        a = list(range(200000))
        b = list(range(100000, 300000))
        self.assertEqual(cl.find_common_efficient(a, b), 100000)

    # ---------- unusual inputs ----------
    def test_negative_numbers_and_zero(self):
        self.assertEqual(cl.find_common_efficient([-1, 0, 1], [-1, 0, 2]), 2)

    def test_duplicates_are_counted_once(self):
        self.assertEqual(cl.find_common_efficient([1, 1, 2], [1, 2]), 2)

    def test_duplicates_in_both_lists_counted_once(self):
        self.assertEqual(cl.find_common_efficient([1, 1], [1, 1]), 1)

    def test_strings(self):
        self.assertEqual(
            cl.find_common_efficient(["a", "b", "c"], ["b", "c", "d"]), 2
        )

    def test_strings_as_iterables(self):
        self.assertEqual(cl.find_common_efficient("abc", "bcd"), 2)

    def test_int_and_equal_float_match(self):
        self.assertEqual(cl.find_common_efficient([1], [1.0]), 1)

    def test_bool_matches_equal_int(self):
        self.assertEqual(cl.find_common_efficient([1], [True]), 1)

    def test_none_elements_match(self):
        self.assertEqual(cl.find_common_efficient([None], [None]), 1)

    def test_tuples_sets_and_iterators_as_input(self):
        self.assertEqual(cl.find_common_efficient((1, 2, 3), (2, 3, 4)), 2)
        self.assertEqual(cl.find_common_efficient({1, 2, 3}, {2, 3, 4}), 2)
        self.assertEqual(cl.find_common_efficient([1, 2], iter([1, 2])), 2)

    def test_unhashable_elements_raise_type_error(self):
        # Unlike find_common, the set-based version cannot handle lists as elements.
        with self.assertRaises(TypeError):
            cl.find_common_efficient([[1], [2]], [[2], [3]])

    def test_same_nan_object_is_found_via_identity(self):
        # Sets match by identity first, so the same NaN object IS found,
        # whereas find_common reports 0.
        nan = float("nan")
        self.assertEqual(cl.find_common_efficient([nan], [nan]), 1)

    # ---------- invalid inputs ----------
    def test_none_first_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.find_common_efficient(None, [1, 2])

    def test_none_second_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.find_common_efficient([1, 2], None)

    def test_empty_first_with_none_second_raises_type_error(self):
        with self.assertRaises(TypeError):
            cl.find_common_efficient([], None)

    def test_int_arguments_raise_type_error(self):
        with self.assertRaises(TypeError):
            cl.find_common_efficient(5, 5)

    def test_missing_arguments_raise_type_error(self):
        with self.assertRaises(TypeError):
            cl.find_common_efficient([1, 2])


class TestImplementationsAgree(unittest.TestCase):
    def test_agree_on_unique_random_lists(self):
        for seed in range(25):
            for size in (0, 1, 2, 5, 17, 40):
                with self.subTest(seed=seed, size=size):
                    random.seed(seed)
                    l1, l2 = cl.generate_lists(size)
                    self.assertEqual(
                        cl.find_common(l1, l2), cl.find_common_efficient(l1, l2)
                    )

    def test_agree_on_hand_picked_unique_cases(self):
        cases = [
            ([], []),
            ([1], [1]),
            ([1, 2, 3], [4, 5, 6]),
            ([-3, -2, -1], [-1, 0, 1]),
            (list(range(50)), list(range(25, 75))),
        ]
        for a, b in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(cl.find_common(a, b), cl.find_common_efficient(a, b))

    def test_disagree_when_duplicates_present(self):
        # Documents the behavioral inconsistency: pair-count vs distinct-count.
        a, b = [1, 1, 2], [1, 2, 2]
        self.assertEqual(cl.find_common(a, b), 4)
        self.assertEqual(cl.find_common_efficient(a, b), 2)

    def test_disagree_on_unhashable_inputs(self):
        a, b = [[1]], [[1]]
        self.assertEqual(cl.find_common(a, b), 1)
        with self.assertRaises(TypeError):
            cl.find_common_efficient(a, b)

    def test_disagree_on_empty_first_list_with_none_second(self):
        self.assertEqual(cl.find_common([], None), 0)
        with self.assertRaises(TypeError):
            cl.find_common_efficient([], None)


class TestMeasureTime(unittest.TestCase):
    EXPECTED_SIZES = [10, 100, 1000, 10000]

    def _run(self, lists=([1, 2, 3], [2, 3, 4]), perf_counter=None):
        """Run measure_time with a stubbed generate_lists so it finishes instantly."""
        buf = io.StringIO()
        with mock.patch.object(cl, "generate_lists", return_value=lists) as gen:
            if perf_counter is not None:
                with mock.patch.object(cl.time, "perf_counter", side_effect=perf_counter):
                    with redirect_stdout(buf):
                        result = cl.measure_time()
            else:
                with redirect_stdout(buf):
                    result = cl.measure_time()
        return result, buf.getvalue().splitlines(), gen

    def test_returns_none(self):
        result, _, _ = self._run()
        self.assertIsNone(result)

    def test_prints_header_plus_one_row_per_size(self):
        _, lines, _ = self._run()
        self.assertEqual(len(lines), 1 + len(self.EXPECTED_SIZES))

    def test_header_contains_column_titles(self):
        _, lines, _ = self._run()
        self.assertIn("List Size", lines[0])
        self.assertIn("find_common Time (s)", lines[0])

    @unittest.expectedFailure
    def test_header_spells_efficient_function_name_correctly(self):
        # BUG: header currently reads "find_common_efficiet" (missing 'n').
        _, lines, _ = self._run()
        self.assertIn("find_common_efficient Time (s)", lines[0])

    def test_rows_report_each_size_in_order(self):
        _, lines, _ = self._run()
        sizes_printed = [int(line[:10].strip()) for line in lines[1:]]
        self.assertEqual(sizes_printed, self.EXPECTED_SIZES)

    def test_generate_lists_called_once_per_size(self):
        _, _, gen = self._run()
        self.assertEqual(
            gen.call_args_list, [mock.call(s) for s in self.EXPECTED_SIZES]
        )

    def test_both_functions_timed_for_every_size(self):
        buf = io.StringIO()
        with mock.patch.object(cl, "generate_lists", return_value=([1, 2], [2, 3])), \
             mock.patch.object(cl, "find_common", return_value=1) as slow, \
             mock.patch.object(cl, "find_common_efficient", return_value=1) as fast, \
             redirect_stdout(buf):
            cl.measure_time()
        self.assertEqual(slow.call_count, len(self.EXPECTED_SIZES))
        self.assertEqual(fast.call_count, len(self.EXPECTED_SIZES))
        slow.assert_called_with([1, 2], [2, 3])
        fast.assert_called_with([1, 2], [2, 3])

    def test_times_are_computed_as_end_minus_start(self):
        # perf_counter yields 0, 0.5, 1.0, ... so every measured interval is 0.5 s.
        _, lines, _ = self._run(perf_counter=itertools.count(0, 0.5))
        for line in lines[1:]:
            self.assertEqual(line.count("0.500000"), 2, msg=line)

    def test_perf_counter_called_twice_per_function_per_size(self):
        counter = itertools.count(0, 1)
        calls = []

        def fake():
            value = next(counter)
            calls.append(value)
            return value

        self._run(perf_counter=fake)
        self.assertEqual(len(calls), 4 * len(self.EXPECTED_SIZES))

    def test_no_nan_values_printed_for_default_sizes(self):
        _, lines, _ = self._run()
        for line in lines[1:]:
            self.assertNotIn("nan", line.lower())

    def test_times_are_non_negative_with_real_clock(self):
        _, lines, _ = self._run()
        for line in lines[1:]:
            fields = line.split()
            self.assertGreaterEqual(float(fields[1]), 0.0)
            self.assertGreaterEqual(float(fields[2]), 0.0)

    def test_empty_generated_lists_do_not_crash(self):
        result, lines, _ = self._run(lists=([], []))
        self.assertIsNone(result)
        self.assertEqual(len(lines), 1 + len(self.EXPECTED_SIZES))

    def test_error_in_generate_lists_propagates(self):
        with mock.patch.object(cl, "generate_lists", side_effect=ValueError("boom")):
            with redirect_stdout(io.StringIO()):
                with self.assertRaises(ValueError):
                    cl.measure_time()

    def test_error_in_find_common_propagates(self):
        with mock.patch.object(cl, "generate_lists", return_value=([1], [1])), \
             mock.patch.object(cl, "find_common", side_effect=RuntimeError("fail")):
            with redirect_stdout(io.StringIO()):
                with self.assertRaises(RuntimeError):
                    cl.measure_time()


if __name__ == "__main__":
    unittest.main()