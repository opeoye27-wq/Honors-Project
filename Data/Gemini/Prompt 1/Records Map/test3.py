import unittest
from RecordsMap import LocalRecord, RecordsMap

class TestLocalRecord(unittest.TestCase):
    def test_init_default_precision(self):
        record = LocalRecord((1.2, 3.8))
        self.assertEqual(record.pos, (1, 4))
        self.assertIsNone(record.max)
        self.assertIsNone(record.min)
        self.assertEqual(record.precision, 0)

    def test_init_custom_precision(self):
        record = LocalRecord((1.234, 3.876), max=10, min=5, precision=2)
        self.assertEqual(record.pos, (1.23, 3.88))
        self.assertEqual(record.max, 10)
        self.assertEqual(record.min, 5)
        self.assertEqual(record.precision, 2)

    def test_add_report(self):
        record = LocalRecord((0, 0), max=10, min=5)
        record.add_report(12)
        self.assertEqual(record.max, 12)
        self.assertEqual(record.min, 5)
        
        record.add_report(2)
        self.assertEqual(record.max, 12)
        self.assertEqual(record.min, 2)

    def test_equality(self):
        r1 = LocalRecord((1.1, 2.2))
        r2 = LocalRecord((1.4, 2.4))  # rounds to (1, 2) with default precision 0
        r3 = LocalRecord((5.0, 5.0))
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)
        self.assertNotEqual(r1, "NotARecord")

    def test_hash(self):
        r1 = LocalRecord((1.1, 2.2))
        r2 = LocalRecord((1.4, 2.4))
        self.assertEqual(hash(r1), hash(r2))

    def test_repr(self):
        record = LocalRecord((1, 2), max=20, min=10)
        self.assertEqual(repr(record), "Record(pos=(1, 2), max=20, min=10)")


class TestRecordsMap(unittest.TestCase):
    def test_init(self):
        rm = RecordsMap(capacity=4)
        self.assertEqual(rm.capacity, 4)
        self.assertEqual(len(rm), 0)

    def test_add_report_and_getitem(self):
        rm = RecordsMap(capacity=8)
        rm.add_report((1.0, 2.0), 25)
        self.assertIn((1.0, 2.0), rm)
        self.assertEqual(len(rm), 1)
        self.assertEqual(rm[(1.0, 2.0)], (25, 25))

    def test_update_report(self):
        rm = RecordsMap(capacity=8)
        rm.add_report((1.0, 2.0), 20)
        rm.add_report((1.0, 2.0), 30)
        rm.add_report((1.0, 2.0), 10)
        self.assertEqual(len(rm), 1)
        self.assertEqual(rm[(1.0, 2.0)], (10, 30))

    def test_getitem_key_error(self):
        rm = RecordsMap(capacity=8)
        with self.assertRaises(KeyError):
            _ = rm[(5.0, 5.0)]

    def test_contains(self):
        rm = RecordsMap(capacity=8)
        rm.add_report((3.4, 4.6), 15)
        self.assertTrue((3.4, 4.6) in rm)
        self.assertFalse((10.0, 10.0) in rm)

    def test_rehash_trigger(self):
        # Capacity is 4, load factor threshold is 0.7.
        # Adding 3 items results in size/capacity = 3/4 = 0.75 > 0.7, triggering rehash.
        rm = RecordsMap(capacity=4)
        rm.add_report((1.0, 1.0), 10)
        rm.add_report((2.0, 2.0), 20)
        rm.add_report((3.0, 3.0), 30)
        self.assertIn((1.0, 1.0), rm)
        self.assertIn((2.0, 2.0), rm)
        self.assertIn((3.0, 3.0), rm)

    def test_negative_coordinates(self):
        rm = RecordsMap(capacity=8)
        rm.add_report((-1.5, -2.5), 10)
        self.assertIn((-1.5, -2.5), rm)
        self.assertEqual(rm[(-1.5, -2.5)], (10, 10))


if __name__ == '__main__':
    unittest.main()