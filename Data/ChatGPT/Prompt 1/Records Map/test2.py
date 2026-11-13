import unittest

# Import LocalRecord and RecordsMap from your program
# from your_file import LocalRecord, RecordsMap
from RecordsMap import LocalRecord, RecordsMap


class TestLocalRecord(unittest.TestCase):
    """Unit tests for the LocalRecord class."""

    def test_initialization(self):
        record = LocalRecord((10.5, 20.7), 90, 40)
        self.assertEqual(record.pos, (11, 21))
        self.assertEqual(record.max, 90)
        self.assertEqual(record.min, 40)

    def test_initialization_without_temperatures(self):
        record = LocalRecord((1.2, 3.4))
        self.assertEqual(record.max, None)
        self.assertEqual(record.min, None)

    def test_initialization_with_custom_precision(self):
        record = LocalRecord((1.23456, 7.89123), precision=2)
        self.assertEqual(record.pos, (1.23, 7.89))

    def test_initialization_with_zero_precision(self):
        record = LocalRecord((1.6, 2.4), precision=0)
        self.assertEqual(record.pos, (2, 2))

    def test_initialization_with_negative_coordinates(self):
        record = LocalRecord((-1.6, -2.4))
        self.assertEqual(record.pos, (-2, -2))

    def test_add_first_report(self):
        record = LocalRecord((1, 2))
        record.add_report(25)
        self.assertEqual(record.min, 25)
        self.assertEqual(record.max, 25)

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

    def test_add_negative_temperature(self):
        record = LocalRecord((1, 2))
        record.add_report(-15)
        self.assertEqual(record.min, -15)
        self.assertEqual(record.max, -15)

    def test_add_zero_temperature(self):
        record = LocalRecord((1, 2))
        record.add_report(0)
        self.assertEqual(record.min, 0)
        self.assertEqual(record.max, 0)

    def test_add_decimal_temperature(self):
        record = LocalRecord((1, 2))
        record.add_report(23.75)
        self.assertEqual(record.min, 23.75)
        self.assertEqual(record.max, 23.75)

    def test_equality_same_position(self):
        record1 = LocalRecord((1.2, 2.3), 30, 10)
        record2 = LocalRecord((1.4, 2.2), 50, 5)
        self.assertEqual(record1, record2)

    def test_inequality_different_positions(self):
        record1 = LocalRecord((1, 2))
        record2 = LocalRecord((3, 4))
        self.assertNotEqual(record1, record2)

    def test_inequality_with_different_object(self):
        record = LocalRecord((1, 2))
        self.assertNotEqual(record, (1, 2))

    def test_equality_with_none(self):
        record = LocalRecord((1, 2))
        self.assertNotEqual(record, None)

    def test_hash_same_position(self):
        record1 = LocalRecord((1.2, 2.3))
        record2 = LocalRecord((1.4, 2.2))
        self.assertEqual(hash(record1), hash(record2))

    def test_hash_different_positions(self):
        record1 = LocalRecord((1, 2))
        record2 = LocalRecord((3, 4))
        self.assertNotEqual(hash(record1), hash(record2))

    def test_record_as_dictionary_key(self):
        record1 = LocalRecord((1, 2))
        record2 = LocalRecord((1.1, 2.1))
        records = {record1: "first"}
        self.assertEqual(records[record2], "first")

    def test_repr(self):
        record = LocalRecord((1, 2), 30, 10)
        self.assertEqual(
            repr(record),
            "Record(pos=(1, 2), max=30, min=10)"
        )


