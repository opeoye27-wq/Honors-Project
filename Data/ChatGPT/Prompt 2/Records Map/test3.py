import pytest
from RecordsMap import LocalRecord, RecordsMap
# Assumed public interface (adapt names if the implementation differs):
#   TemperatureHashTable(initial_capacity=...)
#   table.add_record(position, temperature)
#   table.get_record(position) -> (minimum_temperature, maximum_temperature)
#   table.contains(position) -> bool
#   len(table) -> number of unique positions
#
# Assumptions:
# 1. Positions are supplied as (latitude, longitude) tuples.
# 2. Coordinates use Python's standard round() behavior, including
#    round-to-even for exact halfway values.
# 3. Temperatures are numeric values.
# 4. The table automatically resizes when load_factor > 0.7.
# 5. A record is returned as a (minimum, maximum) tuple.
# 6. Invalid input behavior is not specified, so tests for invalid
#    coordinate and temperature types are intentionally omitted.


@pytest.fixture
def table():
    return RecordsMap(capacity=10)


# --------------------------------------------------
# Basic functionality
# --------------------------------------------------

def test_empty_table_has_zero_records(table):
    assert len(table) == 0


def test_empty_table_does_not_contain_position(table):
    assert (10, 20) not in table


def test_insert_single_record(table):
    table.add_report((10, 20), 25)

    assert len(table) == 1
    assert (10, 20) in table
    assert table[(10, 20)] == (25, 25)


def test_insert_multiple_unique_positions(table):
    table.add_report((10, 20), 25)
    table.add_report((30, 40), 15)
    table.add_report((50, 60), 35)

    assert len(table) == 3
    assert table[(10, 20)] == (25, 25)
    assert table[(30, 40)] == (15, 15)
    assert table[(50, 60)] == (35, 35)


def test_record_count_does_not_increase_for_existing_position(table):
    table.add_report((10, 20), 25)
    table.add_report((10, 20), 30)
    table.add_report((10, 20), 15)

    assert len(table) == 1


# --------------------------------------------------
# Minimum and maximum temperature updates
# --------------------------------------------------

def test_update_maximum_temperature(table):
    table.add_report((10, 20), 20)
    table.add_report((10, 20), 35)

    assert table[(10, 20)] == (20, 35)


def test_update_minimum_temperature(table):
    table.add_report((10, 20), 20)
    table.add_report((10, 20), 5)

    assert table[(10, 20)] == (5, 20)


def test_update_both_minimum_and_maximum(table):
    table.add_report((10, 20), 20)
    table.add_report((10, 20), 35)
    table.add_report((10, 20), 5)

    assert table[(10, 20)] == (5, 35)


def test_repeated_identical_temperature(table):
    table.add_report((10, 20), 25)
    table.add_report((10, 20), 25)
    table.add_report((10, 20), 25)

    assert table[(10, 20)] == (25, 25)
    assert len(table) == 1


def test_temperature_between_existing_minimum_and_maximum(table):
    table.add_report((10, 20), 10)
    table.add_report((10, 20), 40)
    table.add_report((10, 20), 25)

    assert table[(10, 20)] == (10, 40)


def test_many_temperature_updates(table):
    temperatures = [30, 10, 50, 20, 5, 60, 15, 40]

    for temperature in temperatures:
        table.add_report((10, 20), temperature)

    assert table[(10, 20)] == (5, 60)
    assert len(table) == 1


def test_temperature_updates_do_not_affect_other_positions(table):
    table.add_report((10, 20), 15)
    table.add_report((30, 40), 25)

    table.add_report((10, 20), 50)

    assert table[(10, 20)] == (15, 50)
    assert table[(30, 40)] == (25, 25)
    assert len(table) == 2


# --------------------------------------------------
# Zero and negative temperatures
# --------------------------------------------------

def test_zero_temperature(table):
    table.add_report((0, 0), 0)

    assert table[(0, 0)] == (0, 0)


def test_negative_temperature(table):
    table.add_report((10, 20), -15)

    assert table[(10, 20)] == (-15, -15)


