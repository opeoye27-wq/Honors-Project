import pytest

# Assumption: The implementation is located in records.py and defines
# LocalRecord and RecordsMap with the public interfaces described.
from RecordsMap import LocalRecord, RecordsMap


# --------------------------------------------------
# RecordsMap: Initialization and Empty Table
# --------------------------------------------------

def test_empty_table_initialization():
    records = RecordsMap()

    assert len(records) == 0
    assert records.size == 0
    assert records.capacity == 8


def test_empty_table_contains_no_positions():
    records = RecordsMap()

    assert (0, 0) not in records
    assert (10, 20) not in records


def test_empty_table_lookup_raises_key_error():
    records = RecordsMap()

    with pytest.raises(KeyError):
        records[(0, 0)]


def test_custom_initial_capacity():
    records = RecordsMap(capacity=16)

    assert records.capacity == 16
    assert len(records) == 0


# --------------------------------------------------
# RecordsMap: Basic Insertion and Lookup
# --------------------------------------------------

def test_insert_single_record():
    records = RecordsMap()

    records.add_report((10, 20), 75)

    assert len(records) == 1
    assert records.size == 1
    assert (10, 20) in records
    assert records[(10, 20)] == (75, 75)


def test_insert_multiple_distinct_positions():
    records = RecordsMap()

    records.add_report((1, 2), 50)
    records.add_report((3, 4), 60)
    records.add_report((5, 6), 70)

    assert len(records) == 3
    assert records[(1, 2)] == (50, 50)
    assert records[(3, 4)] == (60, 60)
    assert records[(5, 6)] == (70, 70)


def test_insert_zero_temperature():
    records = RecordsMap()

    records.add_report((1, 1), 0)

    assert records[(1, 1)] == (0, 0)


def test_insert_negative_temperature():
    records = RecordsMap()

    records.add_report((1, 1), -15)

    assert records[(1, 1)] == (-15, -15)


def test_insert_negative_and_positive_temperatures():
    records = RecordsMap()

    records.add_report((1, 1), -20)
    records.add_report((2, 2), 30)

    assert records[(1, 1)] == (-20, -20)
    assert records[(2, 2)] == (30, 30)
    assert len(records) == 2


def test_insert_float_temperature():
    records = RecordsMap()

    records.add_report((1, 2), 23.5)

    assert records[(1, 2)] == (23.5, 23.5)


# --------------------------------------------------
# RecordsMap: Temperature Updates
# --------------------------------------------------

def test_repeated_report_at_same_position():
    records = RecordsMap()

    records.add_report((1, 2), 50)
    records.add_report((1, 2), 50)
    records.add_report((1, 2), 50)

    assert len(records) == 1
    assert records[(1, 2)] == (50, 50)


def test_update_minimum_temperature():
    records = RecordsMap()

    records.add_report((1, 2), 50)
    records.add_report((1, 2), 30)

    assert records[(1, 2)] == (30, 50)
    assert len(records) == 1


def test_update_maximum_temperature():
    records = RecordsMap()

    records.add_report((1, 2), 30)
    records.add_report((1, 2), 50)

    assert records[(1, 2)] == (30, 50)
    assert len(records) == 1


def test_update_both_minimum_and_maximum():
    records = RecordsMap()

    records.add_report((1, 2), 40)
    records.add_report((1, 2), 10)
    records.add_report((1, 2), 60)

    assert records[(1, 2)] == (10, 60)
    assert len(records) == 1


def test_temperature_updates_in_random_order():
    records = RecordsMap()

    temperatures = [25, -10, 40, 5, 100, -30, 15]

    for temperature in temperatures:
        records.add_report((1, 2), temperature)

    assert records[(1, 2)] == (-30, 100)
    assert len(records) == 1


def test_repeated_negative_temperature_updates():
    records = RecordsMap()

    records.add_report((1, 2), -5)
    records.add_report((1, 2), -20)
    records.add_report((1, 2), -10)

    assert records[(1, 2)] == (-20, -5)


def test_repeated_zero_temperature_updates():
    records = RecordsMap()

    records.add_report((1, 2), 0)
    records.add_report((1, 2), -10)
    records.add_report((1, 2), 0)
    records.add_report((1, 2), 10)

    assert records[(1, 2)] == (-10, 10)
    assert len(records) == 1


