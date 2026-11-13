"""
Assumed API for the RecordsMap under test:
- Class: RecordsMap()
- Methods:
    - add_report(position: tuple[float, float], temperature: float) -> None
    - __getitem__(position: tuple[float, float]) -> tuple[float, float] (returns (min_temp, max_temp))
    - __contains__(position: tuple[float, float]) -> bool
    - __len__() -> int (returns number of unique positions stored)
- Exceptions:
    - KeyError: Raised when looking up or accessing a position that does not exist.
- Rounding Rule:
    - Coordinates are rounded to the nearest whole number before comparison/storage.
"""

import pytest
from RecordsMap import RecordsMap

# Assuming the class can be imported from the implementation module:
# from RecordsMap import RecordsMap


@pytest.fixture
def table():
    """Fixture providing a fresh instance of RecordsMap for each test."""
    return RecordsMap()


def test_empty_table(table):
    """Test behavior of a newly initialized empty hash table."""
    assert len(table) == 0
    with pytest.raises(KeyError):
        table[(0.0, 0.0)]
    assert (0.0, 0.0) not in table


def test_single_insertion_creates_record(table):
    """Test that inserting into a missing position creates a record with min == max == temp."""
    pos = (10.5, 20.2)
    temp = 25.0

    table.add_report(pos, temp)

    assert len(table) == 1
    assert pos in table
    assert table[pos] == (25.0, 25.0)


def test_repeated_reports_update_min_max(table):
    """Test that subsequent reports at an existing position update min and max temperatures correctly."""
    pos = (5.0, 5.0)

    table.add_report(pos, 20.0)
    assert table[pos] == (20.0, 20.0)

    # Report a lower temperature
    table.add_report(pos, 10.0)
    assert table[pos] == (10.0, 20.0)

    # Report a higher temperature
    table.add_report(pos, 35.0)
    assert table[pos] == (10.0, 35.0)

    # Report a temperature within current bounds
    table.add_report(pos, 25.0)
    assert table[pos] == (10.0, 35.0)

    assert len(table) == 1


def test_negative_and_zero_temperatures(table):
    """Test handling of negative, zero, and positive temperatures."""
    pos = (0.0, 0.0)

    table.add_report(pos, 0.0)
    assert table[pos] == (0.0, 0.0)

    table.add_report(pos, -15.5)
    assert table[pos] == (-15.5, 0.0)

    table.add_report(pos, -20.0)
    assert table[pos] == (-20.0, 0.0)

    table.add_report(pos, 5.5)
    assert table[pos] == (-20.0, 5.5)


def test_coordinate_rounding_rule(table):
    """Test that coordinates rounding to the same whole number refer to the same record."""
    # (1.2, 3.4) rounds to (1, 3)
    pos1 = (1.2, 3.4)
    # (1.4, 3.1) rounds to (1, 3)
    pos2 = (1.4, 3.1)
    # (1.6, 2.7) rounds to (2, 3) - different position
    pos3 = (1.6, 2.7)

    table.add_report(pos1, 10.0)
    assert len(table) == 1
    assert pos2 in table  # Should resolve to the same record

    table.add_report(pos2, 30.0)  # Should update the same record
    assert len(table) == 1
    assert table[pos1] == (10.0, 30.0)
    assert table[pos2] == (10.0, 30.0)

    # Insert at pos3 (different rounded position)
    table.add_report(pos3, 15.0)
    assert len(table) == 2
    assert table[pos3] == (15.0, 15.0)


def test_missing_positions_raise_key_error(table):
    """Test that looking up or checking non-existent positions behaves correctly."""
    table.add_report((1.0, 1.0), 22.0)

    assert (2.0, 2.0) not in table
    with pytest.raises(KeyError):
        table[(2.0, 2.0)]


def test_hash_collisions(table):
    """Test that multiple distinct positions that may cause hash collisions are handled correctly."""
    # Inserting multiple items to ensure correct retrieval even if hash collisions occur.
    positions = [
        (float(i), float(i)) for i in range(50)
    ]

    for i, pos in enumerate(positions):
        table.add_report(pos, float(i))

    assert len(table) == 50

    for i, pos in enumerate(positions):
        assert pos in table
        assert table[pos] == (float(i), float(i))


def test_resizing_and_load_factor(table):
    """Test that capacity increases automatically when load factor exceeds 0.7, preserving all records and values."""
    # Insert enough unique positions to trigger multiple resizes (assuming initial capacity is small, e.g., 8 or 16).
    num_records = 100
    for i in range(num_records):
        pos = (float(i), float(i * 2))
        table.add_report(pos, float(i))
        table.add_report(pos, float(i + 10))  # Update max

    assert len(table) == num_records

    # Verify all records and min/max temperatures are fully preserved after resizing
    for i in range(num_records):
        pos = (float(i), float(i * 2))
        assert pos in table
        assert table[pos] == (float(i), float(i + 10))