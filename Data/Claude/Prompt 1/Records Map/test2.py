import math
import unittest

# Change this import to match the module name your program is saved under.

from RecordsMap import LocalRecord, RecordsMap


class TestLocalRecordInit(unittest.TestCase):
    """Tests for LocalRecord.__init__ (position rounding and defaults)."""

    def test_defaults(self):
        r = LocalRecord((1, 2))
        self.assertEqual(r.pos, (1, 2))
        self.assertIsNone(r.max)
        self.assertIsNone(r.min)
        self.assertEqual(r.precision, 0)

    def test_explicit_max_min_stored(self):
        r = LocalRecord((0, 0), max=30, min=-5)
        self.assertEqual(r.max, 30)
        self.assertEqual(r.min, -5)

    def test_rounds_to_default_precision(self):
        r = LocalRecord((1.4, 2.6))
        self.assertEqual(r.pos, (1, 3))

    def test_rounds_to_given_precision(self):
        r = LocalRecord((1.26, 2.34), precision=1)
        self.assertEqual(r.pos, (1.3, 2.3))

    def test_negative_precision_rounds_to_tens(self):
        r = LocalRecord((14, 26), precision=-1)
        self.assertEqual(r.pos, (10, 30))

    def test_bankers_rounding_at_half(self):
        # Python rounds .5 to the nearest even integer
        self.assertEqual(LocalRecord((0.5, 1.5)).pos, (0, 2))
        self.assertEqual(LocalRecord((2.5, 3.5)).pos, (2, 4))

    def test_negative_coordinates(self):
        self.assertEqual(LocalRecord((-1.6, -2.4)).pos, (-2, -2))

    def test_negative_half_rounds_to_zero(self):
        self.assertEqual(LocalRecord((-0.5, -0.5)).pos, (0, 0))

    def test_pos_is_tuple(self):
        self.assertIsInstance(LocalRecord([1.2, 3.4]).pos, tuple)

    def test_extra_coordinates_ignored(self):
        self.assertEqual(LocalRecord((1, 2, 3)).pos, (1, 2))

    def test_large_coordinates(self):
        self.assertEqual(LocalRecord((10**15, -10**15)).pos, (10**15, -10**15))

    def test_zero_temperatures_not_treated_as_missing(self):
        r = LocalRecord((0, 0), max=0, min=0)
        self.assertEqual(r.max, 0)
        self.assertEqual(r.min, 0)

    # invalid inputs
    def test_none_pos_raises(self):
        with self.assertRaises(TypeError):
            LocalRecord(None)

    def test_scalar_pos_raises(self):
        with self.assertRaises(TypeError):
            LocalRecord(5)

    def test_short_pos_raises(self):
        with self.assertRaises(IndexError):
            LocalRecord((1,))

    def test_empty_pos_raises(self):
        with self.assertRaises(IndexError):
            LocalRecord(())

    def test_string_coordinates_raise(self):
        with self.assertRaises(TypeError):
            LocalRecord(("a", "b"))

    def test_non_integer_precision_raises(self):
        with self.assertRaises(TypeError):
            LocalRecord((1.5, 2.5), precision="1")