class TestRecordsMap(unittest.TestCase):
    """Unit tests for the RecordsMap class."""

    def setUp(self):
        self.records = RecordsMap()

    def test_initialization(self):
        self.assertEqual(self.records.capacity, 8)
        self.assertEqual(self.records.size, 0)
        self.assertEqual(len(self.records), 0)
        self.assertEqual(len(self.records.table), 8)

    def test_custom_capacity(self):
        records = RecordsMap(16)
        self.assertEqual(records.capacity, 16)
        self.assertEqual(len(records.table), 16)

    def test_empty_map_length(self):
        self.assertEqual(len(self.records), 0)

    def test_add_single_report(self):
        self.records.add_report((1, 2), 25)
        self.assertEqual(len(self.records), 1)
        self.assertIn((1, 2), self.records)
        self.assertEqual(self.records[(1, 2)], (25, 25))

    def test_add_multiple_different_positions(self):
        self.records.add_report((1, 2), 25)
        self.records.add_report((3, 4), 30)
        self.records.add_report((5, 6), 15)

        self.assertEqual(len(self.records), 3)
        self.assertEqual(self.records[(1, 2)], (25, 25))
        self.assertEqual(self.records[(3, 4)], (30, 30))
        self.assertEqual(self.records[(5, 6)], (15, 15))

    def test_add_higher_temperature_same_position(self):
        self.records.add_report((1, 2), 20)
        self.records.add_report((1, 2), 35)

        self.assertEqual(len(self.records), 1)
        self.assertEqual(self.records[(1, 2)], (20, 35))

    def test_add_lower_temperature_same_position(self):
        self.records.add_report((1, 2), 20)
        self.records.add_report((1, 2), 5)

        self.assertEqual(len(self.records), 1)
        self.assertEqual(self.records[(1, 2)], (5, 20))

    def test_add_temperature_between_existing_values(self):
        self.records.add_report((1, 2), 10)
        self.records.add_report((1, 2), 30)
        self.records.add_report((1, 2), 20)

        self.assertEqual(self.records[(1, 2)], (10, 30))
        self.assertEqual(len(self.records), 1)

    def test_add_duplicate_temperature(self):
        self.records.add_report((1, 2), 20)
        self.records.add_report((1, 2), 20)
        self.records.add_report((1, 2), 20)

        self.assertEqual(len(self.records), 1)
        self.assertEqual(self.records[(1, 2)], (20, 20))

    def test_add_negative_temperature(self):
        self.records.add_report((1, 2), -15)
        self.assertEqual(self.records[(1, 2)], (-15, -15))

    def test_add_zero_temperature(self):
        self.records.add_report((1, 2), 0)
        self.assertEqual(self.records[(1, 2)], (0, 0))

    def test_add_decimal_temperature(self):
        self.records.add_report((1, 2), 23.75)
        self.assertEqual(self.records[(1, 2)], (23.75, 23.75))

    def test_position_rounding(self):
        self.records.add_report((1.2, 2.3), 20)
        self.assertIn((1.4, 2.2), self.records)
        self.assertEqual(self.records[(1.4, 2.2)], (20, 20))

    def test_position_rounding_boundary(self):
        self.records.add_report((1.5, 2.5), 20)
        self.assertIn((2, 2), self.records)

    def test_negative_position_rounding(self):
        self.records.add_report((-1.6, -2.4), 20)
        self.assertIn((-2, -2), self.records)
        self.assertEqual(self.records[(-2, -2)], (20, 20))

    def test_positions_rounding_to_different_coordinates(self):
        self.records.add_report((1.2, 2.2), 20)
        self.records.add_report((2.2, 3.2), 30)

        self.assertEqual(len(self.records), 2)

    def test_contains_existing_position(self):
        self.records.add_report((1, 2), 20)
        self.assertIn((1, 2), self.records)

    def test_contains_nonexistent_position(self):
        self.assertNotIn((1, 2), self.records)

    def test_contains_position_with_decimal_coordinates(self):
        self.records.add_report((1.2, 2.3), 20)
        self.assertIn((1.4, 2.2), self.records)

    def test_getitem_existing_position(self):
        self.records.add_report((1, 2), 20)
        self.assertEqual(self.records[(1, 2)], (20, 20))

    def test_getitem_nonexistent_position(self):
        with self.assertRaises(KeyError):
            self.records[(10, 20)]

    def test_getitem_position_in_same_bucket_but_different_key(self):
        self.records.add_report((1, 2), 20)
        with self.assertRaises(KeyError):
            self.records[(9, 10)]

    def test_update_does_not_increase_size(self):
        self.records.add_report((1, 2), 20)
        self.records.add_report((1, 2), 30)
        self.records.add_report((1, 2), 10)

        self.assertEqual(len(self.records), 1)

    def test_hash_collisions(self):
        # Different positions that map to the same bucket.
        self.records.add_report((1, 2), 10)
        self.records.add_report((9, 10), 20)

        self.assertEqual(len(self.records), 2)
        self.assertEqual(self.records[(1, 2)], (10, 10))
        self.assertEqual(self.records[(9, 10)], (20, 20))

    def test_rehash_after_threshold(self):
        for i in range(6):
            self.records.add_report((i, i), i * 10)

        self.assertGreater(self.records.capacity, 8)
        self.assertEqual(len(self.records), 6)

        for i in range(6):
            self.assertEqual(self.records[(i, i)], (i * 10, i * 10))

    def test_rehash_preserves_min_and_max(self):
        self.records.add_report((1, 2), 10)
        self.records.add_report((1, 2), 50)

        for i in range(2, 7):
            self.records.add_report((i, i), i * 10)

        self.assertEqual(self.records[(1, 2)], (10, 50))

    def test_rehash_preserves_all_positions(self):
        expected = {}

        for i in range(20):
            pos = (i, i + 1)
            temp = i * 5
            self.records.add_report(pos, temp)
            expected[pos] = (temp, temp)

        self.assertEqual(len(self.records), 20)

        for pos, temps in expected.items():
            self.assertEqual(self.records[pos], temps)

    def test_rehash_preserves_negative_temperatures(self):
        self.records.add_report((1, 2), -30)
        self.records.add_report((1, 2), -10)

        for i in range(2, 7):
            self.records.add_report((i, i), i)

        self.assertEqual(self.records[(1, 2)], (-30, -10))

    def test_rehash_with_multiple_reports(self):
        self.records.add_report((1, 2), 10)
        self.records.add_report((1, 2), 20)
        self.records.add_report((1, 2), 30)

        for i in range(2, 7):
            self.records.add_report((i, i), i)

        self.assertEqual(self.records[(1, 2)], (10, 30))
        self.assertEqual(len(self.records), 6)

    def test_manual_rehash(self):
        self.records.add_report((1, 2), 10)
        self.records.add_report((3, 4), 20)

        self.records._rehash(16)

        self.assertEqual(self.records.capacity, 16)
        self.assertEqual(len(self.records), 2)
        self.assertEqual(self.records[(1, 2)], (10, 10))
        self.assertEqual(self.records[(3, 4)], (20, 20))

    def test_rehash_empty_table(self):
        self.records._rehash(16)

        self.assertEqual(self.records.capacity, 16)
        self.assertEqual(len(self.records), 0)
        self.assertEqual(len(self.records.table), 16)

    def test_rehash_preserves_duplicate_reports(self):
        self.records.add_report((1, 2), 10)
        self.records.add_report((1, 2), 10)

        self.records._rehash(16)

        self.assertEqual(len(self.records), 1)
        self.assertEqual(self.records[(1, 2)], (10, 10))

    def test_repeated_rehashes(self):
        for i in range(50):
            self.records.add_report((i, i), i)

        self.assertGreater(self.records.capacity, 8)
        self.assertEqual(len(self.records), 50)

        for i in range(50):
            self.assertEqual(self.records[(i, i)], (i, i))

    def test_capacity_threshold_exactly_seventy_percent(self):
        records = RecordsMap(10)

        for i in range(7):
            records.add_report((i, i), i)

        # Rehash occurs only when load factor is greater than 0.7.
        self.assertEqual(records.capacity, 10)

    def test_capacity_threshold_above_seventy_percent(self):
        records = RecordsMap(10)

        for i in range(8):
            records.add_report((i, i), i)

        self.assertEqual(records.capacity, 20)

    def test_repr_of_stored_record(self):
        self.records.add_report((1, 2), 25)

        record = next(
            record
            for bucket in self.records.table
            for record in bucket
        )

        self.assertEqual(
            repr(record),
            "Record(pos=(1, 2), max=25, min=25)"
        )


