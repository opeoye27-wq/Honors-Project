import unittest

# Adjust the module name to match the file containing LocalRecord and RecordsMap.
from RecordsMap import LocalRecord, RecordsMap


class TestLocalRecordInit(unittest.TestCase):
    def test_defaults(self):
        r = LocalRecord((1, 2))
        self.assertEqual(r.pos, (1, 2))
        self.assertIsNone(r.max)
        self.assertIsNone(r.min)
        self.assertEqual(r.precision, 0)

    def test_max_and_min_stored(self):
        r = LocalRecord((1, 2), max=30, min=10)
        self.assertEqual(r.max, 30)
        self.assertEqual(r.min, 10)

    def test_only_max_given(self):
        r = LocalRecord((1, 2), max=30)
        self.assertEqual(r.max, 30)
        self.assertIsNone(r.min)

    def test_rounds_to_integer_by_default(self):
        self.assertEqual(LocalRecord((1.4, 2.6)).pos, (1, 3))

    def test_bankers_rounding_at_half(self):
        # Python rounds halves to the nearest even number
        self.assertEqual(LocalRecord((0.5, 1.5)).pos, (0, 2))
        self.assertEqual(LocalRecord((2.5, 3.5)).pos, (2, 4))

    def test_negative_coordinates(self):
        self.assertEqual(LocalRecord((-1.4, -1.6)).pos, (-1, -2))

    def test_zero_coordinates(self):
        self.assertEqual(LocalRecord((0, 0)).pos, (0, 0))

    def test_negative_zero_equals_zero(self):
        self.assertEqual(LocalRecord((-0.4, -0.4)).pos, (0, 0))

    def test_precision_one(self):
        self.assertEqual(LocalRecord((1.26, 2.34), precision=1).pos, (1.3, 2.3))

    def test_precision_two(self):
        self.assertEqual(LocalRecord((3.14159, 2.71828), precision=2).pos, (3.14, 2.72))

    def test_precision_stored(self):
        self.assertEqual(LocalRecord((1, 2), precision=3).precision, 3)

    def test_negative_precision_rounds_to_tens_and_hundreds(self):
        self.assertEqual(LocalRecord((1234, 5678), precision=-2).pos, (1200, 5700))

    def test_extra_coordinates_ignored(self):
        self.assertEqual(LocalRecord((1, 2, 3)).pos, (1, 2))

    def test_list_position_accepted(self):
        self.assertEqual(LocalRecord([1.2, 2.8]).pos, (1, 3))

    def test_large_coordinates(self):
        r = LocalRecord((1e15, -1e15))
        self.assertEqual(r.pos, (1e15, -1e15))

    def test_position_is_tuple(self):
        self.assertIsInstance(LocalRecord([1, 2]).pos, tuple)

    # invalid input
    def test_none_position_raises_type_error(self):
        with self.assertRaises(TypeError):
            LocalRecord(None)

    def test_short_position_raises_index_error(self):
        for bad in [(), (1,)]:
            with self.subTest(pos=bad):
                with self.assertRaises(IndexError):
                    LocalRecord(bad)

    def test_non_numeric_position_raises_type_error(self):
        with self.assertRaises(TypeError):
            LocalRecord(("a", "b"))

    def test_non_integer_precision_raises_type_error(self):
        with self.assertRaises(TypeError):
            LocalRecord((1.5, 2.5), precision=1.5)