class TestLocalRecordAddReport(unittest.TestCase):
    """Tests for LocalRecord.add_report (min/max updating)."""

    def test_first_report_sets_both(self):
        r = LocalRecord((0, 0))
        r.add_report(10)
        self.assertEqual((r.min, r.max), (10, 10))

    def test_higher_temp_updates_max_only(self):
        r = LocalRecord((0, 0))
        r.add_report(10)
        r.add_report(20)
        self.assertEqual((r.min, r.max), (10, 20))

    def test_lower_temp_updates_min_only(self):
        r = LocalRecord((0, 0))
        r.add_report(10)
        r.add_report(-3)
        self.assertEqual((r.min, r.max), (-3, 10))

    def test_middle_temp_changes_nothing(self):
        r = LocalRecord((0, 0))
        r.add_report(0)
        r.add_report(10)
        r.add_report(5)
        self.assertEqual((r.min, r.max), (0, 10))

    def test_equal_temp_changes_nothing(self):
        r = LocalRecord((0, 0))
        r.add_report(7)
        r.add_report(7)
        self.assertEqual((r.min, r.max), (7, 7))

    def test_zero_as_first_report(self):
        r = LocalRecord((0, 0))
        r.add_report(0)
        r.add_report(-1)
        r.add_report(1)
        self.assertEqual((r.min, r.max), (-1, 1))

    def test_all_negative(self):
        r = LocalRecord((0, 0))
        for t in (-5, -20, -1):
            r.add_report(t)
        self.assertEqual((r.min, r.max), (-20, -1))

    def test_floats_and_mixed_numeric_types(self):
        r = LocalRecord((0, 0))
        r.add_report(1)
        r.add_report(1.5)
        r.add_report(0.5)
        self.assertEqual((r.min, r.max), (0.5, 1.5))

    def test_extreme_values(self):
        r = LocalRecord((0, 0))
        r.add_report(float("inf"))
        r.add_report(float("-inf"))
        self.assertEqual((r.min, r.max), (float("-inf"), float("inf")))

    def test_preconstructed_max_min_respected(self):
        r = LocalRecord((0, 0), max=10, min=0)
        r.add_report(5)
        self.assertEqual((r.min, r.max), (0, 10))
        r.add_report(11)
        r.add_report(-1)
        self.assertEqual((r.min, r.max), (-1, 11))

    def test_many_reports(self):
        r = LocalRecord((0, 0))
        for t in range(-500, 501):
            r.add_report(t)
        self.assertEqual((r.min, r.max), (-500, 500))

    # invalid inputs / potential bugs
    def test_incomparable_type_after_valid_report_raises(self):
        r = LocalRecord((0, 0))
        r.add_report(5)
        with self.assertRaises(TypeError):
            r.add_report("hot")

    def test_string_first_then_number_raises(self):
        r = LocalRecord((0, 0))
        r.add_report("hot")
        with self.assertRaises(TypeError):
            r.add_report(5)

    def test_none_first_report_is_silently_accepted(self):
        # Documents a potential bug: no validation, so None is stored as a
        # "report" and min/max stay None.
        r = LocalRecord((0, 0))
        r.add_report(None)
        self.assertIsNone(r.max)
        self.assertIsNone(r.min)

    def test_none_after_valid_report_raises(self):
        r = LocalRecord((0, 0))
        r.add_report(5)
        with self.assertRaises(TypeError):
            r.add_report(None)

    def test_nan_report_does_not_corrupt_after_valid_value(self):
        # NaN compares False to everything, so it should be ignored.
        r = LocalRecord((0, 0))
        r.add_report(5)
        r.add_report(float("nan"))
        self.assertEqual((r.min, r.max), (5, 5))


class TestLocalRecordEqualityHashRepr(unittest.TestCase):
    """Tests for __eq__, __hash__, and __repr__ of LocalRecord."""

    def test_equal_when_same_pos(self):
        self.assertEqual(LocalRecord((1, 2)), LocalRecord((1, 2)))

    def test_equal_ignores_temperatures(self):
        self.assertEqual(LocalRecord((1, 2), 10, 0), LocalRecord((1, 2), 99, -99))

    def test_not_equal_different_pos(self):
        self.assertNotEqual(LocalRecord((1, 2)), LocalRecord((2, 1)))

    def test_equal_after_rounding(self):
        self.assertEqual(LocalRecord((1.2, 2.2)), LocalRecord((0.8, 1.9)))

    def test_not_equal_to_other_types(self):
        r = LocalRecord((1, 2))
        self.assertNotEqual(r, (1, 2))
        self.assertNotEqual(r, None)
        self.assertNotEqual(r, "Record")
        self.assertFalse(r == 5)

    def test_reflexive(self):
        r = LocalRecord((3, 4))
        self.assertEqual(r, r)

    def test_equal_across_precisions_if_pos_matches(self):
        self.assertEqual(LocalRecord((1, 2), precision=0),
                         LocalRecord((1.0, 2.0), precision=3))

    def test_equal_objects_have_equal_hashes(self):
        a, b = LocalRecord((1.2, 2.2)), LocalRecord((1.1, 1.9))
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))

    def test_hash_matches_hash_of_pos(self):
        r = LocalRecord((5, 6))
        self.assertEqual(hash(r), hash(r.pos))

    def test_hash_unchanged_by_new_report(self):
        r = LocalRecord((5, 6))
        h = hash(r)
        r.add_report(100)
        self.assertEqual(hash(r), h)

    def test_set_deduplicates_by_position(self):
        s = {LocalRecord((1, 1), 5, 5), LocalRecord((1, 1), 9, 9), LocalRecord((2, 2))}
        self.assertEqual(len(s), 2)

    def test_usable_as_dict_key(self):
        d = {LocalRecord((1, 1)): "a"}
        self.assertEqual(d[LocalRecord((1, 1))], "a")

    def test_repr_with_no_reports(self):
        r = LocalRecord((1.4, 2.6))
        self.assertEqual(repr(r), "Record(pos=(1.0, 3.0), max=None, min=None)")

    def test_repr_with_reports(self):
        r = LocalRecord((1.26, 2.34), precision=1)
        r.add_report(5)
        r.add_report(3)
        self.assertEqual(repr(r), "Record(pos=(1.3, 2.3), max=5, min=3)")

    def test_repr_with_negative_temps(self):
        r = LocalRecord((0, 0), max=-1, min=-9)
        self.assertEqual(repr(r), "Record(pos=(0, 0), max=-1, min=-9)")


