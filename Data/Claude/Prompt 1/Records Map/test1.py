# test_records.py
# Run with:  python -m unittest test_records -v
# NOTE: change the import below to match the module that holds LocalRecord / RecordsMap.
import math
import random
import unittest

from RecordsMap import LocalRecord, RecordsMap


class TestLocalRecordInit(unittest.TestCase):
    """Constructor behavior: rounding, defaults, invalid positions."""

    def test_defaults(self):
        r = LocalRecord((1, 2))
        self.assertIsNone(r.max)
        self.assertIsNone(r.min)
        self.assertEqual(r.precision, 0)

    def test_stored_max_min(self):
        r = LocalRecord((0, 0), max=10, min=-5)
        self.assertEqual(r.max, 10)
        self.assertEqual(r.min, -5)

    def test_position_rounded_to_nearest_integer_by_default(self):
        self.assertEqual(LocalRecord((1.4, 2.6)).pos, (1, 3))

    def test_position_is_tuple_even_if_list_given(self):
        r = LocalRecord([1.2, 3.8])
        self.assertIsInstance(r.pos, tuple)
        self.assertEqual(r.pos, (1, 4))

    def test_bankers_rounding_on_halves(self):
        self.assertEqual(LocalRecord((0.5, 1.5)).pos, (0, 2))
        self.assertEqual(LocalRecord((2.5, 3.5)).pos, (2, 4))
        self.assertEqual(LocalRecord((-0.5, -1.5)).pos, (0, -2))

    def test_custom_precision(self):
        r = LocalRecord((1.234, 5.678), precision=2)
        self.assertEqual(r.pos, (1.23, 5.68))
        self.assertEqual(r.precision, 2)

    def test_negative_precision(self):
        self.assertEqual(LocalRecord((1234, 5678), precision=-2).pos, (1200, 5700))

    def test_negative_coordinates(self):
        self.assertEqual(LocalRecord((-3.4, -7.6)).pos, (-3, -8))

    def test_negative_zero_equals_zero(self):
        self.assertEqual(LocalRecord((-0.4, 0.4)).pos, (0, 0))

    def test_integer_input_unchanged(self):
        self.assertEqual(LocalRecord((7, -9)).pos, (7, -9))

    def test_extra_coordinates_ignored(self):
        self.assertEqual(LocalRecord((1, 2, 3)).pos, (1, 2))

    def test_very_large_coordinates(self):
        self.assertEqual(LocalRecord((10**12, -10**12)).pos, (10**12, -10**12))

    def test_too_short_position_raises(self):
        with self.assertRaises(IndexError):
            LocalRecord((1,))
        with self.assertRaises(IndexError):
            LocalRecord(())

    def test_none_position_raises(self):
        with self.assertRaises(TypeError):
            LocalRecord(None)

    def test_non_numeric_position_raises(self):
        for bad in [("a", "b"), (1, "b"), (None, 1), ([], [])]:
            with self.subTest(pos=bad):
                with self.assertRaises(TypeError):
                    LocalRecord(bad)

    def test_non_integer_precision_raises(self):
        with self.assertRaises(TypeError):
            LocalRecord((1.5, 2.5), precision="2")


