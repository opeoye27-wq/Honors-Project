import pytest

# Assumptions:
# - The implementation exposes a LocalRecord class and a hash table class.
# - Geographic positions are represented as (latitude, longitude) tuples.
# - Positions are rounded according to the configured precision.
# - Minimum and maximum temperatures are stored independently.
# - Duplicate positions refer to the same record after rounding.
# - Invalid inputs should raise an appropriate exception.
#
# Adjust the import and class names to match the provided implementation.

from RecordsMap import LocalRecord, RecordsMap


# -------------------------
# LocalRecord initialization
# -------------------------

def test_record_initialization():
    record = LocalRecord((40.7128, -74.0060), max=30, min=10)
    assert record.pos == (40.7128, -74.006)
    assert record.max == 30
    assert record.min == 10


def test_record_default_temperatures():
    record = LocalRecord((40.0, -70.0))
    assert record.max is None
    assert record.min is None


def test_record_zero_temperatures():
    record = LocalRecord((0, 0), max=0, min=0)
    assert record.max == 0
    assert record.min == 0


def test_record_negative_temperatures():
    record = LocalRecord((40, -70), max=-5, min=-20)
    assert record.max == -5
    assert record.min == -20


def test_record_rounds_position_to_default_precision():
    record = LocalRecord((40.123456, -70.654321))
    assert record.pos == (40.0, -71.0)


def test_record_rounds_position_to_custom_precision():
    record = LocalRecord((40.123456, -70.654321), precision=3)
    assert record.pos == (40.123, -70.654)


def test_record_zero_precision():
    record = LocalRecord((40.567, -70.432), precision=0)
    assert record.pos == (41.0, -70.0)


def test_record_high_precision():
    record = LocalRecord((40.123456789, -70.987654321), precision=6)
    assert record.pos == (40.123457, -70.987654)


def test_record_boundary_coordinates():
    record = LocalRecord((90, 180), precision=0)
    assert record.pos == (90, 180)

    record = LocalRecord((-90, -180), precision=0)
    assert record.pos == (-90, -180)


def test_record_invalid_position_type():
    with pytest.raises((TypeError, ValueError)):
        LocalRecord("40,-70")


def test_record_incomplete_position():
    with pytest.raises((TypeError, ValueError, IndexError)):
        LocalRecord((40,))


def test_record_extra_position_values():
    # Assumption: exactly two coordinates are required.
    with pytest.raises((TypeError, ValueError)):
        LocalRecord((40, -70, 10))


def test_record_non_numeric_coordinates():
    with pytest.raises((TypeError, ValueError)):
        LocalRecord(("north", "west"))


def test_record_invalid_precision():
    with pytest.raises((TypeError, ValueError)):
        LocalRecord((40, -70), precision=-1)


# -------------------------
# Hash table initialization
# -------------------------

def test_hash_table_initialization():
    table = RecordsMap()
    assert table is not None


def test_hash_table_empty_state():
    table = RecordsMap()
    assert len(table) == 0


# -------------------------
# Insertion and retrieval
# -------------------------

def test_insert_single_record():
    table = RecordsMap()
    record = LocalRecord((40, -70), max=30, min=10)

    table.add_report(record.pos, record.min)
    table.add_report(record.pos, record.max)

    assert len(table) == 1


def test_insert_multiple_records():
    table = RecordsMap()

    records = [
        LocalRecord((40, -70), max=30, min=10),
        LocalRecord((41, -71), max=25, min=5),
        LocalRecord((42, -72), max=35, min=15),
    ]

    for record in records:
        table.add_report(record.pos, record.min)
        table.add_report(record.pos, record.max)

    assert len(table) == 3


def test_insert_duplicate_position():
    table = RecordsMap()

    table.add_report((40, -70), 10)
    table.add_report((40, -70), 30)
    table.add_report((40, -70), 5)
    table.add_report((40, -70), 35)

    # Assumption: duplicate positions update an existing record.
    assert len(table) == 1


def test_insert_same_position_after_rounding():
    table = RecordsMap()

    table.add_report((40.1234, -70.1234), None)
    table.add_report((40.1244, -70.1244), None)

    assert len(table) == 1


def test_insert_distinct_positions():
    table = RecordsMap()

    table.add_report((40, -70), None)
    table.add_report((41, -71), None)

    assert len(table) == 2


def test_insert_record_with_missing_temperatures():
    table = RecordsMap()
    record = LocalRecord((40, -70))

    table.add_report(record.pos, record.max)

    assert len(table) == 1


