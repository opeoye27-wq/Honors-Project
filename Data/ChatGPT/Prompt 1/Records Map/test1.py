import unittest

# Import LocalRecord and RecordsMap from the original module if necessary.
from RecordsMap import LocalRecord, RecordsMap


class TestLocalRecord(unittest.TestCase):
    """Unit tests for the LocalRecord class."""

    def test_initialization(self):
        record = LocalRecord((10.25, 20.75), 85, 40)
        self.assertEqual(record.pos, (10, 21))
        self.assertEqual(record.max, 85)
        self.assertEqual(record.min, 40)

    def test_default_initialization(self):
        record = LocalRecord((1.5, 2.5))
        self.assertEqual(record.pos, (2, 2))
        self.assertIsNone(record.max)
        self.assertIsNone(record.min)

    def test_custom_precision(self):
        record = LocalRecord((1.23456, 2.98765), precision=3)
        self.assertEqual(record.pos, (1.235, 2.988))

    def test_zero_precision(self):
        record = LocalRecord((1.6, 2.4), precision=0)
        self.assertEqual(record.pos, (2, 2))

    def test_negative_coordinates(self):
        record = LocalRecord((-1.6, -2.4))
        self.assertEqual(record.pos, (-2, -2))

    def test_negative_precision(self):
        record = LocalRecord((123.45, 678.91), precision=-1)
        self.assertEqual(record.pos, (120.0, 680.0))

    def test_add_first_report(self):
        record = LocalRecord((1, 2))
        record.add_report(50)
        self.assertEqual(record.min, 50)
        self.assertEqual(record.max, 50)

    def test_add_larger_report(self):
        record = LocalRecord((1, 2), 50, 50)
        record.add_report(80)
        self.assertEqual(record.max, 80)
        self.assertEqual(record.min, 50)

    def test_add_smaller_report(self):
        record = LocalRecord((1, 2), 80, 50)
        record.add_report(20)
        self.assertEqual(record.max, 80)
        self.assertEqual(record.min, 20)

    def test_add_middle_report(self):
        record = LocalRecord((1, 2), 80, 20)
        record.add_report(50)
        self.assertEqual(record.max, 80)
        self.assertEqual(record.min, 20)

    def test_add_duplicate_report(self):
        record = LocalRecord((1, 2), 50, 50)
        record.add_report(50)
        self.assertEqual(record.min, 50)
        self.assertEqual(record.max, 50)

    def test_add_zero_temperature(self):
        record = LocalRecord((1, 2))
        record.add_report(0)
        self.assertEqual(record.min, 0)
        self.assertEqual(record.max, 0)

    def test_add_negative_temperature(self):
        record = LocalRecord((1, 2))
        record.add_report(-15)
        self.assertEqual(record.min, -15)
        self.assertEqual(record.max, -15)

    def test_equality_same_position(self):
        first = LocalRecord((1.2, 2.3))
        second = LocalRecord((1.4, 2.4))
        self.assertEqual(first, second)

    def test_inequality_different_position(self):
        first = LocalRecord((1, 2))
        second = LocalRecord((3, 4))
        self.assertNotEqual(first, second)

    def test_inequality_different_type(self):
        record = LocalRecord((1, 2))
        self.assertNotEqual(record, (1, 2))
        self.assertNotEqual(record, None)
        self.assertNotEqual(record, "record")

    def test_hash_equal_records(self):
        first = LocalRecord((1.2, 2.3))
        second = LocalRecord((1.4, 2.4))
        self.assertEqual(hash(first), hash(second))

    def test_hash_usable_in_set(self):
        first = LocalRecord((1, 2))
        second = LocalRecord((1.1, 2.1))
        records = {first, second}
        self.assertEqual(len(records), 1)

    def test_repr(self):
        record = LocalRecord((1, 2), 80, 20)
        self.assertEqual(
            repr(record),
            "Record(pos=(1, 2), max=80, min=20)"
        )