class TestLocalRecordAddReport(unittest.TestCase):
    """add_report must correctly maintain min and max."""

    def setUp(self):
        self.r = LocalRecord((0, 0))

    def test_first_report_sets_both(self):
        self.r.add_report(50)
        self.assertEqual((self.r.min, self.r.max), (50, 50))

    def test_new_maximum(self):
        self.r.add_report(50)
        self.r.add_report(80)
        self.assertEqual((self.r.min, self.r.max), (50, 80))

    def test_new_minimum(self):
        self.r.add_report(50)
        self.r.add_report(20)
        self.assertEqual((self.r.min, self.r.max), (20, 50))

    def test_value_between_min_and_max_changes_nothing(self):
        self.r.add_report(20)
        self.r.add_report(80)
        self.r.add_report(50)
        self.assertEqual((self.r.min, self.r.max), (20, 80))

    def test_equal_value_changes_nothing(self):
        self.r.add_report(50)
        self.r.add_report(50)
        self.assertEqual((self.r.min, self.r.max), (50, 50))

    def test_zero_temperature_is_not_treated_as_missing(self):
        # Guards against `if not self.max` style bugs: 0 is a valid reading.
        self.r.add_report(0)
        self.assertEqual((self.r.min, self.r.max), (0, 0))
        self.r.add_report(-5)
        self.assertEqual((self.r.min, self.r.max), (-5, 0))
        self.r.add_report(5)
        self.assertEqual((self.r.min, self.r.max), (-5, 5))

    def test_negative_temperatures(self):
        for t in (-10, -30, -20):
            self.r.add_report(t)
        self.assertEqual((self.r.min, self.r.max), (-30, -10))

    def test_float_temperatures(self):
        for t in (1.5, 1.25, 1.75):
            self.r.add_report(t)
        self.assertEqual((self.r.min, self.r.max), (1.25, 1.75))

    def test_mixed_int_and_float(self):
        self.r.add_report(10)
        self.r.add_report(10.5)
        self.r.add_report(9.5)
        self.assertEqual((self.r.min, self.r.max), (9.5, 10.5))

    def test_extreme_values(self):
        self.r.add_report(float("-inf"))
        self.r.add_report(float("inf"))
        self.assertEqual(self.r.min, float("-inf"))
        self.assertEqual(self.r.max, float("inf"))

    def test_only_max_preset_min_gets_filled(self):
        r = LocalRecord((0, 0), max=5)
        r.add_report(3)
        self.assertEqual((r.min, r.max), (3, 5))

    def test_only_min_preset_max_gets_filled(self):
        r = LocalRecord((0, 0), min=5)
        r.add_report(7)
        self.assertEqual((r.min, r.max), (5, 7))

    def test_many_reports(self):
        values = [3, 99, -4, 17, 0, 42, -4, 99]
        for v in values:
            self.r.add_report(v)
        self.assertEqual(self.r.min, min(values))
        self.assertEqual(self.r.max, max(values))

    def test_incomparable_type_raises_and_keeps_state(self):
        self.r.add_report(10)
        with self.assertRaises(TypeError):
            self.r.add_report("hot")
        self.assertEqual((self.r.min, self.r.max), (10, 10))

    def test_none_report_after_real_value_raises(self):
        self.r.add_report(10)
        with self.assertRaises(TypeError):
            self.r.add_report(None)
        self.assertEqual((self.r.min, self.r.max), (10, 10))


class TestLocalRecordEqualityHashRepr(unittest.TestCase):
    """__eq__, __hash__ and __repr__ depend only on position (repr also shows temps)."""

    def test_equal_when_same_position(self):
        self.assertEqual(LocalRecord((1, 2)), LocalRecord((1, 2)))

    def test_not_equal_when_different_position(self):
        self.assertNotEqual(LocalRecord((1, 2)), LocalRecord((2, 1)))
        self.assertNotEqual(LocalRecord((1, 2)), LocalRecord((1, 3)))

    def test_equality_ignores_temperatures(self):
        self.assertEqual(LocalRecord((1, 2), 10, 0), LocalRecord((1, 2), 99, -99))

    def test_equal_after_rounding(self):
        self.assertEqual(LocalRecord((1.2, 2.4)), LocalRecord((0.9, 1.6)))

    def test_float_and_int_positions_equal(self):
        a, b = LocalRecord((1.0, 2.0)), LocalRecord((1, 2))
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))

    def test_not_equal_to_other_types(self):
        r = LocalRecord((1, 2))
        self.assertNotEqual(r, (1, 2))
        self.assertNotEqual(r, None)
        self.assertNotEqual(r, "Record")
        self.assertNotEqual(r, 5)

    def test_equality_symmetric_and_reflexive(self):
        a, b = LocalRecord((4, 4)), LocalRecord((4, 4))
        self.assertEqual(a, a)
        self.assertTrue(a == b and b == a)

    def test_equal_objects_have_equal_hash(self):
        a, b = LocalRecord((3, 4), 1, 0), LocalRecord((3, 4), 9, 9)
        self.assertEqual(hash(a), hash(b))

    def test_hash_is_stable_after_add_report(self):
        r = LocalRecord((3, 4))
        before = hash(r)
        r.add_report(100)
        self.assertEqual(before, hash(r))

    def test_set_deduplicates_by_position(self):
        s = {LocalRecord((1, 1)), LocalRecord((1, 1), 5, 5), LocalRecord((2, 2))}
        self.assertEqual(len(s), 2)

    def test_usable_as_dict_key(self):
        d = {LocalRecord((1, 1)): "a"}
        self.assertEqual(d[LocalRecord((1, 1), 7, 7)], "a")

    def test_repr_without_temps(self):
        self.assertEqual(repr(LocalRecord((1, 2))), "Record(pos=(1, 2), max=None, min=None)")

    def test_repr_with_temps(self):
        self.assertEqual(repr(LocalRecord((1, 2), 5, 3)), "Record(pos=(1, 2), max=5, min=3)")

    def test_repr_reflects_updates(self):
        r = LocalRecord((0, 0))
        r.add_report(4)
        r.add_report(9)
        self.assertEqual(repr(r), "Record(pos=(0, 0), max=9, min=4)")


