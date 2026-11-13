import pytest
from RecordsMap import RecordsMap

# Assuming the implementation class is named RecordsMap
# from RecordsMap import RecordsMap

def test_empty_table():
    table = RecordsMap()
    assert len(table) == 0
    assert (0.0, 0.0) not in table
    with pytest.raises(KeyError):
        table[(0.0, 0.0)]

def test_single_insertion_and_lookup():
    table = RecordsMap()
    table.add_report((1.5, 2.5), 22.5)
    assert len(table) == 1
    assert (1.5, 2.5) in table
    assert table[(1.5, 2.5)] == (22.5, 22.5)

def test_negative_and_zero_temperatures():
    table = RecordsMap()
    table.add_report((0.0, 0.0), 0.0)
    table.add_report((1.0, 2.0), -10.5)

    assert table[(0.0, 0.0)] == (0.0, 0.0)
    assert table[(1.0, 2.0)] == (-10.5, -10.5)

def test_repeated_reports_and_min_max_updates():
    table = RecordsMap()
    pos = (10.0, 20.0)

    # Initial report
    table.add_report(pos, 15.0)
    assert table[pos] == (15.0, 15.0)

    # Report lower temperature (should update minimum)
    table.add_report(pos, 5.0)
    assert table[pos] == (5.0, 15.0)

    # Report higher temperature (should update maximum)
    table.add_report(pos, 30.0)
    assert table[pos] == (5.0, 30.0)

    # Report intermediate temperature (should not change min or max)
    table.add_report(pos, 20.0)
    assert table[pos] == (5.0, 30.0)

    # Unique count should remain 1
    assert len(table) == 1

def test_coordinate_rounding():
    table = RecordsMap()
    # (1.2, 3.4) rounds to (1, 3)
    table.add_report((1.2, 3.4), 10.0)
    assert len(table) == 1

    # (1.8, 3.1) also rounds to (2, 3) - different rounded position
    table.add_report((1.8, 3.1), 20.0)
    assert len(table) == 2

    # (1.4, 3.4) rounds to (1, 3) - should update the existing record at (1, 3)
    table.add_report((1.4, 3.4), 40.0)
    assert len(table) == 2

    assert table[(1.0, 3.0)] == (10.0, 40.0)
    assert table[(2.0, 3.0)] == (20.0, 20.0)

def test_missing_positions():
    table = RecordsMap()
    table.add_report((5.0, 5.0), 12.0)

    assert (6.0, 6.0) not in table
    with pytest.raises(KeyError):
        table[(6.0, 6.0)]

def test_resizing_and_load_factor():
    table = RecordsMap()
    inserted_data = []

    # Insert enough items to trigger resizing (load factor > 0.7)
    for i in range(25):
        pos = (float(i), float(i))
        temp = float(i * 5)
        table.add_report(pos, temp)
        inserted_data.append((pos, temp))

    assert len(table) == 25

    # Verify all records, unique count, and min/max temperatures are preserved after resizing
    for pos, temp in inserted_data:
        assert pos in table
        assert table[pos] == (temp, temp)

def test_hash_collisions_and_preservation():
    table = RecordsMap()
    # Insert multiple distinct positions that may cause hash collisions
    positions = [
        (1.0, 1.0),
        (2.0, 2.0),
        (3.0, 3.0),
        (4.0, 4.0),
        (5.0, 5.0)
    ]

    for pos in positions:
        table.add_report(pos, 50.0)

    assert len(table) == len(positions)

    # Update each position with secondary temperatures
    for i, pos in enumerate(positions):
        table.add_report(pos, float(i + 10))
        table.add_report(pos, float(i + 100))

    # Verify records remain intact and separate despite potential collisions
    for i, pos in enumerate(positions):
        expected_min = float(i + 10)
        expected_max = 100.0 if (i + 100) > 50.0 else 50.0
        assert table[pos] == (expected_min, expected_max)

    assert len(table) == len(positions)