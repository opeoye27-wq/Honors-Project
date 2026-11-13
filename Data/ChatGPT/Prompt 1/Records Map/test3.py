import unittest

# Import LocalRecord and RecordsMap from the original program if stored
# in a separate module. For example:
# from records import LocalRecord, RecordsMap
from RecordsMap import LocalRecord, RecordsMap


class TestLocalRecord(unittest.TestCase):

    def test_initialization(self):
        record = LocalRecord((10.25, 20.75), 30, 15)
        self.assertEqual(record.pos, (10, 21))
        self.assertEqual(record.max, 30)
        self.assertEqual(record.min, 15)

    def test_initialization_without_temperatures(self):
        record = LocalRecord((10, 20))
        self.assertIsNone(record.max)
        self.assertIsNone(record.min)

    def test_initialization_with_custom_precision(self):
        record = LocalRecord((10.12345, 20.67891), precision=2)
        self.assertEqual(record.pos, (10.12, 20.68))

    def test_initialization_with_negative_coordinates(self):
        record = LocalRecord((-10.567, -20.123), precision=2)
        self.assertEqual(record.pos, (-10.57, -20.12))

    def test_initialization_with_zero_coordinates(self):
        record = LocalRecord((0, 0))
        self.assertEqual(record.pos, (0, 0))

    def test_add_first_report(self):
        record = LocalRecord((1, 2))
        record.add_report(25)
        self.assertEqual(record.max, 25)
        self.assertEqual(record.min, 25)

    def test_add_higher_temperature(self):
        record = LocalRecord((1, 2), 30, 10)
        record.add_report(40)
        self.assertEqual(record.max, 40)
        self.assertEqual(record.min, 10)

    def test_add_lower_temperature(self):
        record = LocalRecord((1, 2), 30, 10)
        record.add_report(5)
        self.assertEqual(record.max, 30)
        self.assertEqual(record.min, 5)

    def test_add_temperature_between_min_and_max(self):
        record = LocalRecord((1, 2), 30, 10)
        record.add_report(20)
        self.assertEqual(record.max, 30)
        self.assertEqual(record.min, 10)

    def test_add_temperature_equal_to_max(self):
        record = LocalRecord((1, 2), 30, 10)
        record.add_report(30)
        self.assertEqual(record.max, 30)
        self.assertEqual(record.min, 10)

    def test_add_temperature_equal_to_min(self):
        record = LocalRecord((1, 2), 30, 10)
        record.add_report(10)
        self.assertEqual(record.max, 30)
        self.assertEqual(record.min, 10)

    def test_negative_temperatures(self):
        record = LocalRecord((1, 2))
        record.add_report(-10)
        record.add_report(-20)
        record.add_report(-5)
        self.assertEqual(record.min, -20)
        self.assertEqual(record.max, -5)

    def test_zero_temperature(self):
        record = LocalRecord((1, 2))
        record.add_report(0)
        self.assertEqual(record.min, 0)
        self.assertEqual(record.max, 0)

    def test_float_temperatures(self):
        record = LocalRecord((1, 2))
        record.add_report(12.75)
        record.add_report(15.25)
        self.assertEqual(record.min, 12.75)
        self.assertEqual(record.max, 15.25)

    def test_equality_same_position(self):
        record1 = LocalRecord((1.1, 2.2), 30, 10)
        record2 = LocalRecord((1.4, 2.3), 50, 5)
        self.assertEqual(record1, record2)

    def test_inequality_different_position(self):
        record1 = LocalRecord((1, 2))
        record2 = LocalRecord((3, 4))
        self.assertNotEqual(record1, record2)

    def test_equality_ignores_temperature(self):
        record1 = LocalRecord((1, 2), 30, 10)
        record2 = LocalRecord((1, 2), 100, -50)
        self.assertEqual(record1, record2)

    def test_equality_with_different_object_type(self):
        record = LocalRecord((1, 2))
        self.assertNotEqual(record, (1, 2))
        self.assertNotEqual(record, None)
        self.assertNotEqual(record, "record")

    def test_hash_equal_for_equal_records(self):
        record1 = LocalRecord((1, 2))
        record2 = LocalRecord((1, 2), 50, 10)
        self.assertEqual(hash(record1), hash(record2))

    def test_hash_consistency(self):
        record = LocalRecord((1, 2))
        self.assertEqual(hash(record), hash(record))

    def test_records_in_set(self):
        record1 = LocalRecord((1, 2))
        record2 = LocalRecord((1, 2), 30, 10)
        record3 = LocalRecord((3, 4))
        self.assertEqual(len({record1, record2, record3}), 2)

    def test_repr(self):
        record = LocalRecord((1, 2), 30, 10)
        self.assertEqual(
            repr(record),
            "Record(pos=(1, 2), max=30, min=10)"
        )

    def test_invalid_empty_position(self):
        with self.assertRaises((IndexError, TypeError)):
            LocalRecord(())

    def test_invalid_one_coordinate(self):
        with self.assertRaises((IndexError, TypeError)):
            LocalRecord((1,))

    def test_invalid_non_numeric_coordinates(self):
        with self.assertRaises(TypeError):
            LocalRecord(("north", "south"))

    def test_invalid_none_position(self):
        with self.assertRaises(TypeError):
            LocalRecord(None)

    def test_invalid_precision_type(self):
        with self.assertRaises(TypeError):
            LocalRecord((1, 2), precision="two")

    def test_invalid_precision_negative(self):
        record = LocalRecord((123.456, 789.123), precision=-1)
        self.assertEqual(record.pos, (120.0, 790.0))

    def test_extra_coordinates_are_ignored(self):
        record = LocalRecord((1, 2, 3))
        self.assertEqual(record.pos, (1, 2))