class TestRecordsMapInit(unittest.TestCase):
    """Tests for RecordsMap construction and __len__."""

    def test_default_state(self):
        m = RecordsMap()
        self.assertEqual(m.capacity, 8)
        self.assertEqual(len(m), 0)
        self.assertEqual(len(m.table), 8)
        self.assertTrue(all(bucket == [] for bucket in m.table))

    def test_custom_capacity(self):
        m = RecordsMap(capacity=20)
        self.assertEqual(m.capacity, 20)
        self.assertEqual(len(m.table), 20)

    def test_load_factor_attribute(self):
        self.assertEqual(RecordsMap().cap, 0.7)

    def test_buckets_are_independent_lists(self):
        m = RecordsMap(4)
        m.table[0].append("x")
        self.assertEqual(m.table[1], [])

    def test_zero_capacity_fails_on_first_use(self):
        m = RecordsMap(capacity=0)
        with self.assertRaises(ZeroDivisionError):
            m.add_report((0, 0), 1)

    def test_negative_capacity_fails_on_first_use(self):
        m = RecordsMap(capacity=-3)
        with self.assertRaises((IndexError, ZeroDivisionError, ValueError)):
            m.add_report((0, 0), 1)

    def test_non_integer_capacity_raises(self):
        with self.assertRaises(TypeError):
            RecordsMap(capacity=2.5)

    def test_len_is_int(self):
        self.assertIsInstance(len(RecordsMap()), int)


class TestRecordsMapBasicOperations(unittest.TestCase):
    """Tests for add_report, __getitem__ and __contains__."""

    def setUp(self):
        self.m = RecordsMap()

    def test_add_single_report(self):
        self.m.add_report((1, 2), 15)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(1, 2)], (15, 15))

    def test_getitem_returns_min_then_max(self):
        self.m.add_report((0, 0), 10)
        self.m.add_report((0, 0), 30)
        mn, mx = self.m[(0, 0)]
        self.assertEqual(mn, 10)
        self.assertEqual(mx, 30)

    def test_update_existing_position_does_not_grow(self):
        self.m.add_report((1, 1), 10)
        self.m.add_report((1, 1), 20)
        self.m.add_report((1, 1), 5)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(1, 1)], (5, 20))

    def test_update_with_middle_value(self):
        self.m.add_report((1, 1), 0)
        self.m.add_report((1, 1), 10)
        self.m.add_report((1, 1), 5)
        self.assertEqual(self.m[(1, 1)], (0, 10))

    def test_distinct_positions_tracked_separately(self):
        self.m.add_report((0, 0), 1)
        self.m.add_report((0, 1), 2)
        self.m.add_report((1, 0), 3)
        self.assertEqual(len(self.m), 3)
        self.assertEqual(self.m[(0, 0)], (1, 1))
        self.assertEqual(self.m[(0, 1)], (2, 2))
        self.assertEqual(self.m[(1, 0)], (3, 3))

    def test_swapped_coordinates_are_different_keys(self):
        self.m.add_report((1, 2), 10)
        self.assertNotIn((2, 1), self.m)

    def test_contains_true_and_false(self):
        self.m.add_report((3, 4), 1)
        self.assertIn((3, 4), self.m)
        self.assertNotIn((4, 3), self.m)
        self.assertNotIn((0, 0), self.m)

    def test_contains_on_empty_map(self):
        self.assertNotIn((0, 0), self.m)

    def test_missing_key_raises_keyerror(self):
        with self.assertRaises(KeyError):
            self.m[(9, 9)]

    def test_missing_key_on_nonempty_map_raises(self):
        self.m.add_report((0, 0), 1)
        with self.assertRaises(KeyError):
            self.m[(5, 5)]

    def test_zero_temperature_is_stored(self):
        self.m.add_report((0, 0), 0)
        self.assertEqual(self.m[(0, 0)], (0, 0))

    def test_negative_temperatures(self):
        self.m.add_report((0, 0), -10)
        self.m.add_report((0, 0), -30)
        self.assertEqual(self.m[(0, 0)], (-30, -10))

    def test_float_temperatures(self):
        self.m.add_report((0, 0), 1.5)
        self.m.add_report((0, 0), 2.5)
        self.assertEqual(self.m[(0, 0)], (1.5, 2.5))

    def test_negative_coordinates(self):
        self.m.add_report((-10, -20), 5)
        self.assertIn((-10, -20), self.m)
        self.assertEqual(self.m[(-10, -20)], (5, 5))

    def test_origin_and_zero_axes(self):
        self.m.add_report((0, 0), 1)
        self.m.add_report((0, 5), 2)
        self.m.add_report((5, 0), 3)
        self.assertEqual(len(self.m), 3)

    def test_large_coordinates(self):
        self.m.add_report((10**12, -10**12), 9)
        self.assertEqual(self.m[(10**12, -10**12)], (9, 9))

    def test_list_position_accepted(self):
        self.m.add_report([1, 2], 10)
        self.assertEqual(self.m[(1, 2)], (10, 10))

    def test_getitem_does_not_mutate(self):
        self.m.add_report((1, 1), 10)
        _ = self.m[(1, 1)]
        _ = (1, 1) in self.m
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(1, 1)], (10, 10))


