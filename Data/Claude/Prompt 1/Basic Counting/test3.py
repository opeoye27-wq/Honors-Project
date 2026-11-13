import io
import math
import random
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

# NOTE: change "common_lists" to the name of the module containing your program.
import basic_counting as m


class TestGenerateLists(unittest.TestCase):
    def test_returns_two_lists_of_requested_size(self):
        l1, l2 = m.generate_lists(10)
        self.assertIsInstance(l1, list)
        self.assertIsInstance(l2, list)
        self.assertEqual(len(l1), 10)
        self.assertEqual(len(l2), 10)

    def test_elements_unique_within_each_list(self):
        l1, l2 = m.generate_lists(500)
        self.assertEqual(len(set(l1)), 500)
        self.assertEqual(len(set(l2)), 500)

    def test_elements_within_expected_range(self):
        size = 200
        l1, l2 = m.generate_lists(size)
        for v in l1 + l2:
            self.assertGreaterEqual(v, 0)
            self.assertLess(v, size * 2)

    def test_elements_are_ints(self):
        l1, l2 = m.generate_lists(20)
        self.assertTrue(all(isinstance(v, int) for v in l1 + l2))

    def test_size_zero_returns_empty_lists(self):
        self.assertEqual(m.generate_lists(0), ([], []))

    def test_size_one(self):
        l1, l2 = m.generate_lists(1)
        self.assertEqual(len(l1), 1)
        self.assertEqual(len(l2), 1)
        self.assertIn(l1[0], (0, 1))
        self.assertIn(l2[0], (0, 1))

    def test_size_two_values_in_range(self):
        l1, l2 = m.generate_lists(2)
        self.assertTrue(set(l1) <= {0, 1, 2, 3})
        self.assertTrue(set(l2) <= {0, 1, 2, 3})
        self.assertEqual(len(set(l1)), 2)

    def test_same_seed_is_reproducible(self):
        random.seed(123)
        a = m.generate_lists(50)
        random.seed(123)
        b = m.generate_lists(50)
        self.assertEqual(a, b)

    def test_different_calls_produce_independent_lists(self):
        random.seed(1)
        l1, l2 = m.generate_lists(100)
        self.assertNotEqual(l1, l2)

    def test_overlap_bounded_by_size(self):
        l1, l2 = m.generate_lists(100)
        overlap = len(set(l1) & set(l2))
        self.assertGreaterEqual(overlap, 0)
        self.assertLessEqual(overlap, 100)

    def test_large_size(self):
        l1, l2 = m.generate_lists(50000)
        self.assertEqual(len(l1), 50000)
        self.assertEqual(len(l2), 50000)

    # ---- invalid inputs ----
    def test_negative_size_raises_value_error(self):
        with self.assertRaises(ValueError):
            m.generate_lists(-1)

    def test_large_negative_size_raises_value_error(self):
        with self.assertRaises(ValueError):
            m.generate_lists(-100)

    def test_float_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.generate_lists(5.5)

    def test_integer_valued_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.generate_lists(5.0)

    def test_string_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.generate_lists("5")

    def test_none_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.generate_lists(None)


class TestFindCommon(unittest.TestCase):
    def test_basic_overlap(self):
        self.assertEqual(m.find_common([1, 2, 3], [2, 3, 4]), 2)

    def test_no_overlap(self):
        self.assertEqual(m.find_common([1, 2, 3], [4, 5, 6]), 0)

    def test_identical_lists(self):
        self.assertEqual(m.find_common([1, 2, 3], [1, 2, 3]), 3)

    def test_order_independent(self):
        self.assertEqual(m.find_common([3, 1, 2], [2, 3, 1]), 3)

    def test_both_empty(self):
        self.assertEqual(m.find_common([], []), 0)

    def test_first_empty(self):
        self.assertEqual(m.find_common([], [1, 2]), 0)

    def test_second_empty(self):
        self.assertEqual(m.find_common([1, 2], []), 0)

    def test_single_element_match(self):
        self.assertEqual(m.find_common([5], [5]), 1)

    def test_single_element_no_match(self):
        self.assertEqual(m.find_common([5], [6]), 0)

    def test_negative_numbers_and_zero(self):
        self.assertEqual(m.find_common([-1, 0, 1], [-1, 0, 2]), 2)

    def test_symmetry(self):
        a, b = [1, 2, 3, 4], [3, 4, 5]
        self.assertEqual(m.find_common(a, b), m.find_common(b, a))

    def test_does_not_mutate_inputs(self):
        a, b = [1, 2, 3], [2, 3, 4]
        a_copy, b_copy = a[:], b[:]
        m.find_common(a, b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)

    def test_strings(self):
        self.assertEqual(m.find_common(["a", "b"], ["b", "c"]), 1)

    def test_string_inputs_as_iterables(self):
        self.assertEqual(m.find_common("abc", "bcd"), 2)

    def test_tuples_as_inputs(self):
        self.assertEqual(m.find_common((1, 2, 3), (3, 4)), 1)

    def test_mixed_types_no_false_match(self):
        self.assertEqual(m.find_common([1, "1"], ["1", 2]), 1)

    def test_numeric_equality_across_types(self):
        # 1 == 1.0 == True in Python
        self.assertEqual(m.find_common([1], [1.0]), 1)
        self.assertEqual(m.find_common([1], [True]), 1)

    def test_none_elements_match(self):
        self.assertEqual(m.find_common([None], [None]), 1)

    def test_unhashable_elements_supported(self):
        self.assertEqual(m.find_common([[1], [2]], [[1], [3]]), 1)

    def test_duplicates_count_every_matching_pair(self):
        # current behaviour: counts pairs, so 2 x 2 = 4
        self.assertEqual(m.find_common([1, 1], [1, 1]), 4)

    def test_duplicates_in_one_list_only(self):
        self.assertEqual(m.find_common([1, 1, 1], [1]), 3)

    def test_nan_same_object_not_equal_to_itself(self):
        nan = float("nan")
        self.assertEqual(m.find_common([nan], [nan]), 0)

    def test_generator_as_second_arg_is_exhausted_after_first_pass(self):
        # a generator can only be iterated once, so later items of list1 see nothing
        gen = (x for x in [1, 2, 3])
        self.assertEqual(m.find_common([1, 2, 3], gen), 1)

    def test_larger_known_case(self):
        a = list(range(0, 200))
        b = list(range(100, 300))
        self.assertEqual(m.find_common(a, b), 100)

    # ---- invalid inputs ----
    def test_none_first_arg_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.find_common(None, [1])

    def test_none_second_arg_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.find_common([1], None)

    def test_int_arg_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.find_common(5, [1])

    def test_empty_first_with_invalid_second_does_not_raise(self):
        # inner loop is never reached, so the invalid second arg goes unnoticed
        self.assertEqual(m.find_common([], None), 0)