def test_updates_do_not_change_unique_position_count():
    records = RecordsMap()

    records.add_report((1, 2), 10)
    records.add_report((1, 2), 20)
    records.add_report((1, 2), 30)

    assert len(records) == 1
    assert records.size == 1


# --------------------------------------------------
# RecordsMap: Coordinate Rounding
# --------------------------------------------------

def test_coordinates_round_to_same_position():
    records = RecordsMap()

    records.add_report((1.2, 2.3), 10)
    records.add_report((1.4, 2.4), 20)

    assert len(records) == 1
    assert records[(1, 2)] == (10, 20)


def test_rounded_coordinates_can_be_used_for_lookup():
    records = RecordsMap()

    records.add_report((5.2, 8.3), 25)

    assert records[(5, 8)] == (25, 25)


def test_unrounded_coordinates_can_be_used_for_lookup():
    records = RecordsMap()

    records.add_report((5, 8), 25)

    assert records[(5.2, 8.3)] == (25, 25)


def test_negative_coordinates_round_consistently():
    records = RecordsMap()

    records.add_report((-1.2, -2.3), 10)

    assert (-1, -2) in records
    assert records[(-1, -2)] == (10, 10)


def test_negative_coordinates_round_to_same_position():
    records = RecordsMap()

    records.add_report((-1.2, -2.2), 10)
    records.add_report((-1.4, -2.4), 20)

    assert len(records) == 1
    assert records[(-1, -2)] == (10, 20)


def test_mixed_positive_and_negative_coordinates():
    records = RecordsMap()

    records.add_report((-1.2, 2.3), 15)
    records.add_report((-1.4, 2.4), 25)

    assert len(records) == 1
    assert records[(-1, 2)] == (15, 25)


def test_coordinates_round_independently():
    records = RecordsMap()

    records.add_report((1.2, 2.8), 10)

    assert records[(1, 3)] == (10, 10)


def test_different_rounded_coordinates_remain_distinct():
    records = RecordsMap()

    records.add_report((1.2, 2.2), 10)
    records.add_report((1.6, 2.6), 20)

    assert len(records) == 2
    assert records[(1, 2)] == (10, 10)
    assert records[(2, 3)] == (20, 20)


def test_coordinate_updates_preserve_temperature_extremes():
    records = RecordsMap()

    records.add_report((3.1, 4.1), 50)
    records.add_report((3.4, 4.4), -10)
    records.add_report((3.2, 4.2), 100)

    assert len(records) == 1
    assert records[(3, 4)] == (-10, 100)


# --------------------------------------------------
# RecordsMap: Membership and Missing Positions
# --------------------------------------------------

def test_membership_after_insertion():
    records = RecordsMap()

    records.add_report((1, 2), 30)

    assert (1, 2) in records
    assert (3, 4) not in records


def test_membership_after_multiple_insertions():
    records = RecordsMap()

    positions = [(1, 2), (3, 4), (5, 6), (7, 8)]

    for position in positions:
        records.add_report(position, 20)

    for position in positions:
        assert position in records

    assert (9, 10) not in records


def test_lookup_missing_position_raises_key_error():
    records = RecordsMap()

    records.add_report((1, 2), 30)

    with pytest.raises(KeyError):
        records[(3, 4)]


def test_missing_lookup_does_not_change_size():
    records = RecordsMap()

    records.add_report((1, 2), 30)

    with pytest.raises(KeyError):
        records[(3, 4)]

    assert len(records) == 1


def test_missing_lookup_does_not_modify_existing_records():
    records = RecordsMap()

    records.add_report((1, 2), 30)

    with pytest.raises(KeyError):
        records[(3, 4)]

    assert records[(1, 2)] == (30, 30)


# --------------------------------------------------
# RecordsMap: Hash Collisions
# --------------------------------------------------

def test_hash_collisions_preserve_distinct_records():
    records = RecordsMap(capacity=8)

    positions = []
    buckets = {}

    # Find two distinct positions assigned to the same bucket.
    for i in range(1000):
        position = (i, i + 1)
        bucket = records._hash(position)

        if bucket in buckets:
            positions = [buckets[bucket], position]
            break

        buckets[bucket] = position

    assert len(positions) == 2

    first, second = positions

    records.add_report(first, 10)
    records.add_report(second, 20)

    assert len(records) == 2
    assert records[first] == (10, 10)
    assert records[second] == (20, 20)