class TestRecordsMap(unittest.TestCase):
    """Unit tests for the RecordsMap hash table."""

    def setUp(self):
        self.records = RecordsMap()

    def test_default_initialization(self):
        self.assertEqual(self.records.capacity, 8)
        self.assertEqual(len(self.records), 0)
        self.assertEqual(len(self.records.table), 8)

    def test_custom_capacity(self):
        records = RecordsMap(16)
        self.assertEqual(records.capacity, 16)
        self.assertEqual(len(records.table), 16)
        self.assertEqual(len(records), 0)

    def test_empty_table(self):
        self.assertEqual(len(self.records), 0)
        self.assertNotIn((1, 2), self.records)

    def test_add_single_report(self):
        self.records.add_report((1, 2), 50)
        self.assertEqual(len(self.records), 1)
        self.assertIn((1, 2), self.records)
        self.assertEqual(self.records[(1, 2)], (50, 50))

    def test_add_multiple_positions(self):
        positions = [
            ((1, 2), 30),
            ((3, 4), 40),
            ((5, 6), 50)
        ]

        for pos, temp in positions:
            self.records.add_report(pos, temp)

        self.assertEqual(len(self.records), 3)

        for pos, temp in positions:
            self.assertEqual(self.records[pos], (temp, temp))

    def test_update_maximum_temperature(self):
        self.records.add_report((1, 2), 50)
        self.records.add_report((1, 2), 80)

        self.assertEqual(len(self.records), 1)
        self.assertEqual(self.records[(1, 2)], (50, 80))

    def test_update_minimum_temperature(self):
        self.records.add_report((1, 2), 50)
        self.records.add_report((1, 2), 20)

        self.assertEqual(len(self.records), 1)
        self.assertEqual(self.records[(1, 2)], (20, 50))

    def test_update_with_middle_temperature(self):
        self.records.add_report((1, 2), 20)
        self.records.add_report((1, 2), 80)
        self.records.add_report((1, 2), 50)

        self.assertEqual(self.records[(1, 2)], (20, 80))
        self.assertEqual(len(self.records), 1)

    def test_update_with_duplicate_temperature(self):
        self.records.add_report((1, 2), 50)
        self.records.add_report((1, 2), 50)

        self.assertEqual(self.records[(1, 2)], (50, 50))
        self.assertEqual(len(self.records), 1)

    def test_multiple_negative_temperatures(self):
        self.records.add_report((1, 2), -10)
        self.records.add_report((1, 2), -30)
        self.records.add_report((1, 2), -5)

        self.assertEqual(self.records[(1, 2)], (-30, -5))

    def test_zero_temperature(self):
        self.records.add_report((1, 2), 0)
        self.assertEqual(self.records[(1, 2)], (0, 0))

    def test_negative_coordinates(self):
        self.records.add_report((-5, -10), 30)
        self.assertIn((-5, -10), self.records)
        self.assertEqual(self.records[(-5, -10)], (30, 30))

    def test_decimal_coordinates_rounding(self):
        self.records.add_report((1.2, 2.3), 40)

        self.assertIn((1.4, 2.4), self.records)
        self.assertEqual(self.records[(1.4, 2.4)], (40, 40))

    def test_rounding_boundary(self):
        self.records.add_report((1.49, 2.49), 40)
        self.records.add_report((1.50, 2.50), 60)

        self.assertEqual(len(self.records), 2)
        self.assertEqual(self.records[(1.49, 2.49)], (40, 40))
        self.assertEqual(self.records[(1.50, 2.50)], (60, 60))

    def test_rounding_same_position(self):
        self.records.add_report((1.1, 2.1), 30)
        self.records.add_report((1.4, 2.4), 70)

        self.assertEqual(len(self.records), 1)
        self.assertEqual(self.records[(1.1, 2.1)], (30, 70))

    def test_contains_existing_position(self):
        self.records.add_report((1, 2), 50)
        self.assertTrue((1, 2) in self.records)

    def test_contains_missing_position(self):
        self.records.add_report((1, 2), 50)
        self.assertFalse((3, 4) in self.records)

    def test_contains_rounded_position(self):
        self.records.add_report((1.1, 2.1), 50)
        self.assertIn((1.4, 2.4), self.records)

    def test_getitem_existing_position(self):
        self.records.add_report((10, 20), 75)
        self.assertEqual(self.records[(10, 20)], (75, 75))

    def test_getitem_missing_position(self):
        with self.assertRaises(KeyError):
            self.records[(100, 200)]

    def test_getitem_empty_table(self):
        with self.assertRaises(KeyError):
            self.records[(1, 2)]

    def test_multiple_updates_preserve_size(self):
        self.records.add_report((1, 2), 10)

        for temp in range(20, 101, 10):
            self.records.add_report((1, 2), temp)

        self.assertEqual(len(self.records), 1)
        self.assertEqual(self.records[(1, 2)], (10, 100))

    def test_collisions(self):
        records = RecordsMap(capacity=2)

        positions = [(1, 1), (2, 2), (3, 3)]

        for i, pos in enumerate(positions):
            records.add_report(pos, i * 10)

        self.assertEqual(len(records), 3)

        for i, pos in enumerate(positions):
            self.assertIn(pos, records)
            self.assertEqual(records[pos], (i * 10, i * 10))

    def test_rehash_trigger(self):
        records = RecordsMap(capacity=4)

        for i in range(3):
            records.add_report((i, i), i * 10)

        self.assertEqual(records.capacity, 4)

        records.add_report((3, 3), 30)

        self.assertEqual(records.capacity, 8)
        self.assertEqual(len(records), 4)

    def test_rehash_preserves_all_records(self):
        records = RecordsMap(capacity=4)

        expected = {}

        for i in range(20):
            pos = (i * 10, i * 5)
            temp = i * 3
            records.add_report(pos, temp)
            expected[pos] = (temp, temp)

        self.assertGreater(records.capacity, 4)
        self.assertEqual(len(records), len(expected))

        for pos, temps in expected.items():
            self.assertEqual(records[pos], temps)

    def test_rehash_preserves_min_and_max(self):
        records = RecordsMap(capacity=4)

        records.add_report((1, 1), 20)
        records.add_report((1, 1), 80)
        records.add_report((1, 1), 50)

        for i in range(2, 10):
            records.add_report((i, i), i * 10)

        self.assertEqual(records[(1, 1)], (20, 80))

    def test_rehash_preserves_negative_temperatures(self):
        records = RecordsMap(capacity=2)

        records.add_report((1, 1), -50)
        records.add_report((1, 1), -10)

        for i in range(2, 10):
            records.add_report((i, i), i)

        self.assertEqual(records[(1, 1)], (-50, -10))

    def test_repeated_rehashing(self):
        records = RecordsMap(capacity=2)

        for i in range(100):
            records.add_report((i, i + 1), i)

        self.assertEqual(len(records), 100)

        for i in range(100):
            self.assertEqual(records[(i, i + 1)], (i, i))

    def test_rehash_updates_size_correctly(self):
        records = RecordsMap(capacity=2)

        for i in range(50):
            records.add_report((i, i), i)

        self.assertEqual(len(records), 50)

        unique_positions = set()

        for bucket in records.table:
            for record in bucket:
                unique_positions.add(record.pos)

        self.assertEqual(len(unique_positions), 50)

    def test_rehash_with_multiple_reports_at_same_position(self):
        records = RecordsMap(capacity=2)

        records.add_report((1, 1), 10)
        records.add_report((1, 1), 90)

        for i in range(2, 15):
            records.add_report((i, i), i)

        self.assertEqual(len(records), 14)
        self.assertEqual(records[(1, 1)], (10, 90))

    def test_large_number_of_reports(self):
        records = RecordsMap()

        for i in range(1000):
            records.add_report((i, i), i)

        self.assertEqual(len(records), 1000)

        for i in range(1000):
            self.assertEqual(records[(i, i)], (i, i))

    def test_add_float_temperatures(self):
        self.records.add_report((1, 2), 12.5)
        self.records.add_report((1, 2), 18.75)

        self.assertEqual(self.records[(1, 2)], (12.5, 18.75))

    def test_add_identical_coordinates_after_rehash(self):
        records = RecordsMap(capacity=2)

        records.add_report((1.1, 2.1), 10)

        for i in range(2, 10):
            records.add_report((i, i), i)

        records.add_report((1.4, 2.4), 100)

        self.assertEqual(records[(1.1, 2.1)], (10, 100))
        self.assertEqual(len(records), 9)