class TestLocalRecordAddReport(unittest.TestCase):
    def test_first_report_sets_min_and_max(self):
        r = LocalRecord((0, 0))
        r.add_report(20)
        self.assertEqual((r.min, r.max), (20, 20))

    def test_zero_temperature_is_not_treated_as_missing(self):
        r = LocalRecord((0, 0))
        r.add_report(0)
        self.assertEqual((r.min, r.max), (0, 0))
        r.add_report(-5)
        self.assertEqual((r.min, r.max), (-5, 0))

    def test_higher_temp_updates_max_only(self):
        r = LocalRecord((0, 0))
        r.add_report(10)
        r.add_report(25)
        self.assertEqual((r.min, r.max), (10, 25))

    def test_lower_temp_updates_min_only(self):
        r = LocalRecord((0, 0))
        r.add_report(10)
        r.add_report(-3)
        self.assertEqual((r.min, r.max), (-3, 10))

    def test_temp_between_min_and_max_changes_nothing(self):
        r = LocalRecord((0, 0))
        r.add_report(0)
        r.add_report(100)
        r.add_report(50)
        self.assertEqual((r.min, r.max), (0, 100))

    def test_equal_temp_changes_nothing(self):
        r = LocalRecord((0, 0))
        r.add_report(10)
        r.add_report(10)
        self.assertEqual((r.min, r.max), (10, 10))

    def test_float_temps(self):
        r = LocalRecord((0, 0))
        r.add_report(1.5)
        r.add_report(1.25)
        r.add_report(1.75)
        self.assertEqual((r.min, r.max), (1.25, 1.75))

    def test_existing_values_respected(self):
        r = LocalRecord((0, 0), max=10, min=5)
        r.add_report(7)
        self.assertEqual((r.min, r.max), (5, 10))
        r.add_report(20)
        self.assertEqual((r.min, r.max), (5, 20))
        r.add_report(1)
        self.assertEqual((r.min, r.max), (1, 20))

    def test_only_max_set_then_report_fills_min(self):
        r = LocalRecord((0, 0), max=10)
        r.add_report(5)
        self.assertEqual((r.min, r.max), (5, 10))

    def test_many_reports(self):
        r = LocalRecord((0, 0))
        for t in [3, -8, 14, 0, 99, -100, 42]:
            r.add_report(t)
        self.assertEqual((r.min, r.max), (-100, 99))

    def test_returns_none(self):
        self.assertIsNone(LocalRecord((0, 0)).add_report(1))

    def test_none_temp_on_populated_record_raises_and_leaves_state(self):
        r = LocalRecord((0, 0))
        r.add_report(5)
        with self.assertRaises(TypeError):
            r.add_report(None)
        self.assertEqual((r.min, r.max), (5, 5))

    def test_string_temp_on_numeric_record_raises(self):
        r = LocalRecord((0, 0))
        r.add_report(5)
        with self.assertRaises(TypeError):
            r.add_report("hot")


class TestLocalRecordDunder(unittest.TestCase):
    def test_equal_when_positions_match_regardless_of_temps(self):
        self.assertEqual(LocalRecord((1, 2), 10, 0), LocalRecord((1, 2), 99, -99))

    def test_not_equal_when_positions_differ(self):
        self.assertNotEqual(LocalRecord((1, 2)), LocalRecord((2, 1)))
        self.assertNotEqual(LocalRecord((1, 2)), LocalRecord((1, 3)))

    def test_equal_after_rounding(self):
        self.assertEqual(LocalRecord((1.2, 2.2)), LocalRecord((0.8, 1.8)))

    def test_different_precision_gives_different_position(self):
        self.assertNotEqual(LocalRecord((1.26, 2.34), precision=1), LocalRecord((1.26, 2.34)))

    def test_not_equal_to_other_types(self):
        r = LocalRecord((1, 2))
        for other in [(1, 2), None, "Record", 5, [1, 2]]:
            with self.subTest(other=other):
                self.assertFalse(r == other)
                self.assertTrue(r != other)

    def test_equal_to_itself(self):
        r = LocalRecord((1, 2))
        self.assertEqual(r, r)

    def test_hash_matches_position_hash(self):
        r = LocalRecord((1, 2))
        self.assertEqual(hash(r), hash((1, 2)))

    def test_equal_records_have_equal_hashes(self):
        self.assertEqual(hash(LocalRecord((1, 2), 5, 1)), hash(LocalRecord((1, 2), 9, 3)))

    def test_set_deduplicates_by_position(self):
        s = {LocalRecord((1, 2)), LocalRecord((1, 2), 3, 4), LocalRecord((5, 6))}
        self.assertEqual(len(s), 2)

    def test_usable_as_dict_key(self):
        d = {LocalRecord((1, 2)): "a"}
        self.assertEqual(d[LocalRecord((1, 2), 10, 10)], "a")

    def test_repr_with_values(self):
        self.assertEqual(repr(LocalRecord((1, 2), max=5, min=3)),
                         "Record(pos=(1, 2), max=5, min=3)")

    def test_repr_with_none_values(self):
        self.assertEqual(repr(LocalRecord((1, 2))),
                         "Record(pos=(1, 2), max=None, min=None)")