def test_hash_collisions_do_not_cause_incorrect_updates():
    records = RecordsMap(capacity=8)

    buckets = {}
    collision = None

    for i in range(1000):
        position = (i, i + 1)
        bucket = records._hash(position)

        if bucket in buckets:
            collision = (buckets[bucket], position)
            break

        buckets[bucket] = position

    assert collision is not None

    first, second = collision

    records.add_report(first, 10)
    records.add_report(second, 20)
    records.add_report(first, -5)

    assert len(records) == 2
    assert records[first] == (-5, 10)
    assert records[second] == (20, 20)


def test_multiple_collisions_preserve_all_records():
    records = RecordsMap(capacity=4)

    positions = [(i, i * 2) for i in range(20)]

    for i, position in enumerate(positions):
        records.add_report(position, i)

    assert len(records) == 20

    for i, position in enumerate(positions):
        assert records[position] == (i, i)


# --------------------------------------------------
# RecordsMap: Load Factor and Resizing
# --------------------------------------------------

def test_no_resize_below_load_factor_threshold():
    records = RecordsMap(capacity=10)

    for i in range(7):
        records.add_report((i, i + 1), i)

    assert records.capacity == 10
    assert len(records) == 7


def test_resize_when_load_factor_exceeds_threshold():
    records = RecordsMap(capacity=10)

    for i in range(8):
        records.add_report((i, i + 1), i)

    assert records.capacity > 10
    assert len(records) == 8


def test_resize_doubles_capacity():
    records = RecordsMap(capacity=10)

    for i in range(8):
        records.add_report((i, i + 1), i)

    assert records.capacity == 20


def test_resize_preserves_all_existing_records():
    records = RecordsMap(capacity=4)

    expected = {}

    for i in range(20):
        position = (i, i + 1)
        temperature = i * 5

        records.add_report(position, temperature)
        expected[position] = (temperature, temperature)

    for position, temperatures in expected.items():
        assert records[position] == temperatures

    assert len(records) == 20


def test_resize_preserves_minimum_and_maximum_temperatures():
    records = RecordsMap(capacity=4)

    expected = {}

    for i in range(15):
        position = (i, i + 1)

        records.add_report(position, 50)
        records.add_report(position, -20)
        records.add_report(position, 100)

        expected[position] = (-20, 100)

    for position, temperatures in expected.items():
        assert records[position] == temperatures

    assert len(records) == 15


def test_resize_does_not_increase_unique_count():
    records = RecordsMap(capacity=4)

    for i in range(3):
        records.add_report((i, i + 1), 10)

    assert len(records) == 3

    # Updating existing records should not increase size.
    records.add_report((0, 1), -10)
    records.add_report((1, 2), 20)

    assert len(records) == 3


def test_multiple_resizes_preserve_all_records():
    records = RecordsMap(capacity=2)

    expected = {}

    for i in range(100):
        position = (i, -i)
        records.add_report(position, i)
        expected[position] = (i, i)

    assert len(records) == 100

    for position, temperatures in expected.items():
        assert records[position] == temperatures


def test_updates_after_resizing():
    records = RecordsMap(capacity=4)

    for i in range(20):
        records.add_report((i, i + 1), 50)

    records.add_report((0, 1), -100)
    records.add_report((0, 1), 200)

    assert records[(0, 1)] == (-100, 200)
    assert len(records) == 20


def test_new_records_can_be_inserted_after_resizing():
    records = RecordsMap(capacity=4)

    for i in range(20):
        records.add_report((i, i + 1), i)

    records.add_report((100, 200), 500)

    assert len(records) == 21
    assert records[(100, 200)] == (500, 500)


def test_resizing_preserves_negative_coordinates():
    records = RecordsMap(capacity=4)

    for i in range(20):
        records.add_report((-i, -i - 1), i)

    assert len(records) == 20

    for i in range(20):
        assert records[(-i, -i - 1)] == (i, i)


def test_resizing_preserves_rounded_coordinates():
    records = RecordsMap(capacity=4)

    records.add_report((1.2, 2.2), 10)

    for i in range(20):
        records.add_report((i + 10, i + 20), i)

    records.add_report((1.4, 2.4), -10)

    assert records[(1, 2)] == (-10, 10)
    assert len(records) == 21


# --------------------------------------------------
# LocalRecord: Individual Record Behavior
# --------------------------------------------------

def test_local_record_initialization():
    record = LocalRecord((1, 2), max=50, min=10)

    assert record.pos == (1, 2)
    assert record.max == 50
    assert record.min == 10


