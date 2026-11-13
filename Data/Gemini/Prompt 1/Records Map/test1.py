import unittest
from RecordsMap import LocalRecord, RecordsMap


class TestLocalRecord(unittest.TestCase):
    def test_init_default_precision(self):
        record = LocalRecord((1.4, 2.6))
        self.assertEqual(record.pos, (1, 3))
        self.assertIsNone(record.max)
        self.assertIsNone(record.min)

    def test_init_custom_precision(self):
        record = LocalRecord((1.456, 2.432), max=10, min=2, precision=2)
        self.assertEqual(record.pos, (1.46, 2.43))
        self.assertEqual(record.max, 10)
        self.assertEqual(record.min, 2)

    def test_add_report_updates_min_max(self):
        record = LocalRecord((0, 0), max=10, min=5)

        # Test higher temperature updates max
        record.add_report(15)
        self.assertEqual(record.max, 15)
        self.assertEqual(record.min, 5)

        # Test lower temperature updates min
        record.add_report(2)
        self.assertEqual(record.max, 15)
        self.assertEqual(record.min, 2)

        # Test intermediate temperature leaves min/max unchanged
        record.add_report(8)
        self.assertEqual(record.max, 15)
        self.assertEqual(record.min, 2)

    def test_equality(self):
        r1 = LocalRecord((1.0, 2.0))
        r2 = LocalRecord((1.4, 2.4))  # Rounds to (1, 2) with precision 0
        r3 = LocalRecord((3.0, 4.0))

        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)
        self.assertNotEqual(r1, "not a record")

    def test_hash_consistency(self):
        r1 = LocalRecord((1.0, 2.0))
        r2 = LocalRecord((1.4, 2.4))
        self.assertEqual(hash(r1), hash(r2))

    def test_repr(self):
        record = LocalRecord((1.0, 2.0), max=25, min=10)
        self.assertEqual(repr(record), "Record(pos=(1, 2), max=25, min=10)")


class TestRecordsMap(unittest.TestCase):
    def test_init(self):
        rm = RecordsMap(capacity=4)
        self.assertEqual(rm.capacity, 4)
        self.assertEqual(len(rm), 0)

    def test_add_report_and_getitem(self):
        rm = RecordsMap()
        rm.add_report((1.2, 3.8), 20)

        self.assertIn((1.2, 3.8), rm)
        self.assertEqual(len(rm), 1)
        self.assertEqual(rm[(1.2, 3.8)], (20, 20))

    def test_multiple_reports_same_position(self):
        rm = RecordsMap()
        pos = (5.1, 5.9)
        rm.add_report(pos, 15)
        rm.add_report(pos, 30)
        rm.add_report(pos, 5)

        self.assertEqual(len(rm), 1)
        self.assertEqual(rm[pos], (5, 30))

    def test_missing_key_raises_key_error(self):
        rm = RecordsMap()
        self.assertNotIn((0, 0), rm)
        with self.assertRaises(KeyError):
            _ = rm[(0, 0)]

    def test_rehash_trigger(self):
        # Initial capacity = 4, threshold = 4 * 0.7 = 2.8 (size > 2 triggers rehash)
        rm = RecordsMap(capacity=4)
        self.assertEqual(rm.capacity, 4)

        rm.add_report((1, 1), 10)
        rm.add_report((2, 2), 15)
        self.assertEqual(rm.capacity, 4)  # Size is 2, no rehash yet

        rm.add_report((3, 3), 20)  # Size becomes 3, exceeds threshold
        self.assertEqual(rm.capacity, 8)  # Capacity should double to 8
        self.assertEqual(len(rm), 3)
        self.assertIn((1, 1), rm)
        self.assertIn((2, 2), rm)
        self.assertIn((3, 3), rm)

    def test_negative_coordinates_and_temperatures(self):
        rm = RecordsMap()
        pos = (-1.2, -3.7)
        rm.add_report(pos, -10)
        rm.add_report(pos, 5)
        rm.add_report(pos, -25)

        self.assertIn(pos, rm)
        self.assertEqual(rm[pos], (-25, 5))


if __name__ == '__main__':
    unittest.main()