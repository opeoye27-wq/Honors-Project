
import contextlib
import importlib
import io
import random
import unittest
from unittest import mock

# Change this to the name of the module (file name without .py) that holds the program under test.
MODULE_NAME = "basic_counting"
sol = importlib.import_module(MODULE_NAME)


def run_and_capture(func, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = func(*args, **kwargs)
    return result, buf.getvalue()


# --------------------------------------------------------------------------
# generate_lists
# --------------------------------------------------------------------------
class TestGenerateLists(unittest.TestCase):

    def test_returns_tuple_of_two_lists(self):
        result = sol.generate_lists(10)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[1], list)

    def test_lengths_match_size(self):
        for size in (0, 1, 2, 10, 100, 1000):
            with self.subTest(size=size):
                l1, l2 = sol.generate_lists(size)
                self.assertEqual(len(l1), size)
                self.assertEqual(len(l2), size)

    def test_elements_unique_within_each_list(self):
        for size in (1, 2, 10, 500):
            with self.subTest(size=size):
                l1, l2 = sol.generate_lists(size)
                self.assertEqual(len(set(l1)), size)
                self.assertEqual(len(set(l2)), size)

    def test_elements_within_expected_range(self):
        for size in (1, 5, 100):
            with self.subTest(size=size):
                l1, l2 = sol.generate_lists(size)
                for v in l1 + l2:
                    self.assertIsInstance(v, int)
                    self.assertGreaterEqual(v, 0)
                    self.assertLess(v, size * 2)

    def test_size_zero_returns_empty_lists(self):
        self.assertEqual(sol.generate_lists(0), ([], []))

    def test_size_one_values_are_zero_or_one(self):
        for _ in range(50):
            l1, l2 = sol.generate_lists(1)
            self.assertIn(l1[0], (0, 1))
            self.assertIn(l2[0], (0, 1))

    def test_same_seed_gives_reproducible_output(self):
        random.seed(1234)
        a = sol.generate_lists(50)
        random.seed(1234)
        b = sol.generate_lists(50)
        self.assertEqual(a, b)

    def test_different_calls_give_different_lists(self):
        a = sol.generate_lists(200)
        b = sol.generate_lists(200)
        self.assertNotEqual(a, b)

    def test_two_lists_are_independent_samples(self):
        l1, l2 = sol.generate_lists(200)
        self.assertNotEqual(l1, l2)

    def test_lists_are_distinct_objects(self):
        l1, l2 = sol.generate_lists(5)
        self.assertIsNot(l1, l2)

    def test_negative_size_raises_value_error(self):
        with self.assertRaises(ValueError):
            sol.generate_lists(-1)

    def test_float_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            sol.generate_lists(3.5)

    def test_string_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            sol.generate_lists("10")

    def test_none_size_raises_type_error(self):
        with self.assertRaises(TypeError):
            sol.generate_lists(None)

    def test_missing_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            sol.generate_lists()