def test_multiple_negative_temperatures(table):
    table.add_report((10, 20), -5)
    table.add_report((10, 20), -20)
    table.add_report((10, 20), -10)

    assert table[(10, 20)] == (-20, -5)


def test_positive_and_negative_temperatures(table):
    table.add_report((10, 20), -15)
    table.add_report((10, 20), 25)
    table.add_report((10, 20), 0)

    assert table[(10, 20)] == (-15, 25)


def test_zero_between_negative_and_positive_temperatures(table):
    table.add_report((10, 20), -10)
    table.add_report((10, 20), 0)
    table.add_report((10, 20), 10)

    assert table[(10, 20)] == (-10, 10)


# --------------------------------------------------
# Coordinate rounding
# --------------------------------------------------

def test_coordinates_round_to_same_position(table):
    table.add_report((10.2, 20.3), 15)
    table.add_report((10.4, 20.4), 30)

    assert len(table) == 1
    assert table[(10, 20)] == (15, 30)


def test_coordinates_round_to_same_position_with_different_precision(table):
    table.add_report((10.1, 20.1), 10)
    table.add_report((10.49, 20.49), 20)
    table.add_report((10.01, 20.01), 30)

    assert len(table) == 1
    assert table[(10, 20)] == (10, 30)


def test_coordinates_round_to_different_positions(table):
    table.add_report((10.1, 20.1), 10)
    table.add_report((10.6, 20.6), 20)

    assert len(table) == 2
    assert table[(10, 20)] == (10, 10)
    assert table[(11, 21)] == (20, 20)


def test_rounding_negative_coordinates(table):
    table.add_report((-10.2, -20.3), 15)

    assert (-10, -20) in table
    assert table[(-10, -20)] == (15, 15)


def test_negative_coordinates_round_to_same_position(table):
    table.add_report((-10.1, -20.1), 10)
    table.add_report((-10.4, -20.4), 30)

    assert len(table) == 1
    assert table[(-10, -20)] == (10, 30)


def test_mixed_positive_and_negative_coordinates(table):
    table.add_report((-10.2, 20.3), 10)
    table.add_report((-10.4, 20.4), 20)

    assert len(table) == 1
    assert table[(-10, 20)] == (10, 20)


def test_coordinates_at_zero(table):
    table.add_report((0.1, -0.1), 10)

    assert (0, 0) in table
    assert table[(0, 0)] == (10, 10)


def test_exact_halfway_coordinate_rounding(table):
    # Assumption: Python's built-in round() uses ties-to-even.
    table.add_report((10.5, 20.5), 10)

    assert (10, 20) in table
    assert table[(10, 20)] == (10, 10)


def test_negative_halfway_coordinate_rounding(table):
    # Assumption: Python's built-in round() uses ties-to-even.
    table.add_report((-10.5, -20.5), 10)

    assert (-10, -20) in table
    assert table[(-10, -20)] == (10, 10)


def test_lookup_uses_coordinate_rounding(table):
    table.add_report((10.2, 20.3), 15)

    assert table[(10.4, 20.4)] == (15, 15)


def test_contains_uses_coordinate_rounding(table):
    table.add_report((10.2, 20.3), 15)

    assert (10.4, 20.4) in table


def test_rounded_coordinates_do_not_create_duplicate_records(table):
    positions = [
        (10.1, 20.1),
        (10.2, 20.2),
        (10.3, 20.3),
        (10.4, 20.4),
        (10.49, 20.49),
    ]

    for i, position in enumerate(positions):
        table.add_report(position, i)

    assert len(table) == 1
    assert table[(10, 20)] == (0, 4)


# --------------------------------------------------
# Missing positions
# --------------------------------------------------

def test_lookup_missing_position_raises_key_error(table):
    with pytest.raises(KeyError):
        table[(100, 200)]


def test_lookup_missing_position_does_not_change_count(table):
    table.add_report((10, 20), 15)

    with pytest.raises(KeyError):
        table[(100, 200)]

    assert len(table) == 1


def test_contains_missing_position_returns_false(table):
    assert (100, 200) not in table


