import pytest
from RecordsMap import RecordsMap

# Assuming the implementation is imported as follows:
# from RecordsMap import RecordsMap


@pytest.fixture
def table():
    """Fixture providing a fresh instance of RecordsMap."""
    return RecordsMap()


def test_empty_table(table):
    """Test behavior of a newly initialized empty table."""
    assert len(table) == 0
    with pytest.raises(KeyError):
        table[(0.0, 0.0)]
    assert (0.0, 0.0) not in table


def test_single_insertion_and_lookup(table):
    """Test inserting a single temperature and looking it up."""
    pos = (10.5, 20.5)
    table.add_report(pos, 25.0)

    assert len(table) == 1
    assert pos in table
    assert table[pos] == (25.0, 25.0)


def test_negative_and_zero_temperatures(table):
    """Test handling of zero and negative temperatures."""
    pos = (1.0, 1.0)
    table.add_report(pos, 0.0)
    table.add_report(pos, -15.5)
    table.add_report(pos, -5.0)

    assert len(table) == 1
    assert table[pos] == (-15.5, 0.0)


def test_repeated_reports_and_bounds_updates(table):
    """Test that repeated reports correctly update min and max temperatures."""
    pos = (5.0, 5.0)
    temperatures = [10.0, 25.5, -3.2, 42.1, 15.0]

    for temp in temperatures:
        table.add_report(pos, temp)

    assert len(table) == 1
    assert table[pos] == (min(temperatures), max(temperatures))


def test_coordinate_rounding_rule(table):
    """Test that coordinates rounding to the same whole numbers share a record."""
    pos1 = (2.2, 3.8)
    pos2 = (2.4, 3.1)  # Both round to (2, 4)

    table.add_report(pos1, 10.0)
    table.add_report(pos2, 30.0)

    assert len(table) == 1
    assert pos1 in table
    assert pos2 in table
    assert table[pos1] == (10.0, 30.0)
    assert table[pos2] == (10.0, 30.0)


def test_missing_position_raises_key_error(table):
    """Test that looking up a non-existent position raises a KeyError."""
    table.add_report((1.0, 1.0), 20.0)

    with pytest.raises(KeyError):
        table[(99.0, 99.0)]


def test_existence_checks(table):
    """Test existence verification for present and absent positions."""
    pos = (4.2, 5.7)
    assert pos not in table

    table.add_report(pos, 12.3)
    assert pos in table
    assert (4.8, 5.1) in table  # Rounds to the same position (4, 6)
    assert (10.0, 10.0) not in table


def test_hash_collisions_handling(table):
    """Test that hash collisions are handled correctly without data loss or corruption."""
    # Inserting multiple distinct positions that may or may not collide,
    # verifying all are retrievable with correct min/max values.
    positions = [
        (float(i), float(i)) for i in range(50)
    ]

    for i, pos in enumerate(positions):
        table.add_report(pos, float(i))
        table.add_report(pos, float(i - 10))

    assert len(table) == 50

    for i, pos in enumerate(positions):
        assert pos in table
        assert table[pos] == (float(i - 10), float(i))


def test_automatic_resizing_and_rehash(table):
    """Test that capacity increases automatically when load factor exceeds 0.7,
    preserving all unique records and their temperature bounds."""
    # Insert enough items to trigger load factor threshold (> 0.7)
    # Assuming initial capacity is small (e.g., 10 or 16)
    num_items = 30
    for i in range(num_items):
        pos = (float(i), float(i))
        table.add_report(pos, 50.0)
        table.add_report(pos, float(i))

    assert len(table) == num_items

    # Verify all records are intact and preserved after resizing
    for i in range(num_items):
        pos = (float(i), float(i))
        assert pos in table
        assert table[pos] == (float(i), 50.0)