class TestFindCommonEfficient(unittest.TestCase):
    def test_basic_overlap(self):
        self.assertEqual(m.find_common_efficient([1, 2, 3], [2, 3, 4]), 2)

    def test_no_overlap(self):
        self.assertEqual(m.find_common_efficient([1, 2, 3], [4, 5, 6]), 0)

    def test_identical_lists(self):
        self.assertEqual(m.find_common_efficient([1, 2, 3], [1, 2, 3]), 3)

    def test_both_empty(self):
        self.assertEqual(m.find_common_efficient([], []), 0)

    def test_first_empty(self):
        self.assertEqual(m.find_common_efficient([], [1]), 0)

    def test_second_empty(self):
        self.assertEqual(m.find_common_efficient([1], []), 0)

    def test_single_element(self):
        self.assertEqual(m.find_common_efficient([7], [7]), 1)

    def test_symmetry(self):
        a, b = [1, 2, 3, 4], [3, 4, 5]
        self.assertEqual(m.find_common_efficient(a, b), m.find_common_efficient(b, a))

    def test_negative_numbers_and_zero(self):
        self.assertEqual(m.find_common_efficient([-1, 0, 1], [-1, 0, 2]), 2)

    def test_does_not_mutate_inputs(self):
        a, b = [1, 2, 3], [2, 3, 4]
        a_copy, b_copy = a[:], b[:]
        m.find_common_efficient(a, b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)

    def test_strings(self):
        self.assertEqual(m.find_common_efficient(["a", "b"], ["b", "c"]), 1)

    def test_string_inputs_as_iterables(self):
        self.assertEqual(m.find_common_efficient("abc", "bcd"), 2)

    def test_tuples_as_inputs(self):
        self.assertEqual(m.find_common_efficient((1, 2, 3), (3, 4)), 1)

    def test_numeric_equality_across_types(self):
        self.assertEqual(m.find_common_efficient([1], [1.0]), 1)
        self.assertEqual(m.find_common_efficient([1], [True]), 1)

    def test_none_elements_match(self):
        self.assertEqual(m.find_common_efficient([None], [None]), 1)

    def test_duplicates_counted_once(self):
        # current behaviour: counts distinct shared values
        self.assertEqual(m.find_common_efficient([1, 1], [1, 1]), 1)

    def test_duplicates_in_one_list_only(self):
        self.assertEqual(m.find_common_efficient([1, 1, 1], [1]), 1)

    def test_generator_inputs_work(self):
        self.assertEqual(
            m.find_common_efficient((x for x in [1, 2, 3]), (x for x in [3, 4])), 1
        )

    def test_large_input_is_fast_and_correct(self):
        a = list(range(0, 200000))
        b = list(range(100000, 300000))
        self.assertEqual(m.find_common_efficient(a, b), 100000)

    # ---- invalid inputs ----
    def test_none_first_arg_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.find_common_efficient(None, [1])

    def test_none_second_arg_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.find_common_efficient([1], None)

    def test_int_arg_raises_type_error(self):
        with self.assertRaises(TypeError):
            m.find_common_efficient(5, [1])

    def test_empty_first_with_invalid_second_raises_type_error(self):
        self.assertRaises(TypeError, m.find_common_efficient, [], None)

    def test_unhashable_elements_raise_type_error(self):
        with self.assertRaises(TypeError):
            m.find_common_efficient([[1]], [[1]])