class TestRecordsMapRounding(unittest.TestCase):
    """Tests that nearby positions are merged via rounding."""

    def setUp(self):
        self.m = RecordsMap()

    def test_nearby_positions_share_a_record(self):
        self.m.add_report((1.2, 2.2), 10)
        self.m.add_report((0.8, 1.8), 20)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(1, 2)], (10, 20))

    def test_lookup_with_unrounded_position(self):
        self.m.add_report((3, 4), 7)
        self.assertEqual(self.m[(3.4, 3.6)], (7, 7))
        self.assertIn((2.6, 4.4), self.m)

    def test_int_and_float_positions_equivalent(self):
        self.m.add_report((1, 2), 5)
        self.m.add_report((1.0, 2.0), 6)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(1, 2)], (5, 6))

    def test_bankers_rounding_boundary_merges_1_5_and_2_5(self):
        # round(1.5) == round(2.5) == 2 in Python
        self.m.add_report((1.5, 0), 10)
        self.m.add_report((2.5, 0), 20)
        self.assertEqual(len(self.m), 1)

    def test_half_boundary_distinct_cells(self):
        # round(0.5) == 0, round(0.51) == 1
        self.m.add_report((0.5, 0), 1)
        self.m.add_report((0.51, 0), 2)
        self.assertEqual(len(self.m), 2)

    def test_negative_half_merges_with_zero(self):
        self.m.add_report((-0.5, -0.5), 1)
        self.m.add_report((0, 0), 2)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(0, 0)], (1, 2))

    def test_just_below_and_above_boundary(self):
        self.m.add_report((0.49, 0), 1)
        self.m.add_report((0.51, 0), 2)
        self.assertEqual(len(self.m), 2)


class TestRecordsMapCollisions(unittest.TestCase):
    """Tests separate chaining when positions land in the same bucket."""

    def _colliding_positions(self, m, count=2):
        groups = {}
        for i in range(500):
            groups.setdefault(m._hash((i, 0)), []).append((i, 0))
        for positions in groups.values():
            if len(positions) >= count:
                return positions[:count]
        self.fail("could not find colliding positions")

    def test_colliding_positions_share_bucket_but_stay_distinct(self):
        m = RecordsMap(capacity=64)
        p1, p2 = self._colliding_positions(m)
        m.add_report(p1, 10)
        m.add_report(p2, 50)
        self.assertEqual(len(m), 2)
        self.assertEqual(len(m.table[m._hash(p1)]), 2)
        self.assertEqual(m[p1], (10, 10))
        self.assertEqual(m[p2], (50, 50))

    def test_update_in_collided_bucket_hits_correct_record(self):
        m = RecordsMap(capacity=64)
        p1, p2 = self._colliding_positions(m)
        m.add_report(p1, 10)
        m.add_report(p2, 50)
        m.add_report(p2, 60)
        m.add_report(p1, 0)
        self.assertEqual(m[p1], (0, 10))
        self.assertEqual(m[p2], (50, 60))
        self.assertEqual(len(m), 2)

    def test_contains_in_collided_bucket(self):
        m = RecordsMap(capacity=64)
        p1, p2 = self._colliding_positions(m)
        m.add_report(p1, 1)
        self.assertIn(p1, m)
        self.assertNotIn(p2, m)

    def test_getitem_missing_in_occupied_bucket_raises(self):
        m = RecordsMap(capacity=64)
        p1, p2 = self._colliding_positions(m)
        m.add_report(p1, 1)
        with self.assertRaises(KeyError):
            m[p2]