class TestInvalidInputs(unittest.TestCase):
    """Tests for invalid and unusual inputs."""

    def test_invalid_position_length_in_local_record(self):
        with self.assertRaises((IndexError, TypeError)):
            LocalRecord((1,))

    def test_empty_position_in_local_record(self):
        with self.assertRaises((IndexError, TypeError)):
            LocalRecord(())

    def test_none_position_in_local_record(self):
        with self.assertRaises(TypeError):
            LocalRecord(None)

    def test_invalid_position_length_in_map(self):
        records = RecordsMap()

        with self.assertRaises((IndexError, TypeError)):
            records.add_report((1,), 50)

    def test_empty_position_in_map(self):
        records = RecordsMap()

        with self.assertRaises((IndexError, TypeError)):
            records.add_report((), 50)

    def test_none_position_in_map(self):
        records = RecordsMap()

        with self.assertRaises(TypeError):
            records.add_report(None, 50)

    def test_string_position(self):
        records = RecordsMap()

        with self.assertRaises((TypeError, ValueError)):
            records.add_report(("north", "south"), 50)

    def test_non_numeric_coordinate(self):
        records = RecordsMap()

        with self.assertRaises(TypeError):
            records.add_report(("1", 2), 50)

    def test_nan_coordinate(self):
        records = RecordsMap()
        records.add_report((float("nan"), 2), 50)

        self.assertEqual(len(records), 1)

    def test_infinite_coordinate(self):
        records = RecordsMap()

        with self.assertRaises((OverflowError, ValueError)):
            records.add_report((float("inf"), 2), 50)

    def test_invalid_capacity_zero(self):
        records = RecordsMap(0)

        with self.assertRaises(ZeroDivisionError):
            records.add_report((1, 2), 50)

    def test_negative_capacity(self):
        records = RecordsMap(-1)

        self.assertEqual(records.capacity, -1)

        with self.assertRaises((ZeroDivisionError, IndexError)):
            records.add_report((1, 2), 50)

    def test_non_integer_capacity(self):
        with self.assertRaises((TypeError, OverflowError)):
            RecordsMap("invalid")

    def test_none_capacity(self):
        with self.assertRaises(TypeError):
            RecordsMap(None)

    def test_invalid_precision(self):
        with self.assertRaises(TypeError):
            LocalRecord((1, 2), precision="invalid")

    def test_none_precision(self):
        with self.assertRaises(TypeError):
            LocalRecord((1, 2), precision=None)

    def test_invalid_temperature_string(self):
        records = RecordsMap()
        records.add_report((1, 2), 50)

        with self.assertRaises(TypeError):
            records.add_report((1, 2), "hot")

    def test_invalid_temperature_none(self):
        records = RecordsMap()
        records.add_report((1, 2), None)

        with self.assertRaises(TypeError):
            records.add_report((1, 2), 50)

    def test_incomparable_temperature_types(self):
        records = RecordsMap()
        records.add_report((1, 2), 50)

        with self.assertRaises(TypeError):
            records.add_report((1, 2), "60")

    def test_boolean_temperature(self):
        records = RecordsMap()
        records.add_report((1, 2), True)
        records.add_report((1, 2), False)

        self.assertEqual(records[(1, 2)], (False, True))

    def test_nan_temperature(self):
        records = RecordsMap()
        records.add_report((1, 2), float("nan"))

        self.assertEqual(len(records), 1)

    def test_infinite_temperature(self):
        records = RecordsMap()

        records.add_report((1, 2), float("inf"))
        records.add_report((1, 2), float("-inf"))

        self.assertEqual(
            records[(1, 2)],
            (float("-inf"), float("inf"))
        )

    def test_invalid_getitem_position(self):
        records = RecordsMap()

        with self.assertRaises((TypeError, IndexError)):
            records[None]

    def test_invalid_contains_position(self):
        records = RecordsMap()

        with self.assertRaises((TypeError, IndexError)):
            None in records

    def test_invalid_rehash_capacity_zero(self):
        records = RecordsMap()

        with self.assertRaises((ZeroDivisionError, TypeError)):
            records._rehash(0)

    def test_rehash_negative_capacity(self):
        records = RecordsMap()

        with self.assertRaises((IndexError, ZeroDivisionError)):
            records._rehash(-1)


if __name__ == "__main__":
    unittest.main()