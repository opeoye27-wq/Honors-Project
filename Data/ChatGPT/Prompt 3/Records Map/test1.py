
import pytest

# Assumption: The implementation provides a LocalRecord class and a hash table
# class that supports inserting, retrieving, and storing temperature records.
# The exact hash table class name and method names are not specified.
# These tests assume the module is named temperature_hash_table and that the
# hash table exposes insert(), get(), and len() operations.
# Adjust imports and method names to match the provided program.


from RecordsMap import LocalRecord, RecordsMap


class TestLocalRecord:

    def test_initialization_with_all_values(self):
        record = LocalRecord((10.123, 20.456), max=35.5, min=12.5, precision=2)

        assert record.pos == (10.12, 20.46)
        assert record.max == 35.5
        assert record.min == 12.5
        assert record.precision == 2

    def test_default_temperature_values(self):
        record = LocalRecord((10, 20))

        assert record.pos == (10, 20)
        assert record.max is None
        assert record.min is None

    def test_zero_coordinates(self):
        record = LocalRecord((0, 0))

        assert record.pos == (0, 0)

    def test_negative_coordinates(self):
        record = LocalRecord((-45.678, -90.123), precision=2)

        assert record.pos == (-45.68, -90.12)

    def test_rounding_coordinates(self):
        record = LocalRecord((12.3456, 98.7654), precision=2)

        assert record.pos == (12.35, 98.77)

    def test_zero_precision(self):
        record = LocalRecord((12.8, 45.6), precision=0)

        assert record.pos == (13, 46)

    def test_high_precision(self):
        record = LocalRecord((12.123456789, 45.987654321), precision=6)

        assert record.pos == (12.123457, 45.987654)

    def test_negative_temperature_values(self):
        record = LocalRecord((10, 20), max=-5, min=-25)

        assert record.max == -5
        assert record.min == -25

    def test_zero_temperature_values(self):
        record = LocalRecord((10, 20), max=0, min=0)

        assert record.max == 0
        assert record.min == 0

    def test_max_and_min_equal(self):
        record = LocalRecord((10, 20), max=25, min=25)

        assert record.max == record.min

    def test_invalid_position_length(self):
        with pytest.raises((ValueError, IndexError, TypeError)):
            LocalRecord((10,), max=30, min=10)

    def test_empty_position(self):
        with pytest.raises((ValueError, IndexError, TypeError)):
            LocalRecord(())

    def test_none_position(self):
        with pytest.raises((TypeError, ValueError, IndexError)):
            LocalRecord(None)

    def test_non_numeric_coordinates(self):
        with pytest.raises((TypeError, ValueError)):
            LocalRecord(("north", "east"))

    def test_non_numeric_temperature(self):
        record = LocalRecord((10, 20), max="hot", min="cold")

        # Temperature validation is not specified, so this behavior
        # is intentionally not assumed.