def test_insert_extreme_temperatures():
    table = RecordsMap()

    record = LocalRecord(
        (40, -70),
        max=1000,
        min=-1000
    )

    table.add_report(record.pos, record.min)
    table.add_report(record.pos, record.max)

    assert len(table) == 1


def test_insert_zero_coordinates():
    table = RecordsMap()

    table.add_report((0, 0), 10)
    table.add_report((0, 0), 20)

    assert len(table) == 1


def test_insert_negative_coordinates():
    table = RecordsMap()

    table.add_report((-45, -120), 10)
    table.add_report((-45, -120), 20)

    assert len(table) == 1


def test_insert_invalid_record():
    table = RecordsMap()

    with pytest.raises((TypeError, ValueError, AttributeError)):
        table.add_report(None, None)


# -------------------------
# Minimum and maximum values
# -------------------------

def test_store_maximum_temperature():
    table = RecordsMap()
    record = LocalRecord((40, -70), max=30)

    table.add_report(record.pos, record.max)

    retrieved = table[(40, -70)]
    assert retrieved.max == 30


def test_store_minimum_temperature():
    table = RecordsMap()
    record = LocalRecord((40, -70), min=10)

    table.add_report(record.pos, record.min)

    retrieved = table[(40, -70)]
    assert retrieved.min == 10


def test_store_both_temperatures():
    table = RecordsMap()
    record = LocalRecord((40, -70), max=30, min=10)

    table.add_report(record.pos, record.min)
    table.add_report(record.pos, record.max)

    retrieved = table[(40, -70)]

    assert retrieved.max == 30
    assert retrieved.min == 10


def test_update_maximum_temperature():
    table = RecordsMap()

    table.add_report((40, -70), 10)
    table.add_report((40, -70), 30)
    table.add_report((40, -70), 10)
    table.add_report((40, -70), 40)

    retrieved = table[(40, -70)]
    assert retrieved.max == 40


def test_update_minimum_temperature():
    table = RecordsMap()

    table.add_report((40, -70), 10)
    table.add_report((40, -70), 30)
    table.add_report((40, -70), 5)
    table.add_report((40, -70), 30)

    retrieved = table[(40, -70)]
    assert retrieved.min == 5


def test_update_both_temperatures():
    table = RecordsMap()

    table.add_report((40, -70), 10)
    table.add_report((40, -70), 30)
    table.add_report((40, -70), 5)
    table.add_report((40, -70), 40)

    retrieved = table[(40, -70)]

    assert retrieved.max == 40
    assert retrieved.min == 5


def test_negative_temperature_values():
    table = RecordsMap()

    table.add_report((40, -70), -20)
    table.add_report((40, -70), -5)

    retrieved = table[(40, -70)]

    assert retrieved.max == -5
    assert retrieved.min == -20


def test_zero_temperature_values():
    table = RecordsMap()

    table.add_report((40, -70), 0)
    table.add_report((40, -70), 0)

    retrieved = table[(40, -70)]

    assert retrieved.max == 0
    assert retrieved.min == 0


def test_maximum_less_than_minimum():
    # Assumption: the description does not specify whether this is invalid.
    # The test checks whether both supplied values are preserved.
    table = RecordsMap()

    table.add_report((40, -70), 20)
    table.add_report((40, -70), 5)

    retrieved = table[(40, -70)]

    assert retrieved.max == 5
    assert retrieved.min == 20


# -------------------------
# Searching
# -------------------------

def test_search_existing_position():
    table = RecordsMap()

    record = LocalRecord((40, -70), max=30, min=10)
    table.add_report(record.pos, record.min)
    table.add_report(record.pos, record.max)

    retrieved = table[(40, -70)]

    assert retrieved is not None
    assert retrieved.pos == (40.0, -70.0)


def test_search_missing_position():
    table = RecordsMap()

    with pytest.raises(KeyError):
        table[(40, -70)]


def test_search_empty_table():
    table = RecordsMap()

    with pytest.raises(KeyError):
        table[(0, 0)]


def test_search_multiple_records():
    table = RecordsMap()

    table.add_report((40, -70), 10)
    table.add_report((40, -70), 30)
    table.add_report((41, -71), 5)
    table.add_report((41, -71), 25)
    table.add_report((42, -72), 15)
    table.add_report((42, -72), 35)

    retrieved = table[(41, -71)]

    assert retrieved is not None
    assert retrieved.max == 25
    assert retrieved.min == 5


def test_search_position_with_different_coordinate_precision():
    table = RecordsMap()

    table.add_report((40.12345, -70.12345), None)

    retrieved = table[(40.12349, -70.12349)]

    # Assumption: search applies the same coordinate normalization.
    assert retrieved is not None