# --------------------------------------------------------------------------
# find_common (O(n^2) version)
# --------------------------------------------------------------------------
class TestFindCommon(unittest.TestCase):

    def test_no_common_elements(self):
        self.assertEqual(sol.find_common([1, 2, 3], [4, 5, 6]), 0)

    def test_some_common_elements(self):
        self.assertEqual(sol.find_common([1, 2, 3, 4], [3, 4, 5, 6]), 2)

    def test_all_common_elements(self):
        self.assertEqual(sol.find_common([1, 2, 3], [3, 2, 1]), 3)

    def test_identical_lists(self):
        self.assertEqual(sol.find_common([7, 8, 9], [7, 8, 9]), 3)

    def test_both_empty(self):
        self.assertEqual(sol.find_common([], []), 0)

    def test_first_empty(self):
        self.assertEqual(sol.find_common([], [1, 2, 3]), 0)

    def test_second_empty(self):
        self.assertEqual(sol.find_common([1, 2, 3], []), 0)

    def test_single_element_match(self):
        self.assertEqual(sol.find_common([5], [5]), 1)

    def test_single_element_no_match(self):
        self.assertEqual(sol.find_common([5], [6]), 0)

    def test_different_lengths(self):
        self.assertEqual(sol.find_common([1], [1, 2, 3, 4, 5]), 1)
        self.assertEqual(sol.find_common([1, 2, 3, 4, 5], [5]), 1)

    def test_symmetry(self):
        a, b = [1, 2, 3, 10, 20], [2, 20, 30, 40]
        self.assertEqual(sol.find_common(a, b), sol.find_common(b, a))

    def test_negative_numbers_and_zero(self):
        self.assertEqual(sol.find_common([-3, -2, 0, 5], [0, -2, 9]), 2)

    def test_large_values(self):
        big = 10 ** 20
        self.assertEqual(sol.find_common([big, 1], [big, 2]), 1)

    def test_strings(self):
        self.assertEqual(sol.find_common(["a", "b", "c"], ["c", "d", "a"]), 2)

    def test_case_sensitive_strings(self):
        self.assertEqual(sol.find_common(["A"], ["a"]), 0)

    def test_tuples(self):
        self.assertEqual(sol.find_common([(1, 2), (3, 4)], [(3, 4), (5, 6)]), 1)

    def test_int_and_float_equal_values_match(self):
        self.assertEqual(sol.find_common([1], [1.0]), 1)

    def test_bool_and_int_equal_values_match(self):
        self.assertEqual(sol.find_common([True], [1]), 1)

    def test_none_elements(self):
        self.assertEqual(sol.find_common([None, 1], [None, 2]), 1)

    def test_string_vs_int_not_equal(self):
        self.assertEqual(sol.find_common(["1"], [1]), 0)

    def test_unhashable_elements_supported(self):
        self.assertEqual(sol.find_common([[1], [2]], [[1], [3]]), 1)

    def test_strings_as_iterables(self):
        self.assertEqual(sol.find_common("abc", "bcd"), 2)

    def test_inputs_not_mutated(self):
        a, b = [1, 2, 3], [3, 4, 5]
        a_copy, b_copy = list(a), list(b)
        sol.find_common(a, b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)

    def test_returns_int(self):
        self.assertIsInstance(sol.find_common([1], [1]), int)

    def test_duplicates_count_each_matching_pair(self):
        # Documents current behavior: counts matching PAIRS, so duplicates multiply.
        self.assertEqual(sol.find_common([1, 1], [1, 1]), 4)
        self.assertEqual(sol.find_common([1, 1], [1]), 2)

    def test_single_use_iterator_as_second_argument(self):
        # BUG EXPOSURE: a one-shot iterator is exhausted after the first outer
        # iteration, so later elements of list1 are never compared.
        self.assertEqual(sol.find_common([1, 2, 3], iter([1, 2, 3])), 3)

    def test_nan_same_object(self):
        # BUG EXPOSURE: nan != nan, so the nested loop never counts it,
        # while set intersection uses identity first and does count it.
        nan = float("nan")
        self.assertEqual(sol.find_common([nan], [nan]), 1)

    def test_none_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            sol.find_common(None, [1])
        with self.assertRaises(TypeError):
            sol.find_common([1], None)

    def test_non_iterable_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            sol.find_common(5, [1])
        with self.assertRaises(TypeError):
            sol.find_common([1], 5)

    def test_missing_arguments_raise_type_error(self):
        with self.assertRaises(TypeError):
            sol.find_common([1])


# --------------------------------------------------------------------------
# find_common_efficient (set-based version)
# --------------------------------------------------------------------------
class TestFindCommonEfficient(unittest.TestCase):

    def test_no_common_elements(self):
        self.assertEqual(sol.find_common_efficient([1, 2, 3], [4, 5, 6]), 0)

    def test_some_common_elements(self):
        self.assertEqual(sol.find_common_efficient([1, 2, 3, 4], [3, 4, 5, 6]), 2)

    def test_all_common_elements(self):
        self.assertEqual(sol.find_common_efficient([1, 2, 3], [3, 2, 1]), 3)

    def test_both_empty(self):
        self.assertEqual(sol.find_common_efficient([], []), 0)

    def test_first_empty(self):
        self.assertEqual(sol.find_common_efficient([], [1, 2]), 0)

    def test_second_empty(self):
        self.assertEqual(sol.find_common_efficient([1, 2], []), 0)

    def test_single_element(self):
        self.assertEqual(sol.find_common_efficient([5], [5]), 1)
        self.assertEqual(sol.find_common_efficient([5], [6]), 0)

    def test_symmetry(self):
        a, b = [1, 2, 3, 10, 20], [2, 20, 30, 40]
        self.assertEqual(sol.find_common_efficient(a, b),
                         sol.find_common_efficient(b, a))

    def test_negative_numbers_and_zero(self):
        self.assertEqual(sol.find_common_efficient([-3, -2, 0, 5], [0, -2, 9]), 2)

    def test_strings(self):
        self.assertEqual(sol.find_common_efficient(["a", "b"], ["b", "c"]), 1)

    def test_tuples(self):
        self.assertEqual(
            sol.find_common_efficient([(1, 2), (3, 4)], [(3, 4), (5, 6)]), 1)

    def test_int_and_float_equal_values_match(self):
        self.assertEqual(sol.find_common_efficient([1], [1.0]), 1)

    def test_none_elements(self):
        self.assertEqual(sol.find_common_efficient([None, 1], [None, 2]), 1)

    def test_strings_as_iterables(self):
        self.assertEqual(sol.find_common_efficient("abc", "bcd"), 2)

    def test_accepts_tuples_sets_and_generators(self):
        self.assertEqual(sol.find_common_efficient((1, 2, 3), {2, 3, 4}), 2)
        self.assertEqual(
            sol.find_common_efficient((x for x in range(5)),
                                      (x for x in range(3, 8))), 2)

    def test_inputs_not_mutated(self):
        a, b = [1, 2, 2, 3], [3, 4, 4]
        a_copy, b_copy = list(a), list(b)
        sol.find_common_efficient(a, b)
        self.assertEqual(a, a_copy)
        self.assertEqual(b, b_copy)

    def test_returns_int(self):
        self.assertIsInstance(sol.find_common_efficient([1], [1]), int)

    def test_duplicates_counted_once(self):
        # Documents current behavior: counts DISTINCT shared values.
        self.assertEqual(sol.find_common_efficient([1, 1, 1], [1, 1]), 1)

    def test_unhashable_elements_raise_type_error(self):
        # Documents limitation: lists/dicts cannot be put in a set.
        with self.assertRaises(TypeError):
            sol.find_common_efficient([[1], [2]], [[1]])

    def test_none_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            sol.find_common_efficient(None, [1])
        with self.assertRaises(TypeError):
            sol.find_common_efficient([1], None)

    def test_non_iterable_argument_raises_type_error(self):
        with self.assertRaises(TypeError):
            sol.find_common_efficient(5, [1])

    def test_missing_arguments_raise_type_error(self):
        with self.assertRaises(TypeError):
            sol.find_common_efficient([1])