class TestRecordsMapInit(unittest.TestCase):
    def test_default_state(self):
        m = RecordsMap()
        self.assertEqual(m.capacity, 8)
        self.assertEqual(len(m.table), 8)
        self.assertEqual(len(m), 0)
        self.assertEqual(m.size, 0)
        self.assertEqual(m.cap, 0.7)
        self.assertTrue(all(bucket == [] for bucket in m.table))

    def test_custom_capacity(self):
        m = RecordsMap(capacity=20)
        self.assertEqual(m.capacity, 20)
        self.assertEqual(len(m.table), 20)

    def test_instances_do_not_share_tables(self):
        a, b = RecordsMap(), RecordsMap()
        a.add_report((1, 1), 5)
        self.assertEqual(len(a), 1)
        self.assertEqual(len(b), 0)
        self.assertNotIn((1, 1), b)

    def test_zero_capacity_fails_on_use(self):
        # No validation in the constructor; the failure surfaces on first use.
        m = RecordsMap(0)
        with self.assertRaises(ZeroDivisionError):
            m.add_report((1, 1), 5)

    def test_negative_capacity_fails_on_use(self):
        m = RecordsMap(-1)
        with self.assertRaises((ZeroDivisionError, IndexError)):
            m.add_report((1, 1), 5)


class TestRecordsMapBasics(unittest.TestCase):
    def setUp(self):
        self.m = RecordsMap()

    def test_add_single_report(self):
        self.m.add_report((1, 2), 25)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(1, 2)], (25, 25))

    def test_add_report_returns_none(self):
        self.assertIsNone(self.m.add_report((1, 2), 25))

    def test_getitem_returns_min_then_max(self):
        self.m.add_report((1, 2), 10)
        self.m.add_report((1, 2), 5)
        self.m.add_report((1, 2), 20)
        self.assertEqual(self.m[(1, 2)], (5, 20))

    def test_update_does_not_increase_size(self):
        for t in [1, 2, 3, 4]:
            self.m.add_report((3, 3), t)
        self.assertEqual(len(self.m), 1)

    def test_multiple_distinct_positions(self):
        self.m.add_report((0, 0), 1)
        self.m.add_report((0, 1), 2)
        self.m.add_report((1, 0), 3)
        self.assertEqual(len(self.m), 3)
        self.assertEqual(self.m[(0, 0)], (1, 1))
        self.assertEqual(self.m[(0, 1)], (2, 2))
        self.assertEqual(self.m[(1, 0)], (3, 3))

    def test_swapped_coordinates_are_distinct(self):
        self.m.add_report((1, 2), 10)
        self.m.add_report((2, 1), 20)
        self.assertEqual(len(self.m), 2)
        self.assertEqual(self.m[(1, 2)], (10, 10))
        self.assertEqual(self.m[(2, 1)], (20, 20))

    def test_negative_and_zero_temperatures(self):
        self.m.add_report((1, 1), 0)
        self.assertEqual(self.m[(1, 1)], (0, 0))
        self.m.add_report((1, 1), -40)
        self.assertEqual(self.m[(1, 1)], (-40, 0))

    def test_negative_positions(self):
        self.m.add_report((-5, -7), 12)
        self.assertEqual(self.m[(-5, -7)], (12, 12))
        self.assertIn((-5, -7), self.m)

    def test_large_positions(self):
        self.m.add_report((10**12, -10**12), 3)
        self.assertEqual(self.m[(10**12, -10**12)], (3, 3))

    def test_contains_true_and_false(self):
        self.m.add_report((1, 2), 5)
        self.assertIn((1, 2), self.m)
        self.assertNotIn((2, 1), self.m)
        self.assertNotIn((9, 9), self.m)

    def test_contains_on_empty_map(self):
        self.assertNotIn((0, 0), self.m)

    def test_contains_does_not_insert(self):
        _ = (4, 4) in self.m
        self.assertEqual(len(self.m), 0)

    def test_getitem_missing_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.m[(1, 2)]

    def test_getitem_missing_message(self):
        with self.assertRaisesRegex(KeyError, "does not exist"):
            self.m[(1, 2)]

    def test_getitem_missing_when_map_nonempty(self):
        self.m.add_report((1, 2), 5)
        with self.assertRaises(KeyError):
            self.m[(3, 4)]

    def test_getitem_does_not_insert(self):
        try:
            self.m[(1, 2)]
        except KeyError:
            pass
        self.assertEqual(len(self.m), 0)

    def test_list_position_accepted(self):
        self.m.add_report([1, 2], 5)
        self.assertEqual(self.m[(1, 2)], (5, 5))
        self.assertIn([1, 2], self.m)

    def test_extra_coordinates_ignored(self):
        self.m.add_report((1, 2, 99), 5)
        self.assertEqual(self.m[(1, 2, 0)], (5, 5))
        self.assertEqual(len(self.m), 1)

    def test_lookup_of_integer_position_with_float_equivalent(self):
        self.m.add_report((1, 2), 5)
        self.assertIn((1.0, 2.0), self.m)
        self.assertEqual(self.m[(1.0, 2.0)], (5, 5))