class TestImplementationsAgree(unittest.TestCase):
    """Cross-checks between the naive and efficient versions."""

    def test_agree_on_unique_inputs(self):
        cases = [
            ([], []),
            ([1], [1]),
            ([1, 2, 3], [4, 5, 6]),
            ([1, 2, 3], [3, 2, 1]),
            (list(range(50)), list(range(25, 75))),
        ]
        for a, b in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(m.find_common(a, b), m.find_common_efficient(a, b))

    def test_agree_on_generated_lists(self):
        for size in (0, 1, 2, 10, 100, 500):
            for seed in range(5):
                with self.subTest(size=size, seed=seed):
                    random.seed(seed)
                    a, b = m.generate_lists(size)
                    self.assertEqual(
                        m.find_common(a, b), m.find_common_efficient(a, b)
                    )

    def test_agree_on_random_unique_inputs(self):
        rng = random.Random(42)
        for _ in range(50):
            a = rng.sample(range(100), rng.randint(0, 50))
            b = rng.sample(range(100), rng.randint(0, 50))
            with self.subTest(a=a, b=b):
                self.assertEqual(m.find_common(a, b), m.find_common_efficient(a, b))

    # The next tests expose a real inconsistency: the two functions give
    # different answers once duplicates (or NaN / unhashables) are involved.
    # They are expected to FAIL against the current implementation.
    def test_agree_when_duplicates_present(self):
        self.assertEqual(
            m.find_common([1, 1], [1, 1]), m.find_common_efficient([1, 1], [1, 1])
        )

    def test_agree_on_nan_same_object(self):
        nan = float("nan")
        self.assertEqual(
            m.find_common([nan], [nan]), m.find_common_efficient([nan], [nan])
        )

    def test_agree_on_unhashable_elements(self):
        self.assertEqual(
            m.find_common([[1]], [[1]]), m.find_common_efficient([[1]], [[1]])
        )


class TestMeasureTime(unittest.TestCase):
    def _run(self, perf_values=None):
        buf = io.StringIO()
        if perf_values is None:
            perf_values = []
            for k in range(4):
                base = 10.0 * k
                perf_values += [base, base + 1.0, base + 1.0, base + 1.5]
        with patch.object(m.time, "perf_counter", side_effect=perf_values):
            with redirect_stdout(buf):
                result = m.measure_time()
        return result, buf.getvalue()

    def test_returns_none(self):
        result, _ = self._run()
        self.assertIsNone(result)

    def test_prints_header_and_four_rows(self):
        _, out = self._run()
        self.assertEqual(len(out.strip().splitlines()), 5)

    def test_header_labels(self):
        _, out = self._run()
        header = out.splitlines()[0]
        self.assertIn("List Size", header)
        self.assertIn("find_common Time (s)", header)

    def test_header_has_correct_function_name_spelling(self):
        # Exposes the typo "find_common_efficiet" in the header.
        _, out = self._run()
        self.assertIn("find_common_efficient Time (s)", out.splitlines()[0])

    def test_rows_report_each_size_in_order(self):
        _, out = self._run()
        sizes = [int(line.split()[0]) for line in out.splitlines()[1:]]
        self.assertEqual(sizes, [10, 100, 1000, 10000])

    def test_rows_report_measured_times(self):
        _, out = self._run()
        for line in out.splitlines()[1:]:
            parts = line.split()
            self.assertAlmostEqual(float(parts[1]), 1.0, places=5)
            self.assertAlmostEqual(float(parts[2]), 0.5, places=5)

    def test_no_nan_for_default_sizes(self):
        _, out = self._run()
        self.assertNotIn("nan", out.lower())

    def test_generate_lists_called_once_per_size(self):
        with patch.object(m, "generate_lists", wraps=m.generate_lists) as spy:
            self._run()
        self.assertEqual([c.args[0] for c in spy.call_args_list], [10, 100, 1000, 10000])

    def test_both_functions_called_for_each_size(self):
        with patch.object(m, "find_common", wraps=m.find_common) as slow, \
             patch.object(m, "find_common_efficient", wraps=m.find_common_efficient) as fast:
            self._run()
        self.assertEqual(slow.call_count, 4)
        self.assertEqual(fast.call_count, 4)

    def test_times_are_non_negative_with_real_clock(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.measure_time()
        for line in buf.getvalue().splitlines()[1:]:
            parts = line.split()
            self.assertFalse(math.isnan(float(parts[1])))
            self.assertGreaterEqual(float(parts[1]), 0.0)
            self.assertGreaterEqual(float(parts[2]), 0.0)

    def test_efficient_not_slower_than_naive_at_largest_size(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.measure_time()
        last = buf.getvalue().splitlines()[-1].split()
        self.assertLessEqual(float(last[2]), float(last[1]))


class TestModuleImport(unittest.TestCase):
    def test_import_does_not_run_measure_time(self):
        import importlib

        buf = io.StringIO()
        with redirect_stdout(buf):
            importlib.reload(m)
        self.assertEqual(buf.getvalue(), "")


if __name__ == "__main__":
    unittest.main()