class TestRecordsMap(unittest.TestCase):

    def setUp(self):
        self.records = RecordsMap()

    def test_initialization(self):
        self.assertEqual(self.records.capacity, 8)
        self.assertEqual(len(self.records), 0)
        self.assertEqual(len(self.records.table), 8)

    def test_custom_capacity(self):
        records = RecordsMap(16)
        self.assertEqual(records.capacity, 16)
        self.assertEqual(len(records.table), 16)

    def test_add_single_report(self):
        self.records.add_report((1, 2), 25)
        self.assertEqual(len(self.records), 1)
        self.assertIn((1, 2), self.records)
        self.assertEqual(self.records[(1, 2)], (25, 25))

    def test_add_multiple_distinct_positions(self):
        positions = [(1, 2), (3, 4), (5, 6)]
        for i, pos in enumerate(positions):
            self.records.add_report(pos, 10 + i)

        self.assertEqual(len(self.records), 3)

        for i, pos in enumerate(positions):
            self.assertEqual(self.records[pos], (10 + i, 10 + i))

    def test_update_maximum_temperature(self):
        self.records.add_report((1, 2), 20)
        self.records.add_report((1, 2), 40)
        self.assertEqual(self.records[(1, 2)], (20, 40))
        self.assertEqual(len(self.records), 1)

    def test_update_minimum_temperature(self):
        self.records.add_report((1, 2), 40)
        self.records.add_report((1, 2), 10)
        self.assertEqual(self.records[(1, 2)], (10, 40))

    def test_update_temperature_between_min_and_max(self):
        self.records.add_report((1, 2), 10)
        self.records.add_report((1, 2), 30)
        self.records.add_report((1, 2), 20)
        self.assertEqual(self.records[(1, 2)], (10, 30))

    def test_duplicate_position_does_not_increase_size(self):
        self.records.add_report((1, 2), 10)
        self.records.add_report((1, 2), 20)
        self.records.add_report((1, 2), 30)
        self.assertEqual(len(self.records), 1)

    def test_rounded_positions_are_treated_as_same(self):
        self.records.add_report((1.2, 2.3), 10)
        self.records.add_report((1.4, 2.4), 30)
        self.assertEqual(len(self.records), 1)
        self.assertEqual(self.records[(1, 2)], (10, 30))

    def test_rounding_boundary(self):
        self.records.add_report((1.5, 2.5), 10)
        self.assertIn((2, 2), self.records)
        self.assertEqual(self.records[(2, 2)], (10, 10))

    def test_negative_coordinates(self):
        self.records.add_report((-1.5, -2.5), 15)
        self.assertIn((-2, -2), self.records)
        self.assertEqual(self.records[(-2, -2)], (15, 15))

    def test_zero_coordinates(self):
        self.records.add_report((0, 0), 10)
        self.assertIn((0, 0), self.records)
        self.assertEqual(self.records[(0, 0)], (10, 10))

    def test_negative_temperatures(self):
        self.records.add_report((1, 2), -10)
        self.records.add_report((1, 2), -20)
        self.records.add_report((1, 2), -5)
        self.assertEqual(self.records[(1, 2)], (-20, -5))

    def test_zero_temperature(self):
        self.records.add_report((1, 2), 0)
        self.assertEqual(self.records[(1, 2)], (0, 0))

    def test_float_temperatures(self):
        self.records.add_report((1, 2), 10.5)
        self.records.add_report((1, 2), 20.5)
        self.assertEqual(self.records[(1, 2)], (10.5, 20.5))

    def test_same_temperature_multiple_reports(self):
        for _ in range(10):
            self.records.add_report((1, 2), 25)

        self.assertEqual(len(self.records), 1)
        self.assertEqual(self.records[(1, 2)], (25, 25))

    def test_contains_existing_position(self):
        self.records.add_report((1, 2), 10)
        self.assertIn((1, 2), self.records)

    def test_contains_missing_position(self):
        self.assertNotIn((100, 200), self.records)

    def test_contains_rounded_position(self):
        self.records.add_report((1.2, 2.2), 10)
        self.assertIn((1.4, 2.4), self.records)

    def test_getitem_missing_position(self):
        with self.assertRaises(KeyError):
            self.records[(100, 200)]

    def test_getitem_rounded_position(self):
        self.records.add_report((1.2, 2.2), 10)
        self.assertEqual(self.records[(1.4, 2.4)], (10, 10))

    def test_getitem_returns_min_then_max(self):
        self.records.add_report((1, 2), 50)
        self.records.add_report((1, 2), 10)
        self.assertEqual(self.records[(1, 2)], (10, 50))

    def test_len_empty_map(self):
        self.assertEqual(len(self.records), 0)

    def test_len_after_insertions(self):
        for i in range(5):
            self.records.add_report((i, i + 1), i * 10)

        self.assertEqual(len(self.records), 5)

    def test_collision_handling(self):
        # Find two different positions that map to the same bucket.
        positions = []
        for i in range(100):
            pos = (i, i + 1)
            if not positions:
                positions.append(pos)
            elif self.records._hash(pos) == self.records._hash(positions[0]):
                positions.append(pos)
                break

        self.assertEqual(len(positions), 2)

        self.records.add_report(positions[0], 10)
        self.records.add_report(positions[1], 20)

        self.assertEqual(len(self.records), 2)
        self.assertEqual(self.records[positions[0]], (10, 10))
        self.assertEqual(self.records[positions[1]], (20, 20))

    def test_rehash_triggered_at_load_factor(self):
        for i in range(6):
            self.records.add_report((i, i + 10), i)

        self.assertEqual(self.records.capacity, 8)

        self.records.add_report((6, 16), 6)

        self.assertEqual(self.records.capacity, 16)
        self.assertEqual(len(self.records), 7)

    def test_rehash_preserves_all_records(self):
        original = {}

        for i in range(50):
            pos = (i, i + 100)
            self.records.add_report(pos, i)
            self.records.add_report(pos, i + 50)
            original[pos] = (i, i + 50)

        self.assertEqual(len(self.records), 50)

        for pos, expected in original.items():
            self.assertEqual(self.records[pos], expected)

    def test_rehash_preserves_minimum_and_maximum(self):
        self.records.add_report((1, 2), 10)
        self.records.add_report((1, 2), 50)

        for i in range(20):
            self.records.add_report((i + 10, i + 20), i)

        self.assertEqual(self.records[(1, 2)], (10, 50))

    def test_multiple_rehashes(self):
        for i in range(200):
            self.records.add_report((i, i * 2), i)

        self.assertGreater(self.records.capacity, 8)
        self.assertEqual(len(self.records), 200)

        for i in range(200):
            self.assertEqual(self.records[(i, i * 2)], (i, i))

    def test_rehash_empty_table(self):
        self.records._rehash(16)
        self.assertEqual(self.records.capacity, 16)
        self.assertEqual(len(self.records), 0)
        self.assertEqual(len(self.records.table), 16)

    def test_rehash_preserves_single_temperature(self):
        self.records.add_report((1, 2), 25)
        self.records._rehash(16)
        self.assertEqual(self.records[(1, 2)], (25, 25))

    def test_rehash_preserves_negative_temperatures(self):
        self.records.add_report((1, 2), -50)
        self.records.add_report((1, 2), -10)
        self.records._rehash(16)
        self.assertEqual(self.records[(1, 2)], (-50, -10))

    def test_rehash_does_not_duplicate_records(self):
        for i in range(100):
            self.records.add_report((i, i + 1), i)

        self.assertEqual(len(self.records), 100)

        positions = set()
        for bucket in self.records.table:
            for record in bucket:
                positions.add(record.pos)

        self.assertEqual(len(positions), 100)

    def test_rehash_capacity_matches_table_length(self):
        for i in range(100):
            self.records.add_report((i, i + 1), i)

        self.assertEqual(self.records.capacity, len(self.records.table))

    def test_invalid_position_none(self):
        with self.assertRaises(TypeError):
            self.records.add_report(None, 10)

    def test_invalid_empty_position(self):
        with self.assertRaises((IndexError, TypeError)):
            self.records.add_report((), 10)

    def test_invalid_one_coordinate(self):
        with self.assertRaises((IndexError, TypeError)):
            self.records.add_report((1,), 10)

    def test_invalid_non_numeric_coordinates(self):
        with self.assertRaises(TypeError):
            self.records.add_report(("north", "south"), 10)

    def test_invalid_position_for_getitem(self):
        with self.assertRaises((IndexError, TypeError)):
            self.records[()]

    def test_invalid_position_for_contains(self):
        with self.assertRaises((IndexError, TypeError)):
            _ = () in self.records

    def test_invalid_capacity_zero(self):
        records = RecordsMap(0)
        with self.assertRaises(ZeroDivisionError):
            records.add_report((1, 2), 10)

    def test_invalid_negative_capacity(self):
        records = RecordsMap(-1)
        with self.assertRaises((ValueError, ZeroDivisionError)):
            records.add_report((1, 2), 10)

    def test_invalid_non_integer_capacity(self):
        with self.assertRaises(TypeError):
            RecordsMap("eight")

    def test_invalid_none_capacity(self):
        with self.assertRaises(TypeError):
            RecordsMap(None)

    def test_invalid_non_numeric_temperature(self):
        with self.assertRaises(TypeError):
            self.records.add_report((1, 2), "hot")

    def test_invalid_temperature_none(self):
        self.records.add_report((1, 2), None)
        self.assertEqual(self.records[(1, 2)], (None, None))

        with self.assertRaises(TypeError):
            self.records.add_report((1, 2), 10)

    def test_boolean_temperature(self):
        self.records.add_report((1, 2), True)
        self.records.add_report((1, 2), False)
        self.assertEqual(self.records[(1, 2)], (False, True))

    def test_nan_temperature(self):
        self.records.add_report((1, 2), float("nan"))
        self.assertTrue((1, 2) in self.records)

    def test_infinity_temperature(self):
        self.records.add_report((1, 2), float("inf"))
        self.records.add_report((1, 2), float("-inf"))
        self.assertEqual(self.records[(1, 2)], (float("-inf"), float("inf")))

    def test_extra_coordinates_are_ignored(self):
        self.records.add_report((1, 2, 3), 10)
        self.assertIn((1, 2), self.records)

    def test_integer_and_float_coordinates(self):
        self.records.add_report((1, 2), 10)
        self.assertIn((1.0, 2.0), self.records)
        self.assertEqual(self.records[(1.0, 2.0)], (10, 10))

    def test_rounding_consistency_after_rehash(self):
        self.records.add_report((1.2, 2.2), 10)
        self.records.add_report((1.4, 2.4), 20)

        for i in range(20):
            self.records.add_report((i + 10, i + 20), i)

        self.assertEqual(self.records[(1, 2)], (10, 20))