class TestRecordsMapRounding(unittest.TestCase):
    def setUp(self):
        self.m = RecordsMap()

    def test_nearby_positions_share_a_record(self):
        self.m.add_report((1.1, 2.1), 10)
        self.m.add_report((0.9, 1.9), 20)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(1, 2)], (10, 20))

    def test_lookup_uses_rounded_position(self):
        self.m.add_report((3, 4), 10)
        self.assertIn((3.4, 3.6), self.m)
        self.assertEqual(self.m[(2.6, 4.4)], (10, 10))

    def test_rounding_boundaries(self):
        self.m.add_report((0.4999999, 0.4999999), 1)
        self.m.add_report((0.5000001, 0.5000001), 2)
        self.assertEqual(len(self.m), 2)
        self.assertEqual(self.m[(0, 0)], (1, 1))
        self.assertEqual(self.m[(1, 1)], (2, 2))

    def test_bankers_rounding_merges_half_values_to_even(self):
        # round(0.5) == 0 and round(2.5) == 2, round(1.5) == 2
        self.m.add_report((1.5, 1.5), 10)
        self.m.add_report((2.5, 2.5), 30)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(2, 2)], (10, 30))

    def test_half_rounds_to_zero(self):
        self.m.add_report((0.5, 0.5), 7)
        self.assertIn((0, 0), self.m)

    def test_small_negative_and_positive_collapse_to_origin(self):
        self.m.add_report((0.4, 0.4), 1)
        self.m.add_report((-0.4, -0.4), 9)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(0, 0)], (1, 9))

    def test_negative_rounding(self):
        self.m.add_report((-1.6, -2.4), 5)
        self.assertEqual(self.m[(-2, -2)], (5, 5))

    def test_stored_record_matches_lookup_key(self):
        self.m.add_report((2.7, 3.2), 8)
        records = [r for bucket in self.m.table for r in bucket]
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].pos, (3, 3))