class TestRecordsMapRehash(unittest.TestCase):
    """Tests for automatic resizing and _rehash."""

    def test_no_resize_at_or_below_threshold(self):
        m = RecordsMap(capacity=8)
        for i in range(5):  # 5/8 = 0.625
            m.add_report((i, 0), i)
        self.assertEqual(m.capacity, 8)
        self.assertEqual(len(m), 5)

    def test_resize_when_threshold_exceeded(self):
        m = RecordsMap(capacity=8)
        for i in range(6):  # 6/8 = 0.75 > 0.7
            m.add_report((i, 0), i)
        self.assertEqual(m.capacity, 16)
        self.assertEqual(len(m.table), 16)
        self.assertEqual(len(m), 6)

    def test_updates_never_trigger_resize(self):
        m = RecordsMap(capacity=8)
        for i in range(5):
            m.add_report((i, 0), i)
        for t in range(100):
            m.add_report((0, 0), t)
        self.assertEqual(m.capacity, 8)
        self.assertEqual(len(m), 5)

    def test_data_preserved_after_rehash(self):
        m = RecordsMap(capacity=8)
        for i in range(6):
            m.add_report((i, i), i)
            m.add_report((i, i), i + 100)
        self.assertEqual(m.capacity, 16)
        for i in range(6):
            self.assertEqual(m[(i, i)], (i, i + 100))

    def test_rehash_preserves_equal_min_max(self):
        m = RecordsMap(capacity=2)
        m.add_report((0, 0), 5)
        m.add_report((1, 1), 5)
        m.add_report((2, 2), 5)
        for p in ((0, 0), (1, 1), (2, 2)):
            self.assertEqual(m[p], (5, 5))
        self.assertEqual(len(m), 3)

    def test_rehash_preserves_negative_and_zero_values(self):
        m = RecordsMap(capacity=2)
        m.add_report((0, 0), 0)
        m.add_report((0, 0), -10)
        m.add_report((1, 0), 0)
        m.add_report((2, 0), 0)
        self.assertEqual(m[(0, 0)], (-10, 0))

    def test_load_factor_invariant_maintained(self):
        m = RecordsMap(capacity=8)
        for i in range(200):
            m.add_report((i, -i), i)
            self.assertLessEqual(len(m) / m.capacity, 0.7)

    def test_capacity_one_grows(self):
        m = RecordsMap(capacity=1)
        m.add_report((0, 0), 1)
        self.assertEqual(m.capacity, 2)
        self.assertEqual(m[(0, 0)], (1, 1))

    def test_capacity_two_grows_to_four(self):
        m = RecordsMap(capacity=2)
        m.add_report((0, 0), 1)
        self.assertEqual(m.capacity, 2)
        m.add_report((1, 0), 2)
        self.assertEqual(m.capacity, 4)

    def test_multiple_consecutive_rehashes(self):
        m = RecordsMap(capacity=2)
        for i in range(100):
            m.add_report((i, 0), i)
        self.assertEqual(len(m), 100)
        self.assertGreaterEqual(m.capacity, 100 / 0.7)
        for i in range(100):
            self.assertEqual(m[(i, 0)], (i, i))

    def test_updates_still_work_after_rehash(self):
        m = RecordsMap(capacity=2)
        for i in range(20):
            m.add_report((i, 0), 10)
        m.add_report((7, 0), 99)
        m.add_report((7, 0), -99)
        self.assertEqual(m[(7, 0)], (-99, 99))
        self.assertEqual(len(m), 20)

    def test_manual_rehash_preserves_contents(self):
        m = RecordsMap(capacity=8)
        m.add_report((1, 1), 3)
        m.add_report((1, 1), 9)
        m.add_report((2, 2), 4)
        m._rehash(32)
        self.assertEqual(m.capacity, 32)
        self.assertEqual(len(m.table), 32)
        self.assertEqual(len(m), 2)
        self.assertEqual(m[(1, 1)], (3, 9))
        self.assertEqual(m[(2, 2)], (4, 4))

    def test_manual_rehash_to_smaller_capacity(self):
        m = RecordsMap(capacity=16)
        m.add_report((1, 1), 3)
        m.add_report((2, 2), 4)
        m._rehash(4)
        self.assertEqual(len(m), 2)
        self.assertEqual(m[(1, 1)], (3, 3))
        self.assertEqual(m[(2, 2)], (4, 4))

    def test_rehash_on_empty_table(self):
        m = RecordsMap(capacity=4)
        m._rehash(8)
        self.assertEqual(m.capacity, 8)
        self.assertEqual(len(m), 0)

    def test_no_duplicate_records_after_rehash(self):
        m = RecordsMap(capacity=2)
        for i in range(30):
            m.add_report((i % 10, 0), i)
        total = sum(len(b) for b in m.table)
        self.assertEqual(total, len(m))
        self.assertEqual(len(m), 10)