class TestInvalidInputs(unittest.TestCase):
    """Tests for invalid and unusual input values."""

    def test_empty_position_tuple_local_record(self):
        with self.assertRaises((IndexError, TypeError)):
            LocalRecord(())

    def test_one_coordinate_local_record(self):
        with self.assertRaises((IndexError, TypeError)):
            LocalRecord((1,))

    def test_missing_position(self):
        with self.assertRaises((TypeError, IndexError)):
            LocalRecord(None)

    def test_string_position(self):
        with self.assertRaises((TypeError, ValueError)):
            LocalRecord("12")

    def test_non_numeric_coordinates(self):
        with self.assertRaises((TypeError, ValueError)):
            LocalRecord(("north", "south"))

    def test_invalid_precision(self):
        with self.assertRaises((TypeError, ValueError)):
            LocalRecord((1, 2), precision="two")

    def test_negative_precision(self):
        record = LocalRecord((123.45, 678.91), precision=-1)
        self.assertEqual(record.pos, (120.0, 680.0))

    def test_non_numeric_temperature(self):
        record = LocalRecord((1, 2))
        with self.assertRaises(TypeError):
            record.add_report("hot")

    def test_none_temperature(self):
        record = LocalRecord((1, 2))
        with self.assertRaises(TypeError):
            record.add_report(None)

    def test_zero_capacity(self):
        with self.assertRaises((ZeroDivisionError, ZeroDivisionError)):
            records = RecordsMap(0)
            records.add_report((1, 2), 20)

    def test_negative_capacity(self):
        with self.assertRaises((ZeroDivisionError, IndexError)):
            records = RecordsMap(-1)
            records.add_report((1, 2), 20)

    def test_non_integer_capacity(self):
        with self.assertRaises((TypeError, IndexError)):
            RecordsMap(2.5)

    def test_invalid_position_add_report(self):
        with self.assertRaises((TypeError, IndexError)):
            self.records = RecordsMap()
            self.records.add_report((), 20)

    def test_invalid_position_getitem(self):
        records = RecordsMap()
        with self.assertRaises((TypeError, IndexError)):
            records[()]

    def test_invalid_position_contains(self):
        records = RecordsMap()
        with self.assertRaises((TypeError, IndexError)):
            () in records

    def test_nan_temperature(self):
        records = RecordsMap()
        records.add_report((1, 2), float("nan"))

        self.assertTrue((1, 2) in records)

    def test_infinite_temperature(self):
        records = RecordsMap()
        records.add_report((1, 2), float("inf"))

        self.assertEqual(records[(1, 2)], (float("inf"), float("inf")))

    def test_nan_coordinates(self):
        records = RecordsMap()
        with self.assertRaises((ValueError, OverflowError)):
            records.add_report((float("nan"), 2), 20)

    def test_infinite_coordinates(self):
        records = RecordsMap()
        with self.assertRaises((OverflowError, ValueError)):
            records.add_report((float("inf"), 2), 20)


if __name__ == "__main__":
    unittest.main()