class TestHashTable:

    @pytest.fixture
    def table(self):
        return RecordsMap()

    def test_empty_table(self, table):
        assert len(table) == 0

    def test_insert_single_record(self, table):
        record = LocalRecord((10, 20), max=30, min=15)

        table.add_report(record.pos, record.max)

        assert table.get((10, 20)) is not None

    def test_insert_multiple_records(self, table):
        records = [
            LocalRecord((10, 20), max=30, min=15),
            LocalRecord((30, 40), max=35, min=10),
            LocalRecord((-10, -20), max=25, min=5),
        ]

        for record in records:
            table.add_report(record.pos, record.max)

        for record in records:
            retrieved = table.get(record.pos)
            assert retrieved is not None
            assert retrieved.max == record.max
            assert retrieved.min == record.min

    def test_retrieve_nonexistent_position(self, table):
        assert table.get((100, 100)) is None

    def test_duplicate_position(self, table):
        first = LocalRecord((10, 20), max=30, min=15)
        second = LocalRecord((10, 20), max=40, min=10)

        table.add_report(first.pos, first.max)
        table.add_report(second.pos, second.max)

        retrieved = table.get((10, 20))

        # Assumption: inserting a record at an existing position
        # replaces the previous record.
        assert retrieved.max == 40
        assert retrieved.min == 10

    def test_positions_rounded_to_same_key(self, table):
        first = LocalRecord((10.123, 20.456), max=30, min=15, precision=2)
        second = LocalRecord((10.124, 20.455), max=35, min=12, precision=2)

        table.add_report(first.pos, first.max)
        table.add_report(second.pos, second.max)

        assert table.get(first.pos) is not None

    def test_negative_coordinates(self, table):
        record = LocalRecord((-10.5, -20.5), max=25, min=5)

        table.add_report(record.pos, record.max)

        retrieved = table.get((-10.5, -20.5))
        assert retrieved.max == 25
        assert retrieved.min == 5

    def test_zero_coordinates(self, table):
        record = LocalRecord((0, 0), max=20, min=0)

        table.add_report(record.pos, record.max)

        retrieved = table.get((0, 0))
        assert retrieved is not None

    def test_large_coordinates(self, table):
        record = LocalRecord((1e10, -1e10), max=50, min=-50)

        table.add_report(record.pos, record.max)

        retrieved = table.get((1e10, -1e10))
        assert retrieved is not None

    def test_extreme_temperature_values(self, table):
        record = LocalRecord((10, 20), max=1e6, min=-1e6)

        table.add_report(record.pos, record.max)

        retrieved = table.get((10, 20))
        assert retrieved.max == 1e6
        assert retrieved.min == -1e6

    def test_negative_temperatures(self, table):
        record = LocalRecord((10, 20), max=-5, min=-30)

        table.add_report(record.pos, record.max)

        retrieved = table.get((10, 20))
        assert retrieved.max == -5
        assert retrieved.min == -30

    def test_same_temperature_values(self, table):
        record = LocalRecord((10, 20), max=15, min=15)

        table.add_report(record.pos, record.max)

        retrieved = table.get((10, 20))
        assert retrieved.max == retrieved.min

    def test_insert_record_with_missing_temperatures(self, table):
        record = LocalRecord((10, 20))

        table.add_report(record.pos, record.max)

        retrieved = table.get((10, 20))
        assert retrieved is not None
        assert retrieved.max is None
        assert retrieved.min is None

    def test_insert_many_records(self, table):
        records = [
            LocalRecord((i, i + 1), max=i * 2, min=-i)
            for i in range(1000)
        ]

        for record in records:
            table.add_report(record.pos, record.max)

        for record in records:
            retrieved = table.get(record.pos)
            assert retrieved is not None
            assert retrieved.max == record.max
            assert retrieved.min == record.min

    def test_repeated_retrieval(self, table):
        record = LocalRecord((10, 20), max=30, min=15)
        table.add_report(record.pos, record.max)

        for _ in range(100):
            retrieved = table.get((10, 20))
            assert retrieved.max == 30
            assert retrieved.min == 15

    def test_insert_after_retrieval(self, table):
        first = LocalRecord((10, 20), max=30, min=15)
        table.add_report(first.pos, first.max)

        table.get((10, 20))

        second = LocalRecord((30, 40), max=35, min=10)
        table.add_report(second.pos, second.max)

        assert table.get((30, 40)).max == 35
        assert table.get((10, 20)).max == 30

    def test_invalid_record_insertion(self, table):
        with pytest.raises((TypeError, AttributeError, ValueError)):
            table.add_report(None, None)

    def test_invalid_lookup_key(self, table):
        with pytest.raises((TypeError, ValueError, IndexError)):
            table.get(None)

    def test_lookup_with_incomplete_position(self, table):
        with pytest.raises((TypeError, ValueError, IndexError)):
            table.get((10,))

    def test_lookup_with_non_numeric_position(self, table):
        with pytest.raises((TypeError, ValueError)):
            table.get(("north", "east"))

    def test_lookup_with_list_position(self, table):
        # Assumption: positions are represented as tuples.
        # Whether lists are accepted is implementation-dependent.
        try:
            result = table.get([10, 20])
            assert result is None or isinstance(result, LocalRecord)
        except (TypeError, ValueError):
            pass

    def test_lookup_with_different_precision(self, table):
        record = LocalRecord((10.123, 20.456), max=30, min=15, precision=2)
        table.add_report(record.pos, record.max)

        # Assumption: lookup uses the same coordinate normalization
        # as insertion.
        assert table.get((10.12, 20.46)) is not None


class TestHashTableEdgeCases:

    @pytest.fixture
    def table(self):
        return RecordsMap()

    def test_multiple_distinct_positions_with_similar_hashes(self, table):
        records = [
            LocalRecord((i, i + 100), max=i, min=-i)
            for i in range(100)
        ]

        for record in records:
            table.add_report(record.pos, record.max)

        for record in records:
            retrieved = table.get(record.pos)
            assert retrieved.max == record.max
            assert retrieved.min == record.min

    def test_insert_same_record_repeatedly(self, table):
        record = LocalRecord((10, 20), max=30, min=15)

        for _ in range(10):
            table.add_report(record.pos, record.max)

        retrieved = table.get((10, 20))
        assert retrieved.max == 30
        assert retrieved.min == 15

    def test_insert_records_in_reverse_order(self, table):
        records = [
            LocalRecord((i, i + 1), max=i, min=-i)
            for i in range(50)
        ]

        for record in reversed(records):
            table.add_report(record.pos, record.max)

        for record in records:
            assert table.get(record.pos) is not None

    def test_insert_after_many_collisions(self, table):
        records = [
            LocalRecord((i, 0), max=i, min=-i)
            for i in range(500)
        ]

        for record in records:
            table.add_report(record.pos, record.max)

        extra = LocalRecord((1000, 0), max=1000, min=-1000)
        table.add_report(extra.pos, extra.max)

        retrieved = table.get((1000, 0))
        assert retrieved.max == 1000
        assert retrieved.min == -1000

    def test_insert_float_and_integer_equivalent_coordinates(self, table):
        record = LocalRecord((10, 20), max=30, min=15)
        table.add_report(record.pos, record.max)

        # Assumption: Python numeric equality makes (10, 20)
        # equivalent to (10.0, 20.0).
        retrieved = table.get((10.0, 20.0))
        assert retrieved is not None

    def test_temperature_values_do_not_affect_position_lookup(self, table):
        first = LocalRecord((10, 20), max=30, min=15)
        second = LocalRecord((30, 40), max=30, min=15)

        table.add_report(first.pos, first.max)
        table.add_report(second.pos, second.max)

        assert table.get((10, 20)).pos == (10, 20)
        assert table.get((30, 40)).pos == (30, 40)