class TestRecordsMapInit(unittest.TestCase):
    def test_defaults(self):
        m = RecordsMap()
        self.assertEqual(m.capacity, 8)
        self.assertEqual(len(m), 0)
        self.assertEqual(len(m.table), 8)
        self.assertTrue(all(bucket == [] for bucket in m.table))

    def test_custom_capacity(self):
        m = RecordsMap(31)
        self.assertEqual(m.capacity, 31)
        self.assertEqual(len(m.table), 31)

    def test_buckets_are_independent_lists(self):
        m = RecordsMap(4)
        m.table[0].append("x")
        self.assertEqual(m.table[1], [])

    def test_zero_capacity_fails_on_use(self):
        m = RecordsMap(0)
        with self.assertRaises(ZeroDivisionError):
            m.add_report((0, 0), 1)

    def test_negative_capacity_fails_on_use(self):
        m = RecordsMap(-3)
        with self.assertRaises(IndexError):
            m.add_report((0, 0), 1)

    def test_non_integer_capacity_raises(self):
        with self.assertRaises(TypeError):
            RecordsMap(2.5)
        with self.assertRaises(TypeError):
            RecordsMap("8")


class TestRecordsMapBasicOperations(unittest.TestCase):
    def setUp(self):
        self.m = RecordsMap()

    def test_add_then_get_returns_min_max_in_that_order(self):
        self.m.add_report((1, 2), 70)
        self.assertEqual(self.m[(1, 2)], (70, 70))
        self.assertEqual(len(self.m), 1)

    def test_getitem_returns_tuple(self):
        self.m.add_report((0, 0), 5)
        self.assertIsInstance(self.m[(0, 0)], tuple)

    def test_update_existing_position(self):
        self.m.add_report((1, 2), 70)
        self.m.add_report((1, 2), 50)
        self.m.add_report((1, 2), 90)
        self.assertEqual(self.m[(1, 2)], (50, 90))
        self.assertEqual(len(self.m), 1)

    def test_same_temperature_twice(self):
        self.m.add_report((1, 2), 70)
        self.m.add_report((1, 2), 70)
        self.assertEqual(self.m[(1, 2)], (70, 70))
        self.assertEqual(len(self.m), 1)

    def test_distinct_positions_tracked_separately(self):
        self.m.add_report((0, 0), 10)
        self.m.add_report((0, 1), 20)
        self.m.add_report((1, 0), 30)
        self.assertEqual(len(self.m), 3)
        self.assertEqual(self.m[(0, 0)], (10, 10))
        self.assertEqual(self.m[(0, 1)], (20, 20))
        self.assertEqual(self.m[(1, 0)], (30, 30))

    def test_swapped_coordinates_are_different_positions(self):
        self.m.add_report((1, 2), 10)
        self.m.add_report((2, 1), 20)
        self.assertEqual(len(self.m), 2)
        self.assertEqual(self.m[(1, 2)], (10, 10))
        self.assertEqual(self.m[(2, 1)], (20, 20))

    def test_updating_one_position_does_not_touch_another(self):
        self.m.add_report((0, 0), 10)
        self.m.add_report((5, 5), 99)
        self.m.add_report((0, 0), 1)
        self.assertEqual(self.m[(5, 5)], (99, 99))

    def test_negative_coordinates(self):
        self.m.add_report((-3, -4), 12)
        self.assertEqual(self.m[(-3, -4)], (12, 12))
        self.assertIn((-3, -4), self.m)

    def test_origin(self):
        self.m.add_report((0, 0), 0)
        self.assertEqual(self.m[(0, 0)], (0, 0))

    def test_large_coordinates(self):
        self.m.add_report((10**9, -10**9), 5)
        self.assertEqual(self.m[(10**9, -10**9)], (5, 5))

    def test_negative_and_zero_temperatures(self):
        self.m.add_report((0, 0), -40)
        self.m.add_report((0, 0), 0)
        self.assertEqual(self.m[(0, 0)], (-40, 0))

    def test_mixed_int_float_temperatures(self):
        self.m.add_report((0, 0), 10)
        self.m.add_report((0, 0), 10.5)
        self.assertEqual(self.m[(0, 0)], (10, 10.5))

    def test_list_position_accepted(self):
        self.m.add_report([1, 2], 5)
        self.assertEqual(self.m[(1, 2)], (5, 5))
        self.assertIn([1, 2], self.m)

    def test_third_coordinate_ignored(self):
        self.m.add_report((1, 2, 3), 10)
        self.m.add_report((1, 2, 99), 20)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(1, 2)], (10, 20))

    def test_none_temperature_on_new_position(self):
        self.m.add_report((0, 0), None)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(0, 0)], (None, None))

    def test_none_then_real_temperature(self):
        self.m.add_report((0, 0), None)
        self.m.add_report((0, 0), 5)
        self.assertEqual(self.m[(0, 0)], (5, 5))

    def test_real_then_none_temperature_raises_and_keeps_state(self):
        self.m.add_report((0, 0), 5)
        with self.assertRaises(TypeError):
            self.m.add_report((0, 0), None)
        self.assertEqual(self.m[(0, 0)], (5, 5))
        self.assertEqual(len(self.m), 1)


