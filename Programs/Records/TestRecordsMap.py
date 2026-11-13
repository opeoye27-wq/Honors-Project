# Import what you need
# Include unittests here. Focus on readability, including comments and docstrings.
import unittest
from RecordsMap import LocalRecord, RecordsMap

class TestLocalRecord(unittest.TestCase):
    def test_init(self):
        """testing the initializer"""
        record1 = LocalRecord((41.23567, 42.67834))
        self.assertTupleEqual(record1.pos, (41, 43))
        self.assertEqual(record1.min, None)
        self.assertEqual(record1.max, None)
        self.assertEqual(record1.precision, 0)

        record2 = LocalRecord((32.63458, -62.7985), max = 48)
        self.assertTupleEqual(record2.pos, (33, -63))
        self.assertEqual(record2.min, None)
        self.assertEqual(record2.max, 48)
        self.assertEqual(record1.precision, 0)

        record3 = LocalRecord((48.98754, -32.1456), min = 43, max = 87, precision =2)
        self.assertTupleEqual(record3.pos, (48.99, -32.15))
        self.assertEqual(record3.min, 43)
        self.assertEqual(record3.max, 87)
        self.assertEqual(record3.precision, 2)


    def test_hash(self):
        """testing the hash function"""
        record1 = LocalRecord((41.23567, 42.67834))
        hash_rec1 = record1.__hash__()
        self.assertEqual(hash(record1.pos), hash_rec1)

        record2 = LocalRecord((32.63458, -62.7985))
        hash_rec2 = record2.__hash__()
        self.assertEqual(hash(record2.pos), hash_rec2)


    def test_eq(self):
        """testing the equal instance function"""
        record1 = LocalRecord((41.53567, 42.67834))
        record2 = LocalRecord((41.5326, 43.174643))
        self.assertIsInstance(record1, LocalRecord) and self.assertIsInstance(record2, LocalRecord)
        self.assertEqual(record1.pos, record2.pos)
        self.assertTrue(record1.__eq__(record2))

        record3 = LocalRecord((35.2378, 45.7865))
        self.assertIsInstance(record3, LocalRecord) 
        self.assertNotEqual(record1.pos, record3.pos)
        self.assertFalse(record3.__eq__(record1))

    def test_add_report(self):
        """testing adding a report function"""
        record1 = LocalRecord((41.23567, 42.67834))
        record1.add_report(55)
        self.assertEqual(record1.min, 55)
        self.assertEqual(record1.max, 55)

        record2 = LocalRecord((32.63458, -62.7985), min = 45, max =67)
        record2.add_report(57)
        self.assertEqual(record2.min, 45)
        self.assertEqual(record2.max, 67)

        record3 = LocalRecord((48.98754, -32.1456), min = 36, max = 47)
        record3.add_report(52)
        self.assertEqual(record3.min, 36)
        self.assertEqual(record3.max, 52)



class TestRecordsMap(unittest.TestCase):
    def test_add_one_report(self):
        """Testing adding only one report Remember to test len, get, contains, and add_report"""
        map = RecordsMap()
        #initialized values
        self.assertEqual(map.capacity, 8)
        self.assertEqual(map.size, 0)
        #adding a value
        map.add_report((35.2378, 45.7865), 57)
        self.assertEqual(1, map.size)
        #hashing for index
        index = map._hash((35.2378, 45.7865))
        self.assertEqual(index, hash((round(35.2378), round(45.7865))) % map.capacity)
        #checking len
        self.assertEqual(map.__len__(), 1)
        #checking get
        self.assertTupleEqual(map.__getitem__((35.2378, 45.7865)), (57,57))
        with self.assertRaises(KeyError):
            map.__getitem__((12.7856, 89.2469))
        #checking contains
        self.assertTrue(map.__contains__((35.2378, 45.7865)))
        self.assertFalse(map.__contains__((18.9754, 78.6548)))


    def test_add_many_reports(self):
        """testing adding multiple reports. Remember to test len, get, contains, and add_report"""
        map = RecordsMap()
        self.assertEqual(map.capacity, 8)
        self.assertEqual(map.size, 0)
        #adding values
        map.add_report((35.2378, 45.7865), 57)
        index1 = map._hash((35.2378, 45.7865))
        self.assertEqual(index1, hash((round(35.2378), round(45.7865))) % map.capacity)
        self.assertEqual(map.__len__(), 1)
        self.assertTupleEqual(map.__getitem__((35.2378, 45.7865)), (57, 57))
        self.assertTrue(map.__contains__((35.2378, 45.7865)))

        map.add_report((32.63458, -62.7985), 38)
        index2 = map._hash((32.63458, -62.7985))
        self.assertEqual(index2, hash((round(32.63458), round(-62.7985))) % map.capacity)
        self.assertEqual(map.__len__(), 2)
        self.assertTupleEqual(map.__getitem__((32.63458, -62.7985)), (38, 38))
        self.assertTrue(map.__contains__((32.63458, -62.7985)))

        map.add_report((48.98754, -32.1456), 49)
        index3 = map._hash((48.98754, -32.1456))
        self.assertEqual(index3, hash((round(48.98754), round(-32.1456))) % map.capacity)
        self.assertEqual(map.__len__(), 3)
        self.assertTupleEqual(map.__getitem__((48.98754, -32.1456)), (49, 49))
        self.assertTrue(map.__contains__((48.98754, -32.1456)))
        

# You need to add a line here to run the unittests
if __name__ == "__main__":
    unittest.main()