# --------------------------------------------------------------------------
# Consistency between the two implementations
# --------------------------------------------------------------------------
class TestImplementationsAgree(unittest.TestCase):

    def test_agree_on_unique_inputs_from_generate_lists(self):
        for size in (0, 1, 2, 10, 50, 200):
            with self.subTest(size=size):
                l1, l2 = sol.generate_lists(size)
                expected = len(set(l1) & set(l2))
                self.assertEqual(sol.find_common(l1, l2), expected)
                self.assertEqual(sol.find_common_efficient(l1, l2), expected)

    def test_agree_on_random_unique_inputs(self):
        rng = random.Random(99)
        for _ in range(100):
            a = rng.sample(range(60), rng.randint(0, 30))
            b = rng.sample(range(60), rng.randint(0, 30))
            self.assertEqual(sol.find_common(a, b),
                             sol.find_common_efficient(a, b))

    def test_disjoint_ranges_agree(self):
        a, b = list(range(0, 100)), list(range(100, 200))
        self.assertEqual(sol.find_common(a, b), 0)
        self.assertEqual(sol.find_common_efficient(a, b), 0)

    def test_identical_large_lists_agree(self):
        a = list(range(300))
        self.assertEqual(sol.find_common(a, a), 300)
        self.assertEqual(sol.find_common_efficient(a, a), 300)

    def test_agree_when_duplicates_present(self):
        # BUG EXPOSURE: find_common counts matching pairs (2 here) while
        # find_common_efficient counts distinct shared values (1 here).
        a, b = [1, 1], [1]
        self.assertEqual(sol.find_common(a, b), sol.find_common_efficient(a, b))

    def test_agree_on_duplicate_heavy_inputs(self):
        # BUG EXPOSURE: same discrepancy with larger multiplicities.
        a, b = [1, 1, 2, 2, 2], [2, 2, 3]
        self.assertEqual(sol.find_common(a, b), sol.find_common_efficient(a, b))

    def test_agree_on_nan(self):
        # BUG EXPOSURE: identity vs. equality semantics differ for NaN.
        nan = float("nan")
        self.assertEqual(sol.find_common([nan], [nan]),
                         sol.find_common_efficient([nan], [nan]))

    def test_agree_on_unhashable_inputs(self):
        # BUG EXPOSURE: one works, the other raises TypeError.
        a, b = [[1], [2]], [[1]]
        self.assertEqual(sol.find_common(a, b), sol.find_common_efficient(a, b))


