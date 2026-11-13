import unittest
from RecordsMap import LocalRecord, RecordsMap

class TestLocalRecord(unittest.TestCase):
    def test_init_default_precision(self):
        record = LocalRecord((1.6, 2.4), max=10, min=5)
        self.assertEqual(record.pos, (2, 2))
        self.assertEqual(record.max, 10)
        self.assertEqual(record.min, 5)
        self.assertEqual(record.precision, 0)

    def test_init_custom_precision(self):
        record = LocalRecord((1.567, 2.433), max=20, min=10, precision=2)
        self.assertEqual(record.pos, (1.57, 2.43))
        self.assertEqual(record.precision, 2)

    def test_add_report_updates(self):
        record = LocalRecord((1.0, 1.0), max=15, min=15)
        record.add_report(20)
        self.assertEqual(record.max, 20)
        self.assertEqual(record.min, 15)

        record.add_report(10)
        self.assertEqual(record.max, 20)
        self.assertEqual(record.min, 10)

    def test_equality(self):
        r1 = LocalRecord((1.0, 2.0))
        r2 = LocalRecord((1.0, 2.0))
        r3 = LocalRecord((3.0, 4.0))
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)
        self.assertNotEqual(r1, "not a record")

    def test_hash(self):
        r1 = LocalRecord((1.0, 2.0))
        r2 = LocalRecord((1.0, 2.0))
        self.assertEqual(hash(r1), hash(r2))

    def test_repr(self):
        record = LocalRecord((1.0, 2.0), max=30, min=10)
        self.assertEqual(repr(record), "Record(pos=(1, 2), max=30, min=10)")


class TestRecordsMap(unittest.TestCase):
    def test_init(self):
        rmap = RecordsMap(capacity=4)
        self.assertEqual(rmap.capacity, 4)
        self.assertEqual(len(rmap), 0)

    def test_add_and_contains(self):
        rmap = RecordsMap(capacity=8)
        self.assertFalse((1.0, 1.0) in rmap)
        
        rmap.add_report((1.0, 1.0), 22)
        self.assertTrue((1.0, 1.0) in rmap)
        self.assertEqual(len(rmap), 1)

    def test_getitem_success(self):
        rmap = RecordsMap(capacity=8)
        rmap.add_report((1.2, 1.8), 15)
        rmap.add_report((1.2, 1.8), 25)
        rmap.add_report((1.2, 1.8), 10)

        min_val, max_val = rmap[(1.2, 1.8)]
        self.assertEqual(min_val, 10)
        self.assertEqual(max_val, 25)

    def test_getitem_key_error(self):
        rmap = RecordsMap(capacity=8)
        with self.assertRaises(KeyError):
            _ = rmap[(5.0, 5.0)]

    def test_rehash_trigger(self):
        # Capacity = 4, threshold = 0.7. Max size before rehash = 2.
        rmap = RecordsMap(capacity=4)
        rmap.add_report((1.0, 1.0), 10)
        rmap.add_report((2.0, 2.0), 20)
        self.assertEqual(rmap.capacity, 4)
        
        # Adding a 3rd item triggers rehash (3/4 = 0.75 > 0.7)
        rmap.add_report((3.0, 3.0), 30)
        self.assertEqual(rmap.capacity, 8)
        self.assertEqual(len(rmap), 3)
        self.assertTrue((1.0, 1.0) in rmap)
        self.assertTrue((2.0, 2.0) in rmap)
        self.assertTrue((3.0, 3.0) in rmap)
        self.assertEqual(rmap[(1.0, 1.0)], (10, 10))
        self.assertEqual(rmap[(2.0, 2.0)], (20, 20))
        self.assertEqual(rmap[(3.0, 3.0)], (30, 30))

if __name__ == '__main__':
    unittest.main()