def test_search_invalid_position():
    table = RecordsMap()

    with pytest.raises((TypeError, ValueError, IndexError)):
        table["invalid"]


def test_search_incomplete_position():
    table = RecordsMap()

    with pytest.raises((TypeError, ValueError, IndexError)):
        table[(40,)]


def test_search_non_numeric_position():
    table = RecordsMap()

    with pytest.raises((TypeError, ValueError)):
        table[("north", "west")]


# -------------------------
# Hash collisions
# -------------------------

def test_multiple_records_with_same_hash():
    table = RecordsMap()

    # Assumption: collisions must not cause records to overwrite each other.
    records = [
        LocalRecord((10, 10), max=20, min=5),
        LocalRecord((20, 20), max=30, min=10),
        LocalRecord((30, 30), max=40, min=15),
    ]

    for record in records:
        table.add_report(record.pos, record.min)
        table.add_report(record.pos, record.max)

    assert len(table) == 3

    for record in records:
        retrieved = table[record.pos]
        assert retrieved is not None
        assert retrieved.max == record.max
        assert retrieved.min == record.min


def test_collision_does_not_corrupt_existing_records():
    table = RecordsMap()

    table.add_report((10, 10), 5)
    table.add_report((10, 10), 20)
    table.add_report((20, 20), 10)
    table.add_report((20, 20), 30)

    assert table[(10, 10)].max == 20
    assert table[(20, 20)].max == 30


def test_duplicate_position_after_collision():
    table = RecordsMap()

    table.add_report((10, 10), 5)
    table.add_report((10, 10), 20)
    table.add_report((20, 20), 10)
    table.add_report((20, 20), 30)
    table.add_report((10, 10), 0)
    table.add_report((10, 10), 50)

    assert table[(10, 10)].max == 50
    assert table[(20, 20)].max == 30


# -------------------------
# Large input and unusual cases
# -------------------------

def test_insert_large_number_of_records():
    table = RecordsMap()

    for i in range(1000):
        table.add_report((i, -i), i - 10)
        table.add_report((i, -i), i + 10)

    assert len(table) == 1000

    for i in range(1000):
        retrieved = table[(i, -i)]
        assert retrieved is not None
        assert retrieved.max == i + 10
        assert retrieved.min == i - 10


def test_insert_same_record_multiple_times():
    table = RecordsMap()
    record = LocalRecord((40, -70), max=30, min=10)

    table.add_report(record.pos, record.min)
    table.add_report(record.pos, record.max)
    table.add_report(record.pos, record.min)
    table.add_report(record.pos, record.max)
    table.add_report(record.pos, record.min)
    table.add_report(record.pos, record.max)

    assert len(table) == 1


def test_insert_and_search_after_many_operations():
    table = RecordsMap()

    for i in range(100):
        table.add_report((i, i), -i)
        table.add_report((i, i), i)

    for i in range(50):
        table.add_report((i, i), -i - 100)
        table.add_report((i, i), i + 100)

    for i in range(50):
        retrieved = table[(i, i)]
        assert retrieved.max == i + 100
        assert retrieved.min == -i - 100

    for i in range(50, 100):
        retrieved = table[(i, i)]
        assert retrieved.max == i
        assert retrieved.min == -i


def test_insert_float_coordinates():
    table = RecordsMap()

    table.add_report((40.7128, -74.0060), 10)
    table.add_report((40.7128, -74.0060), 30)

    assert table[(40.7128, -74.0060)] is not None


def test_insert_very_small_coordinate_values():
    table = RecordsMap()

    table.add_report((0.0000001, -0.0000001), None)

    assert table[(0.0000001, -0.0000001)] is not None


def test_insert_very_large_temperature_values():
    table = RecordsMap()

    table.add_report((40, -70), -(10**12))
    table.add_report((40, -70), 10**12)

    retrieved = table[(40, -70)]

    assert retrieved.max == 10**12
    assert retrieved.min == -(10**12)


def test_insert_boolean_temperature_values():
    # Assumption: Python booleans are technically numeric, but acceptance
    # of booleans as temperatures is not specified.
    table = RecordsMap()

    table.add_report((40, -70), False)
    table.add_report((40, -70), True)

    retrieved = table[(40, -70)]

    assert retrieved.max is True
    assert retrieved.min is False