class TestRecordsMapRoundingOfPositions(unittest.TestCase):
    def setUp(self):
        self.m = RecordsMap()

    def test_nearby_positions_merge(self):
        self.m.add_report((1.2, 3.4), 10)
        self.m.add_report((0.8, 3.1), 30)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(1, 3)], (10, 30))

    def test_lookup_with_unrounded_position(self):
        self.m.add_report((1, 3), 10)
        self.assertEqual(self.m[(1.49, 2.51)], (10, 10))
        self.assertIn((1.49, 2.51), self.m)

    def test_just_over_half_goes_to_next_cell(self):
        self.m.add_report((0.4, 0.4), 1)
        self.m.add_report((0.6, 0.6), 2)
        self.assertEqual(len(self.m), 2)
        self.assertEqual(self.m[(0, 0)], (1, 1))
        self.assertEqual(self.m[(1, 1)], (2, 2))

    def test_bankers_rounding_merges_half_cells(self):
        # 1.5 -> 2 and 2.5 -> 2 under round-half-to-even
        self.m.add_report((1.5, 1.5), 10)
        self.m.add_report((2.5, 2.5), 20)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(2, 2)], (10, 20))

    def test_half_values_around_zero_merge(self):
        self.m.add_report((0.5, 0.5), 1)
        self.m.add_report((-0.5, -0.5), 2)
        self.m.add_report((0, 0), 3)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(0, 0)], (1, 3))

    def test_negative_zero_and_zero_same_cell(self):
        self.m.add_report((-0.0, -0.0), 4)
        self.m.add_report((0.0, 0.0), 8)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(0, 0)], (4, 8))

    def test_float_and_int_query_equivalent(self):
        self.m.add_report((1, 2), 10)
        self.assertEqual(self.m[(1.0, 2.0)], (10, 10))


class TestRecordsMapContainsAndGetitem(unittest.TestCase):
    def setUp(self):
        self.m = RecordsMap()

    def test_contains_false_on_empty(self):
        self.assertNotIn((0, 0), self.m)

    def test_contains_true_and_false(self):
        self.m.add_report((1, 1), 5)
        self.assertIn((1, 1), self.m)
        self.assertNotIn((1, 2), self.m)
        self.assertNotIn((2, 1), self.m)

    def test_contains_does_not_change_size(self):
        self.m.add_report((1, 1), 5)
        _ = (9, 9) in self.m
        self.assertEqual(len(self.m), 1)

    def test_getitem_missing_raises_keyerror(self):
        with self.assertRaises(KeyError):
            self.m[(0, 0)]

    def test_getitem_missing_with_other_entries_raises_keyerror(self):
        self.m.add_report((0, 0), 1)
        with self.assertRaises(KeyError):
            self.m[(0, 1)]

    def test_getitem_does_not_create_entry(self):
        with self.assertRaises(KeyError):
            self.m[(3, 3)]
        self.assertEqual(len(self.m), 0)
        self.assertNotIn((3, 3), self.m)