def test_missing_position_after_other_insertions(table):
    table.add_report((10, 20), 15)
    table.add_report((30, 40), 25)

    with pytest.raises(KeyError):
        table[(50, 60)]

    assert len(table) == 2


# --------------------------------------------------
# Hash collisions
# --------------------------------------------------

def test_collision_handling_with_minimum_capacity():
    # Assumption: the constructor accepts an initial capacity of 1.
    # All positions necessarily map to the same bucket initially.
    collision_table = RecordsMap(capacity=1)

    collision_table.add_report((10, 20), 15)
    collision_table.add_report((30, 40), 25)

    assert (10, 20) in collision_table
    assert (30, 40) in collision_table

    assert collision_table[(10, 20)] == (15, 15)
    assert collision_table[(30, 40)] == (25, 25)

    assert len(collision_table) == 2


def test_collisions_do_not_overwrite_existing_records():
    collision_table = RecordsMap(capacity=1)

    collision_table.add_report((10, 20), 10)
    collision_table.add_report((30, 40), 30)
    collision_table.add_report((50, 60), 50)

    assert collision_table[(10, 20)] == (10, 10)
    assert collision_table[(30, 40)] == (30, 30)
    assert collision_table[(50, 60)] == (50, 50)

    assert len(collision_table) == 3


def test_update_record_after_collision():
    collision_table = RecordsMap(capacity=1)

    collision_table.add_report((10, 20), 10)
    collision_table.add_report((30, 40), 30)

    collision_table.add_report((10, 20), 5)

    assert collision_table[(10, 20)] == (5, 10)
    assert collision_table[(30, 40)] == (30, 30)
    assert len(collision_table) == 2


def test_colliding_positions_remain_independent_after_updates():
    collision_table = RecordsMap(capacity=1)

    collision_table.add_report((10, 20), 10)
    collision_table.add_report((30, 40), 20)

    collision_table.add_report((10, 20), 50)
    collision_table.add_report((30, 40), -10)

    assert collision_table[(10, 20)] == (10, 50)
    assert collision_table[(30, 40)] == (-10, 20)

    assert len(collision_table) == 2


# --------------------------------------------------
# Load factor and resizing
# --------------------------------------------------

def test_table_resizes_when_load_factor_exceeds_threshold():
    # Assumption: initial capacity is 10 and resizing occurs
    # when the resulting load factor becomes greater than 0.7.
    resize_table = RecordsMap(capacity=10)

    for i in range(8):
        resize_table.add_report((i * 10, i * 20), i)

    # Eight unique positions should have triggered resizing.
    assert len(resize_table) == 8

    for i in range(8):
        assert resize_table[(i * 10, i * 20)] == (i, i)


def test_table_does_not_count_duplicate_positions_toward_resize(table):
    for _ in range(20):
        table.add_report((10, 20), 25)

    assert len(table) == 1
    assert table[(10, 20)] == (25, 25)


def test_resize_preserves_all_existing_records():
    resize_table = RecordsMap(capacity=4)

    records = {
        (10, 20): (5, 15),
        (30, 40): (-10, 10),
        (50, 60): (20, 30),
    }

    for position, (minimum, maximum) in records.items():
        resize_table.add_report(position, minimum)
        resize_table.add_report(position, maximum)

    # Insert enough additional unique positions to trigger resizing.
    for i in range(10):
        resize_table.add_report((100 + i, 200 + i), i)

    assert len(resize_table) == 13

    for position, expected in records.items():
        assert resize_table[position] == expected


def test_resize_preserves_negative_and_zero_temperatures():
    resize_table = RecordsMap(capacity=2)

    resize_table.add_report((10, 20), -20)
    resize_table.add_report((10, 20), 0)

    resize_table.add_report((30, 40), -5)
    resize_table.add_report((50, 60), 0)

    for i in range(10):
        resize_table.add_report((100 + i, 200 + i), i)

    assert resize_table[(10, 20)] == (-20, 0)
    assert resize_table[(30, 40)] == (-5, -5)
    assert resize_table[(50, 60)] == (0, 0)