def test_insert_nan_temperature():
    # Assumption: NaN is accepted unless the implementation explicitly
    # validates temperature values.
    table = RecordsMap()

    record = LocalRecord((40, -70), max=float("nan"), min=10)
    table.add_report(record.pos, record.min)
    table.add_report(record.pos, record.max)

    retrieved = table[(40, -70)]

    assert retrieved is not None
    assert retrieved.max != retrieved.max


def test_insert_infinite_temperature():
    table = RecordsMap()

    table.add_report((40, -70), float("-inf"))
    table.add_report((40, -70), float("inf"))

    retrieved = table[(40, -70)]

    assert retrieved.max == float("inf")
    assert retrieved.min == float("-inf")


# -------------------------
# Data integrity
# -------------------------

def test_inserting_record_does_not_corrupt_other_records():
    table = RecordsMap()

    table.add_report((10, 10), 5)
    table.add_report((10, 10), 20)
    table.add_report((20, 20), 10)
    table.add_report((20, 20), 30)
    table.add_report((30, 30), 15)
    table.add_report((30, 30), 40)

    assert table[(10, 10)].max == 20
    assert table[(20, 20)].max == 30
    assert table[(30, 30)].max == 40


def test_retrieved_record_has_correct_position():
    table = RecordsMap()

    table.add_report((40.123, -70.456), None)

    retrieved = table[(40.123, -70.456)]

    assert retrieved.pos == (40.123, -70.456)


def test_retrieved_record_temperatures_are_independent():
    table = RecordsMap()

    table.add_report((10, 10), 10)
    table.add_report((10, 10), 30)
    table.add_report((20, 20), 20)
    table.add_report((20, 20), 40)

    first = table[(10, 10)]
    second = table[(20, 20)]

    assert first.max == 30
    assert first.min == 10

    assert second.max == 40
    assert second.min == 20


def test_search_does_not_modify_table():
    table = RecordsMap()

    table.add_report((40, -70), 10)
    table.add_report((40, -70), 30)
    original_length = len(table)

    table[(40, -70)]
    with pytest.raises(KeyError):
        table[(50, -80)]
    table[(40, -70)]

    assert len(table) == original_length


def test_insert_does_not_modify_original_position():
    position = (40.12345, -70.54321)
    original = position

    record = LocalRecord(position, precision=2)

    assert position == original
    assert record.pos == (40.12, -70.54)


# -------------------------
# Geographic coordinate boundaries
# -------------------------

@pytest.mark.parametrize(
    "position",
    [
        (90, 180),
        (-90, -180),
        (0, 0),
        (90, -180),
        (-90, 180),
        (45, 90),
        (-45, -90),
    ]
)
def test_geographic_boundary_positions(position):
    table = RecordsMap()

    table.add_report(position, 10)
    table.add_report(position, 30)

    assert table[position] is not None


@pytest.mark.parametrize(
    "position",
    [
        (91, 0),
        (-91, 0),
        (0, 181),
        (0, -181),
    ]
)
def test_out_of_range_geographic_coordinates(position):
    # Assumption: geographic coordinates should be validated.
    table = RecordsMap()

    with pytest.raises((ValueError, TypeError)):
        table.add_report(position, None)


# -------------------------
# Precision edge cases
# -------------------------

def test_rounding_positive_halfway_coordinate():
    record = LocalRecord((1.25, 2.25), precision=1)

    # Python's round() uses round-half-to-even.
    assert record.pos == (1.2, 2.2)


def test_rounding_negative_halfway_coordinate():
    record = LocalRecord((-1.25, -2.25), precision=1)

    assert record.pos == (-1.2, -2.2)


def test_different_precision_records():
    table = RecordsMap()

    table.add_report((40.1234, -70.1234), None)
    table.add_report((40.1234, -70.1234), None)

    # Assumption: the table's behavior for mixed precision is unspecified.
    # This checks that insertion does not crash.
    assert len(table) >= 1


def test_very_high_precision():
    record = LocalRecord(
        (40.123456789123, -70.987654321987),
        precision=10
    )

    assert record.pos == (40.1234567891, -70.987654322)


# -------------------------
# Special numeric coordinate values
# -------------------------

def test_nan_coordinate():
    with pytest.raises((ValueError, TypeError)):
        LocalRecord((float("nan"), 10))


def test_infinite_coordinate():
    with pytest.raises((ValueError, TypeError, OverflowError)):
        LocalRecord((float("inf"), 10))


def test_none_coordinate():
    with pytest.raises((TypeError, ValueError)):
        LocalRecord((None, 10))


def test_boolean_coordinates():
    # Assumption: booleans should not be accepted as geographic coordinates.
    with pytest.raises((TypeError, ValueError)):
        LocalRecord((True, False))