class TestRecordsMapCollisions(unittest.TestCase):
    """Two distinct positions that land in the same bucket must stay independent."""

    def _colliding_positions(self, capacity):
        m = RecordsMap(capacity)
        buckets = {}
        for i in range(500):
            buckets.setdefault(m._hash((i, 0)), []).append((i, 0))
        for group in buckets.values():
            if len(group) >= 2:
                return group[0], group[1]
        self.fail("could not find colliding positions")

    def test_colliding_positions_are_independent(self):
        p, q = self._colliding_positions(8)
        m = RecordsMap(8)
        self.assertEqual(m._hash(p), m._hash(q))
        m.add_report(p, 10)
        m.add_report(q, 99)
        self.assertEqual(len(m), 2)
        self.assertEqual(m[p], (10, 10))
        self.assertEqual(m[q], (99, 99))
        m.add_report(p, 1)
        self.assertEqual(m[p], (1, 10))
        self.assertEqual(m[q], (99, 99))

    def test_missing_position_in_occupied_bucket(self):
        p, q = self._colliding_positions(8)
        m = RecordsMap(8)
        m.add_report(p, 10)
        self.assertNotIn(q, m)
        with self.assertRaises(KeyError):
            m[q]


class TestRecordsMapHashFunction(unittest.TestCase):
    def test_hash_in_range(self):
        m = RecordsMap(8)
        for pos in [(0, 0), (-5, 7), (10**9, -10**9), (-1.5, 2.5), (123456.7, -0.2)]:
            with self.subTest(pos=pos):
                self.assertTrue(0 <= m._hash(pos) < m.capacity)

    def test_hash_deterministic(self):
        m = RecordsMap(16)
        self.assertEqual(m._hash((3, 4)), m._hash((3, 4)))

    def test_positions_rounding_to_same_cell_hash_equally(self):
        m = RecordsMap(16)
        self.assertEqual(m._hash((1.2, 3.4)), m._hash((0.8, 3.1)))
        self.assertEqual(m._hash((1, 2)), m._hash((1.0, 2.0)))


class TestRecordsMapInvalidPositions(unittest.TestCase):
    def setUp(self):
        self.m = RecordsMap()

    def test_none_position(self):
        with self.assertRaises(TypeError):
            self.m.add_report(None, 1)
        with self.assertRaises(TypeError):
            self.m[None]
        with self.assertRaises(TypeError):
            None in self.m

    def test_too_short_position(self):
        for bad in [(1,), ()]:
            with self.subTest(pos=bad):
                with self.assertRaises(IndexError):
                    self.m.add_report(bad, 1)
                with self.assertRaises(IndexError):
                    self.m[bad]
                with self.assertRaises(IndexError):
                    bad in self.m

    def test_non_numeric_position(self):
        for bad in [("a", "b"), (1, "b"), (None, None)]:
            with self.subTest(pos=bad):
                with self.assertRaises(TypeError):
                    self.m.add_report(bad, 1)

    def test_nan_position(self):
        with self.assertRaises(ValueError):
            self.m.add_report((float("nan"), 0), 1)

    def test_infinite_position(self):
        with self.assertRaises(OverflowError):
            self.m.add_report((float("inf"), 0), 1)
        with self.assertRaises(OverflowError):
            self.m.add_report((0, float("-inf")), 1)

    def test_invalid_position_does_not_change_size(self):
        self.m.add_report((0, 0), 1)
        for bad in [None, (1,), ("a", "b"), (float("nan"), 0)]:
            try:
                self.m.add_report(bad, 5)
            except (TypeError, IndexError, ValueError, OverflowError):
                pass
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(0, 0)], (1, 1))