def test_local_record_rounds_coordinates():
    record = LocalRecord((1.4, 2.6))

    assert record.pos == (1, 3)


def test_local_record_updates_maximum():
    record = LocalRecord((1, 2), max=50, min=50)

    record.add_report(100)

    assert record.max == 100
    assert record.min == 50


def test_local_record_updates_minimum():
    record = LocalRecord((1, 2), max=50, min=50)

    record.add_report(10)

    assert record.min == 10
    assert record.max == 50


def test_local_record_updates_both_extremes():
    record = LocalRecord((1, 2), max=50, min=50)

    record.add_report(-10)
    record.add_report(100)

    assert record.min == -10
    assert record.max == 100


def test_local_record_accepts_zero_temperature():
    record = LocalRecord((1, 2), max=0, min=0)

    record.add_report(0)

    assert record.min == 0
    assert record.max == 0


def test_local_record_accepts_negative_temperature():
    record = LocalRecord((1, 2), max=-5, min=-5)

    record.add_report(-20)

    assert record.min == -20
    assert record.max == -5


def test_local_record_equality_for_same_position():
    first = LocalRecord((1, 2))
    second = LocalRecord((1, 2))

    assert first == second


def test_local_record_equality_for_rounded_positions():
    first = LocalRecord((1.2, 2.2))
    second = LocalRecord((1.4, 2.4))

    assert first == second


def test_local_record_inequality_for_different_positions():
    first = LocalRecord((1, 2))
    second = LocalRecord((3, 4))

    assert first != second


def test_local_record_hash_consistency():
    first = LocalRecord((1.2, 2.2))
    second = LocalRecord((1.4, 2.4))

    assert first == second
    assert hash(first) == hash(second)


def test_local_record_hash_deterministic():
    first = LocalRecord((1, 2))
    second = LocalRecord((1, 2))

    assert hash(first) == hash(second)


# --------------------------------------------------
# RecordsMap: Combined Stress Tests
# --------------------------------------------------

def test_large_number_of_insertions_and_updates():
    records = RecordsMap(capacity=4)

    for i in range(200):
        records.add_report((i, i * 2), i)

    for i in range(200):
        records.add_report((i, i * 2), -i)

    assert len(records) == 200

    for i in range(200):
        assert records[(i, i * 2)] == (-i, i)


def test_interleaved_insertions_and_updates():
    records = RecordsMap(capacity=4)

    records.add_report((1, 1), 10)
    records.add_report((2, 2), 20)
    records.add_report((1, 1), -10)
    records.add_report((3, 3), 30)
    records.add_report((2, 2), 40)
    records.add_report((1, 1), 50)

    assert len(records) == 3
    assert records[(1, 1)] == (-10, 50)
    assert records[(2, 2)] == (20, 40)
    assert records[(3, 3)] == (30, 30)


def test_all_records_remain_accessible_after_many_resizes():
    records = RecordsMap(capacity=2)

    expected = {}

    for i in range(150):
        position = (i - 75, i + 25)
        records.add_report(position, i - 50)
        expected[position] = (i - 50, i - 50)

    for position, temperatures in expected.items():
        assert position in records
        assert records[position] == temperatures

    assert len(records) == 150
    assert records.size == 150


def test_rounded_duplicate_positions_do_not_increase_size_after_resizing():
    records = RecordsMap(capacity=4)

    for i in range(20):
        records.add_report((i + 10, i + 20), i)

    original_size = len(records)

    records.add_report((10.1, 20.1), -100)
    records.add_report((10.4, 20.4), 100)

    assert len(records) == original_size
    assert records[(10, 20)] == (-100, 100)


def test_temperature_extremes_remain_correct_after_many_updates_and_resizes():
    records = RecordsMap(capacity=4)

    records.add_report((0, 0), 25)

    for i in range(1, 100):
        records.add_report((i, i), i)

    records.add_report((0, 0), -100)
    records.add_report((0, 0), 500)
    records.add_report((0, 0), 0)

    assert records[(0, 0)] == (-100, 500)
    assert len(records) == 100


def test_size_attribute_matches_len_after_all_operations():
    records = RecordsMap(capacity=4)

    for i in range(50):
        records.add_report((i, i + 1), i)

        assert records.size == len(records)

    for i in range(50):
        records.add_report((i, i + 1), -i)

        assert records.size == len(records)

    assert len(records) == 50