class TestRecordsMapRehash(unittest.TestCase):
    def test_no_rehash_below_threshold(self):
        m = RecordsMap()
        for i in range(5):  # 5/8 = 0.625
            m.add_report((i, 0), i)
        self.assertEqual(m.capacity, 8)

    def test_rehash_when_load_exceeds_threshold(self):
        m = RecordsMap()
        for i in range(6):  # 6/8 = 0.75 > 0.7
            m.add_report((i, 0), i)
        self.assertEqual(m.capacity, 16)
        self.assertEqual(len(m.table), 16)

    def test_second_rehash(self):
        m = RecordsMap()
        for i in range(12):  # 12/16 = 0.75 > 0.7
            m.add_report((i, 0), i)
        self.assertEqual(m.capacity, 32)

    def test_small_capacity_grows(self):
        m = RecordsMap(4)
        m.add_report((0, 0), 0)
        m.add_report((1, 0), 1)
        self.assertEqual(m.capacity, 4)
        m.add_report((2, 0), 2)  # 3/4 = 0.75
        self.assertEqual(m.capacity, 8)

    def test_capacity_one(self):
        m = RecordsMap(1)
        for i in range(10):
            m.add_report((i, i), i)
        self.assertEqual(len(m), 10)
        for i in range(10):
            self.assertEqual(m[(i, i)], (i, i))

    def test_size_preserved_by_rehash(self):
        m = RecordsMap()
        for i in range(30):
            m.add_report((i, -i), i)
        self.assertEqual(len(m), 30)
        self.assertEqual(sum(len(b) for b in m.table), 30)

    def test_all_records_retrievable_after_rehash(self):
        m = RecordsMap()
        for i in range(50):
            m.add_report((i, i * 2), i)
        for i in range(50):
            self.assertIn((i, i * 2), m)
            self.assertEqual(m[(i, i * 2)], (i, i))

    def test_min_and_max_preserved_by_rehash(self):
        m = RecordsMap()
        for t in [10, 3, 7]:
            m.add_report((0, 0), t)
        for i in range(1, 6):  # forces a rehash
            m.add_report((i, 0), i)
        self.assertGreater(m.capacity, 8)
        self.assertEqual(m[(0, 0)], (3, 10))

    def test_records_with_equal_min_and_max_survive_rehash(self):
        m = RecordsMap()
        for i in range(20):
            m.add_report((i, 0), 42)
        for i in range(20):
            self.assertEqual(m[(i, 0)], (42, 42))

    def test_negative_extremes_survive_rehash(self):
        m = RecordsMap()
        m.add_report((0, 0), -50)
        m.add_report((0, 0), 50)
        for i in range(1, 20):
            m.add_report((i, 0), 0)
        self.assertEqual(m[(0, 0)], (-50, 50))

    def test_update_after_rehash(self):
        m = RecordsMap()
        m.add_report((0, 0), 5)
        for i in range(1, 10):
            m.add_report((i, 0), i)
        m.add_report((0, 0), 100)
        m.add_report((0, 0), -100)
        self.assertEqual(m[(0, 0)], (-100, 100))
        self.assertEqual(len(m), 10)

    def test_load_factor_never_exceeds_threshold(self):
        m = RecordsMap()
        for i in range(200):
            m.add_report((i, 0), i)
            self.assertLessEqual(len(m) / m.capacity, 0.7)

    def test_rehash_called_directly_keeps_data(self):
        m = RecordsMap()
        m.add_report((1, 1), 5)
        m.add_report((1, 1), 9)
        m.add_report((2, 2), 3)
        m._rehash(32)
        self.assertEqual(m.capacity, 32)
        self.assertEqual(len(m), 2)
        self.assertEqual(m[(1, 1)], (5, 9))
        self.assertEqual(m[(2, 2)], (3, 3))

    def test_rehash_empty_table(self):
        m = RecordsMap()
        m._rehash(16)
        self.assertEqual(m.capacity, 16)
        self.assertEqual(len(m), 0)


class TestRecordsMapCollisions(unittest.TestCase):
    def test_colliding_positions_chain_in_one_bucket(self):
        m = RecordsMap(64)
        seen = {}
        pair = None
        for i in range(200):  # pigeonhole guarantees a collision
            idx = m._hash((i, 0))
            if idx in seen:
                pair = (seen[idx], (i, 0))
                break
            seen[idx] = (i, 0)
        self.assertIsNotNone(pair)
        a, b = pair
        m.add_report(a, 10)
        m.add_report(b, 20)
        self.assertEqual(len(m), 2)
        self.assertEqual(m[a], (10, 10))
        self.assertEqual(m[b], (20, 20))
        self.assertEqual(len(m.table[m._hash(a)]), 2)

    def test_update_in_colliding_bucket_updates_correct_record(self):
        m = RecordsMap(64)
        seen = {}
        pair = None
        for i in range(200):
            idx = m._hash((i, 0))
            if idx in seen:
                pair = (seen[idx], (i, 0))
                break
            seen[idx] = (i, 0)
        a, b = pair
        m.add_report(a, 10)
        m.add_report(b, 20)
        m.add_report(b, 50)
        self.assertEqual(m[a], (10, 10))
        self.assertEqual(m[b], (20, 50))
        self.assertEqual(len(m), 2)

    def test_hash_index_within_range(self):
        m = RecordsMap(8)
        for pos in [(0, 0), (-1, -1), (10**9, -10**9), (3.7, -2.2)]:
            with self.subTest(pos=pos):
                self.assertTrue(0 <= m._hash(pos) < 8)

    def test_hash_consistent_for_positions_that_round_alike(self):
        m = RecordsMap()
        self.assertEqual(m._hash((1.2, 2.2)), m._hash((0.8, 1.8)))