# --------------------------------------------------------------------------
# measure_time
# --------------------------------------------------------------------------
class TestMeasureTime(unittest.TestCase):

    EXPECTED_SIZES = [10, 100, 1000, 10000]

    def _run_with_mocks(self, perf_values=None):
        """Run measure_time with the heavy functions mocked out so it is fast
        and deterministic."""
        if perf_values is None:
            # Per size: find_common takes 0.25 s, find_common_efficient 0.125 s.
            perf_values = [0.0, 0.25, 0.0, 0.125] * len(self.EXPECTED_SIZES)

        gen = mock.Mock(side_effect=lambda n: (list(range(n)), list(range(n))))
        fc = mock.Mock(return_value=0)
        fce = mock.Mock(return_value=0)
        pc = mock.Mock(side_effect=perf_values)

        with mock.patch.object(sol, "generate_lists", gen), \
             mock.patch.object(sol, "find_common", fc), \
             mock.patch.object(sol, "find_common_efficient", fce), \
             mock.patch.object(sol.time, "perf_counter", pc):
            result, out = run_and_capture(sol.measure_time)
        return result, out, gen, fc, fce, pc

    def test_returns_none(self):
        result, _, _, _, _, _ = self._run_with_mocks()
        self.assertIsNone(result)

    def test_generate_lists_called_for_each_size_in_order(self):
        _, _, gen, _, _, _ = self._run_with_mocks()
        self.assertEqual([c.args[0] for c in gen.call_args_list],
                         self.EXPECTED_SIZES)

    def test_both_functions_called_once_per_size(self):
        _, _, _, fc, fce, _ = self._run_with_mocks()
        self.assertEqual(fc.call_count, len(self.EXPECTED_SIZES))
        self.assertEqual(fce.call_count, len(self.EXPECTED_SIZES))

    def test_both_functions_receive_generated_lists(self):
        _, _, _, fc, fce, _ = self._run_with_mocks()
        for call, size in zip(fc.call_args_list, self.EXPECTED_SIZES):
            self.assertEqual(len(call.args[0]), size)
            self.assertEqual(len(call.args[1]), size)
        for call, size in zip(fce.call_args_list, self.EXPECTED_SIZES):
            self.assertEqual(len(call.args[0]), size)
            self.assertEqual(len(call.args[1]), size)

    def test_perf_counter_called_twice_per_timing(self):
        _, _, _, _, _, pc = self._run_with_mocks()
        self.assertEqual(pc.call_count, 4 * len(self.EXPECTED_SIZES))

    def test_output_has_header_plus_one_row_per_size(self):
        _, out, _, _, _, _ = self._run_with_mocks()
        lines = out.strip("\n").split("\n")
        self.assertEqual(len(lines), 1 + len(self.EXPECTED_SIZES))

    def test_header_contents(self):
        _, out, _, _, _, _ = self._run_with_mocks()
        header = out.split("\n")[0]
        self.assertIn("List Size", header)
        self.assertIn("find_common Time (s)", header)

    def test_header_spells_function_name_correctly(self):
        # BUG EXPOSURE: header currently reads "find_common_efficiet" (typo).
        _, out, _, _, _, _ = self._run_with_mocks()
        self.assertIn("find_common_efficient", out.split("\n")[0])

    def test_rows_start_with_expected_sizes_in_order(self):
        _, out, _, _, _, _ = self._run_with_mocks()
        rows = out.strip("\n").split("\n")[1:]
        for row, size in zip(rows, self.EXPECTED_SIZES):
            self.assertEqual(row.split()[0], str(size))

    def test_rows_report_measured_times(self):
        _, out, _, _, _, _ = self._run_with_mocks()
        rows = out.strip("\n").split("\n")[1:]
        for row in rows:
            cols = row.split()
            self.assertEqual(len(cols), 3)
            self.assertAlmostEqual(float(cols[1]), 0.25, places=6)
            self.assertAlmostEqual(float(cols[2]), 0.125, places=6)

    def test_times_are_non_negative_with_real_timer(self):
        # Mock only the expensive functions; use the real clock.
        gen = mock.Mock(side_effect=lambda n: ([1], [1]))
        with mock.patch.object(sol, "generate_lists", gen), \
             mock.patch.object(sol, "find_common", mock.Mock(return_value=0)), \
             mock.patch.object(sol, "find_common_efficient",
                               mock.Mock(return_value=0)):
            _, out = run_and_capture(sol.measure_time)
        for row in out.strip("\n").split("\n")[1:]:
            cols = row.split()
            self.assertGreaterEqual(float(cols[1]), 0.0)
            self.assertGreaterEqual(float(cols[2]), 0.0)

    def test_exception_in_find_common_propagates(self):
        gen = mock.Mock(side_effect=lambda n: ([1], [1]))
        with mock.patch.object(sol, "generate_lists", gen), \
             mock.patch.object(sol, "find_common",
                               mock.Mock(side_effect=RuntimeError("boom"))), \
             mock.patch.object(sol, "find_common_efficient",
                               mock.Mock(return_value=0)):
            with self.assertRaises(RuntimeError):
                run_and_capture(sol.measure_time)

    def test_exception_in_generate_lists_propagates(self):
        with mock.patch.object(sol, "generate_lists",
                               mock.Mock(side_effect=ValueError("bad"))):
            with self.assertRaises(ValueError):
                run_and_capture(sol.measure_time)

    def test_importing_module_produces_no_output(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            importlib.reload(sol)
        self.assertEqual(buf.getvalue(), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