class TestRecordsMapResizing(unittest.TestCase):
    def test_no_rehash_below_threshold(self):
        m = RecordsMap(8)
        for i in range(5):  # 5/8 = 0.625
            m.add_report((i, 0), i)
        self.assertEqual(m.capacity, 8)
        self.assertEqual(len(m), 5)

    def test_rehash_when_threshold_exceeded(self):
        m = RecordsMap(8)
        for i in range(6):  # 6/8 = 0.75 > 0.7
            m.add_report((i, 0), i)
        self.assertEqual(m.capacity, 16)
        self.assertEqual(len(m), 6)
        self.assertEqual(len(m.table), 16)

    def test_exact_threshold_does_not_rehash(self):
        m = RecordsMap(10)
        for i in range(7):  # 7/10 == 0.7, not strictly greater
            m.add_report((i, i), i)
        self.assertEqual(m.capacity, 10)
        m.add_report((7, 7), 7)  # 8/10 > 0.7
        self.assertEqual(m.capacity, 20)
        self.assertEqual(len(m), 8)

    def test_updating_existing_position_never_grows_table(self):
        m = RecordsMap(8)
        for i in range(5):
            m.add_report((i, 0), i)
        for t in range(100):
            m.add_report((0, 0), t)
        self.assertEqual(m.capacity, 8)
        self.assertEqual(len(m), 5)

    def test_all_entries_survive_rehash(self):
        m = RecordsMap(8)
        for i in range(6):
            m.add_report((i, -i), 10 * i)
        for i in range(6):
            self.assertEqual(m[(i, -i)], (10 * i, 10 * i))
            self.assertIn((i, -i), m)

    def test_rehash_preserves_min_and_max(self):
        m = RecordsMap(8)
        m.add_report((0, 0), 10)
        m.add_report((0, 0), 20)
        m.add_report((0, 0), 15)
        m.add_report((9, 9), 5)  # single reading: min == max
        for i in range(1, 5):
            m.add_report((i, 0), i)  # pushes past the threshold
        self.assertGreater(m.capacity, 8)
        self.assertEqual(m[(0, 0)], (10, 20))
        self.assertEqual(m[(9, 9)], (5, 5))

    def test_rehash_preserves_negative_and_zero_extremes(self):
        m = RecordsMap(8)
        m.add_report((0, 0), -30)
        m.add_report((0, 0), 0)
        for i in range(1, 7):
            m.add_report((i, i), i)
        self.assertEqual(m[(0, 0)], (-30, 0))

    def test_size_not_double_counted_after_rehash(self):
        m = RecordsMap(8)
        for i in range(6):
            m.add_report((i, 0), 1)
            m.add_report((i, 0), 2)  # min != max for every record
        self.assertEqual(len(m), 6)
        self.assertEqual(sum(len(b) for b in m.table), 6)

    def test_updates_work_after_rehash(self):
        m = RecordsMap(8)
        for i in range(6):
            m.add_report((i, 0), 50)
        m.add_report((3, 0), 70)
        m.add_report((3, 0), 30)
        self.assertEqual(m[(3, 0)], (30, 70))
        self.assertEqual(len(m), 6)

    def test_capacity_one_grows_and_stays_correct(self):
        m = RecordsMap(1)
        for i in range(20):
            m.add_report((i, i), i)
        self.assertEqual(len(m), 20)
        for i in range(20):
            self.assertEqual(m[(i, i)], (i, i))

    def test_multiple_consecutive_rehashes(self):
        m = RecordsMap(2)
        for i in range(200):
            m.add_report((i, 2 * i), i)
        self.assertEqual(len(m), 200)
        self.assertGreaterEqual(m.capacity, 200 / 0.7 / 2)
        for i in range(200):
            self.assertEqual(m[(i, 2 * i)], (i, i))


class TestRecordsMapAgainstReferenceModel(unittest.TestCase):
    """Randomized comparison with a plain dict that applies the same rounding."""

    def test_random_workload(self):
        rng = random.Random(12345)
        m = RecordsMap()
        ref = {}
        for _ in range(2000):
            pos = (rng.uniform(-30, 30), rng.uniform(-30, 30))
            temp = rng.randint(-100, 100)
            m.add_report(pos, temp)
            key = (round(pos[0]), round(pos[1]))
            lo, hi = ref.get(key, (temp, temp))
            ref[key] = (min(lo, temp), max(hi, temp))

            # Load factor invariant holds after every insertion.
            self.assertLessEqual(len(m) / m.capacity, 0.7)

        self.assertEqual(len(m), len(ref))
        self.assertEqual(sum(len(b) for b in m.table), len(ref))
        for key, expected in ref.items():
            self.assertIn(key, m)
            self.assertEqual(m[key], expected)

        # No duplicate positions inside any bucket.
        for bucket in m.table:
            positions = [rec.pos for rec in bucket]
            self.assertEqual(len(positions), len(set(positions)))

        # Positions never inserted must be absent.
        self.assertNotIn((1000, 1000), m)
        self.assertNotIn((-1000, 5), m)


if __name__ == "__main__":
    unittest.main()