def test_multiple_resizes_preserve_all_records():
    resize_table = RecordsMap(capacity=2)

    expected_records = {}

    for i in range(100):
        position = (i * 10, i * 20)
        temperature = i - 50

        resize_table.add_report(position, temperature)
        expected_records[position] = (temperature, temperature)

    assert len(resize_table) == 100

    for position, expected in expected_records.items():
        assert resize_table[position] == expected


def test_updates_after_resizing():
    resize_table = RecordsMap(capacity=2)

    for i in range(20):
        resize_table.add_report((i * 10, i * 20), i)

    resize_table.add_report((0, 0), -100)
    resize_table.add_report((0, 0), 100)

    assert resize_table[(0, 0)] == (-100, 100)
    assert len(resize_table) == 20


def test_duplicate_positions_after_resizing_do_not_increase_count():
    resize_table = RecordsMap(capacity=2)

    for i in range(20):
        resize_table.add_report((i * 10, i * 20), i)

    original_count = len(resize_table)

    for _ in range(10):
        resize_table.add_report((0, 0), 50)

    assert len(resize_table) == original_count
    assert resize_table[(0, 0)] == (0, 50)


def test_rounded_duplicate_positions_after_resizing():
    resize_table = RecordsMap(capacity=2)

    for i in range(20):
        resize_table.add_report((i * 10, i * 20), i)

    original_count = len(resize_table)

    resize_table.add_report((0.1, 0.1), -10)
    resize_table.add_report((0.4, 0.4), 50)

    assert len(resize_table) == original_count
    assert resize_table[(0, 0)] == (-10, 50)


# --------------------------------------------------
# Larger datasets and combined operations
# --------------------------------------------------

def test_many_unique_positions():
    for i in range(500):
        table.add_report((i, i * 2), i)

    assert len(table) == 500

    for i in range(500):
        assert table[(i, i * 2)] == (i, i)


def test_many_positions_with_multiple_temperature_reports():
    expected = {}

    for i in range(100):
        position = (i, i * 2)

        temperatures = [i, i - 10, i + 20]

        for temperature in temperatures:
            table.add_report(position, temperature)

        expected[position] = (i - 10, i + 20)

    assert len(table) == 100

    for position, expected_values in expected.items():
        assert table[position] == expected_values


def test_interleaved_updates_to_multiple_positions(table):
    table.add_report((10, 20), 10)
    table.add_report((30, 40), 30)
    table.add_report((10, 20), 5)
    table.add_report((50, 60), 50)
    table.add_report((30, 40), 40)
    table.add_report((10, 20), 20)
    table.add_report((50, 60), -10)

    assert table[(10, 20)] == (5, 20)
    assert table[(30, 40)] == (30, 40)
    assert table[(50, 60)] == (-10, 50)

    assert len(table) == 3


def test_all_records_remain_accessible_after_many_updates_and_resizes():
    resize_table = RecordsMap(capacity=2)

    expected = {}

    for i in range(50):
        position = (i * 5, i * 7)

        resize_table.add_report(position, 10)
        resize_table.add_report(position, -10)
        resize_table.add_report(position, 20)
        resize_table.add_report(position, 0)

        expected[position] = (-10, 20)

    assert len(resize_table) == 50

    for position, values in expected.items():
        assert position in resize_table
        assert resize_table[position] == values


def test_lookup_and_contains_after_multiple_resizes():
    resize_table = RecordsMap(capacity=2)

    for i in range(100):
        resize_table.add_report((i, i + 100), i)

    for i in range(100):
        assert (i, i + 100) in resize_table
        assert resize_table[(i, i + 100)] == (i, i)

    assert (1000, 2000) not in resize_table


def test_record_count_matches_unique_rounded_positions():
    positions = [
        (10.1, 20.1),
        (10.2, 20.2),
        (11.1, 21.1),
        (11.2, 21.2),
        (12.1, 22.1),
        (12.2, 22.2),
    ]

    for i, position in enumerate(positions):
        table.add_report(position, i)

    # Each pair of positions rounds to the same coordinates.
    assert len(table) == 3

    assert table[(10, 20)] == (0, 1)
    assert table[(11, 21)] == (2, 3)
    assert table[(12, 22)] == (4, 5)