class TestRecordsMapEdgeCases(unittest.TestCase):

    def test_capacity_one(self):
        records = RecordsMap(1)
        records.add_report((1, 2), 10)
        self.assertEqual(records[(1, 2)], (10, 10))

    def test_capacity_two_collision(self):
        records = RecordsMap(2)
        records.add_report((1, 2), 10)
        records.add_report((3, 4), 20)
        records.add_report((5, 6), 30)

        self.assertEqual(len(records), 3)

        self.assertEqual(records[(1, 2)], (10, 10))
        self.assertEqual(records[(3, 4)], (20, 20))
        self.assertEqual(records[(5, 6)], (30, 30))

    def test_very_large_coordinates(self):
        records = RecordsMap()
        records.add_report((10**100, -(10**100)), 50)

        self.assertEqual(records[(10**100, -(10**100))], (50, 50))

    def test_very_small_coordinates(self):
        records = RecordsMap()
        records.add_report((0.0000001, -0.0000001), 50)

        self.assertEqual(records[(0, 0)], (50, 50))

    def test_rehash_to_non_integer_capacity(self):
        records = RecordsMap()
        with self.assertRaises(TypeError):
            records._rehash(8.5)

    def test_rehash_to_zero_capacity(self):
        records = RecordsMap()
        with self.assertRaises((ZeroDivisionError, TypeError)):
            records._rehash(0)

    def test_rehash_to_negative_capacity(self):
        records = RecordsMap()
        with self.assertRaises((ValueError, ZeroDivisionError)):
            records._rehash(-5)

    def test_manual_rehash_to_smaller_capacity(self):
        records = RecordsMap(16)

        for i in range(8):
            records.add_report((i, i + 10), i)

        records._rehash(4)

        self.assertEqual(len(records), 8)

        for i in range(8):
            self.assertEqual(records[(i, i + 10)], (i, i))

    def test_manual_rehash_preserves_multiple_reports(self):
        records = RecordsMap()

        records.add_report((1, 2), 10)
        records.add_report((1, 2), 20)
        records.add_report((1, 2), 30)

        records._rehash(16)

        self.assertEqual(records[(1, 2)], (10, 30))
        self.assertEqual(len(records), 1)


if __name__ == "__main__":
    unittest.main()