class TestRecordsMapInvalidInput(unittest.TestCase):
    def setUp(self):
        self.m = RecordsMap()

    def test_none_position(self):
        with self.assertRaises(TypeError):
            self.m.add_report(None, 5)
        with self.assertRaises(TypeError):
            self.m[None]
        with self.assertRaises(TypeError):
            None in self.m

    def test_integer_position(self):
        with self.assertRaises(TypeError):
            self.m.add_report(5, 5)

    def test_short_positions(self):
        for bad in [(), (1,)]:
            with self.subTest(pos=bad):
                with self.assertRaises(IndexError):
                    self.m.add_report(bad, 5)
                with self.assertRaises(IndexError):
                    self.m[bad]
                with self.assertRaises(IndexError):
                    bad in self.m

    def test_non_numeric_position(self):
        with self.assertRaises(TypeError):
            self.m.add_report(("a", "b"), 5)

    def test_nan_position(self):
        with self.assertRaises(ValueError):
            self.m.add_report((float("nan"), 0), 5)

    def test_infinite_position(self):
        with self.assertRaises(OverflowError):
            self.m.add_report((float("inf"), 0), 5)
        with self.assertRaises(OverflowError):
            self.m.add_report((0, float("-inf")), 5)

    def test_failed_add_does_not_change_size(self):
        for bad in [None, (1,), ("a", "b"), (float("nan"), 0)]:
            try:
                self.m.add_report(bad, 5)
            except Exception:
                pass
        self.assertEqual(len(self.m), 0)

    def test_non_numeric_temp_on_existing_position_raises_and_preserves_state(self):
        self.m.add_report((1, 1), 5)
        with self.assertRaises(TypeError):
            self.m.add_report((1, 1), "hot")
        self.assertEqual(self.m[(1, 1)], (5, 5))
        self.assertEqual(len(self.m), 1)

    def test_none_temp_on_existing_position_raises(self):
        self.m.add_report((1, 1), 5)
        with self.assertRaises(TypeError):
            self.m.add_report((1, 1), None)
        self.assertEqual(self.m[(1, 1)], (5, 5))

    def test_none_temp_on_new_position_creates_placeholder(self):
        # Documents current behaviour: no validation of temperature on first report.
        self.m.add_report((1, 1), None)
        self.assertEqual(len(self.m), 1)
        self.assertEqual(self.m[(1, 1)], (None, None))
        self.m.add_report((1, 1), 5)
        self.assertEqual(self.m[(1, 1)], (5, 5))

    @unittest.expectedFailure
    def test_nan_temp_should_not_poison_later_reports(self):
        # Potential bug: comparisons with NaN are always False, so once a NaN
        # is stored as min/max, real temperatures can never replace it.
        self.m.add_report((1, 1), float("nan"))
        self.m.add_report((1, 1), 5)
        self.assertEqual(self.m[(1, 1)], (5, 5))


class TestRecordsMapStress(unittest.TestCase):
    def test_grid_of_positions_with_multiple_reports(self):
        m = RecordsMap()
        for x in range(-15, 15):
            for y in range(-15, 15):
                m.add_report((x, y), x + y)
                m.add_report((x, y), x - y)
        self.assertEqual(len(m), 900)
        for x in range(-15, 15):
            for y in range(-15, 15):
                self.assertEqual(m[(x, y)], (min(x + y, x - y), max(x + y, x - y)))

    def test_repeated_updates_to_single_position(self):
        m = RecordsMap()
        for t in range(-500, 501):
            m.add_report((7, 7), t)
        self.assertEqual(len(m), 1)
        self.assertEqual(m[(7, 7)], (-500, 500))

    def test_bucket_total_matches_size(self):
        m = RecordsMap()
        for i in range(257):
            m.add_report((i, i % 7), i)
        self.assertEqual(sum(len(b) for b in m.table), len(m))
        self.assertEqual(len(m), 257)


if __name__ == "__main__":
    unittest.main()