class TestRecordsMapStress(unittest.TestCase):
    """Larger-scale behaviour checks."""

    def test_many_distinct_positions(self):
        m = RecordsMap()
        n = 1000
        for i in range(n):
            m.add_report((i, i * 2), i)
        self.assertEqual(len(m), n)
        for i in range(n):
            self.assertIn((i, i * 2), m)
            self.assertEqual(m[(i, i * 2)], (i, i))

    def test_many_reports_one_position(self):
        m = RecordsMap()
        for t in range(-1000, 1001):
            m.add_report((5, 5), t)
        self.assertEqual(len(m), 1)
        self.assertEqual(m[(5, 5)], (-1000, 1000))

    def test_grid_of_positions_including_negatives(self):
        m = RecordsMap()
        for x in range(-10, 11):
            for y in range(-10, 11):
                m.add_report((x, y), x * y)
        self.assertEqual(len(m), 21 * 21)
        self.assertEqual(m[(-10, 10)], (-100, -100))
        self.assertEqual(m[(0, 0)], (0, 0))

    def test_size_matches_total_bucket_contents(self):
        m = RecordsMap()
        for i in range(250):
            m.add_report((i % 97, i % 31), i)
        self.assertEqual(sum(len(b) for b in m.table), len(m))


class TestRecordsMapInvalidInputs(unittest.TestCase):
    """Tests for malformed positions and temperatures."""

    def setUp(self):
        self.m = RecordsMap()

    def test_none_position_raises(self):
        with self.assertRaises(TypeError):
            self.m.add_report(None, 1)
        with self.assertRaises(TypeError):
            self.m[None]
        with self.assertRaises(TypeError):
            None in self.m

    def test_scalar_position_raises(self):
        with self.assertRaises(TypeError):
            self.m.add_report(5, 1)

    def test_short_position_raises(self):
        with self.assertRaises(IndexError):
            self.m.add_report((1,), 1)
        with self.assertRaises(IndexError):
            self.m[(1,)]
        with self.assertRaises(IndexError):
            (1,) in self.m

    def test_empty_position_raises(self):
        with self.assertRaises(IndexError):
            self.m.add_report((), 1)

    def test_string_position_raises(self):
        with self.assertRaises(TypeError):
            self.m.add_report(("a", "b"), 1)

    def test_nan_position_raises(self):
        with self.assertRaises(ValueError):
            self.m.add_report((float("nan"), 0), 1)

    def test_infinite_position_raises(self):
        with self.assertRaises(OverflowError):
            self.m.add_report((float("inf"), 0), 1)
        with self.assertRaises(OverflowError):
            self.m.add_report((0, float("-inf")), 1)

    def test_failed_add_leaves_map_unchanged(self):
        with self.assertRaises(TypeError):
            self.m.add_report(None, 1)
        self.assertEqual(len(self.m), 0)

    def test_incomparable_temperature_raises_and_size_unchanged(self):
        self.m.add_report((0, 0), 5)
        with self.assertRaises(TypeError):
            self.m.add_report((0, 0), "warm")
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(0, 0)], (5, 5))

    def test_none_temperature_on_existing_position_raises(self):
        self.m.add_report((0, 0), 5)
        with self.assertRaises(TypeError):
            self.m.add_report((0, 0), None)


if __name__ == "__main__":
    unittest.main()