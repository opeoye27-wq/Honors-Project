
import pytest
from RecordsMap import LocalRecord, RecordsMap


class TestLocalRecord:

    def test_initialization(self):
        record = LocalRecord((10, 20))
        assert record.pos == (10, 20)

    def test_initialization_with_temperatures(self):
        record = LocalRecord((10, 20), max=30, min=10)
        assert record.min == 10
        assert record.max == 30

    def test_coordinate_rounding(self):
        record = LocalRecord((10.4, 20.6))
        assert record.pos == (10, 21)

    def test_negative_coordinates(self):
        record = LocalRecord((-10.4, -20.6))
        assert record.pos == (-10, -21)

    def test_add_first_report(self):
        record = LocalRecord((1, 2))
        record.add_report(25)
        assert record.min == 25
        assert record.max == 25

    def test_add_lower_temperature(self):
        record = LocalRecord((1, 2), max=30, min=20)
        record.add_report(10)
        assert record.min == 10
        assert record.max == 30

    def test_add_higher_temperature(self):
        record = LocalRecord((1, 2), max=30, min=20)
        record.add_report(40)
        assert record.min == 20
        assert record.max == 40

    def test_add_temperature_between_extremes(self):
        record = LocalRecord((1, 2), max=30, min=10)
        record.add_report(20)
        assert record.min == 10
        assert record.max == 30

    def test_add_negative_temperature(self):
        record = LocalRecord((1, 2))
        record.add_report(-15)
        assert record.min == -15
        assert record.max == -15

    def test_add_zero_temperature(self):
        record = LocalRecord((1, 2))
        record.add_report(0)
        assert record.min == 0
        assert record.max == 0

    def test_repeated_identical_reports(self):
        record = LocalRecord((1, 2))
        for _ in range(5):
            record.add_report(15)
        assert record.min == 15
        assert record.max == 15

    def test_equality_same_position(self):
        record1 = LocalRecord((10.2, 20.3))
        record2 = LocalRecord((10.4, 20.1))
        assert record1 == record2

    def test_inequality_different_positions(self):
        record1 = LocalRecord((10, 20))
        record2 = LocalRecord((11, 20))
        assert record1 != record2

    def test_hash_equal_for_same_rounded_position(self):
        record1 = LocalRecord((10.2, 20.3))
        record2 = LocalRecord((10.4, 20.1))
        assert hash(record1) == hash(record2)


class TestRecordsMap:

    def test_empty_table_has_zero_length(self):
        table = RecordsMap()
        assert len(table) == 0

    def test_empty_table_does_not_contain_position(self):
        table = RecordsMap()
        assert (1, 2) not in table

    def test_insert_first_record(self):
        table = RecordsMap()
        table.add_report((10, 20), 25)

        assert len(table) == 1
        assert (10, 20) in table
        assert table[(10, 20)] == (25, 25)

    def test_insert_multiple_unique_positions(self):
        table = RecordsMap()
        table.add_report((1, 2), 10)
        table.add_report((3, 4), 20)
        table.add_report((5, 6), 30)

        assert len(table) == 3

    def test_multiple_reports_same_position(self):
        table = RecordsMap()
        table.add_report((1, 2), 20)
        table.add_report((1, 2), 30)
        table.add_report((1, 2), 10)

        assert len(table) == 1
        assert table[(1, 2)] == (10, 30)

    def test_update_minimum_temperature(self):
        table = RecordsMap()
        table.add_report((1, 2), 30)
        table.add_report((1, 2), 10)

        assert table[(1, 2)] == (10, 30)
        assert len(table) == 1

    def test_update_maximum_temperature(self):
        table = RecordsMap()
        table.add_report((1, 2), 10)
        table.add_report((1, 2), 30)

        assert table[(1, 2)] == (10, 30)
        assert len(table) == 1

    def test_temperature_between_existing_extremes(self):
        table = RecordsMap()
        table.add_report((1, 2), 10)
        table.add_report((1, 2), 30)
        table.add_report((1, 2), 20)

        assert table[(1, 2)] == (10, 30)
        assert len(table) == 1

    def test_negative_temperatures(self):
        table = RecordsMap()
        table.add_report((1, 2), -10)
        table.add_report((1, 2), -30)
        table.add_report((1, 2), -5)

        assert table[(1, 2)] == (-30, -5)

    def test_zero_temperature(self):
        table = RecordsMap()
        table.add_report((1, 2), 0)

        assert table[(1, 2)] == (0, 0)

    def test_mixed_positive_negative_and_zero_temperatures(self):
        table = RecordsMap()
        table.add_report((1, 2), -10)
        table.add_report((1, 2), 0)
        table.add_report((1, 2), 15)

        assert table[(1, 2)] == (-10, 15)

    def test_duplicate_rounded_coordinates(self):
        table = RecordsMap()
        table.add_report((10.2, 20.3), 15)
        table.add_report((10.4, 20.1), 25)

        assert len(table) == 1
        assert table[(10, 20)] == (15, 25)

    def test_lookup_using_different_rounded_coordinates(self):
        table = RecordsMap()
        table.add_report((10.2, 20.3), 15)

        assert table[(10.4, 20.1)] == (15, 15)

    def test_coordinates_round_to_different_positions(self):
        table = RecordsMap()
        table.add_report((10.2, 20.3), 15)
        table.add_report((10.7, 20.3), 25)

        assert len(table) == 2

    def test_negative_coordinates(self):
        table = RecordsMap()
        table.add_report((-10.2, -20.3), 15)

        assert (-10, -20) in table
        assert table[(-10, -20)] == (15, 15)

    def test_zero_coordinates(self):
        table = RecordsMap()
        table.add_report((0, 0), 10)

        assert (0, 0) in table
        assert table[(0, 0)] == (10, 10)

    def test_missing_position_raises_key_error(self):
        table = RecordsMap()
        with pytest.raises(KeyError):
            table[(100, 200)]

    def test_missing_position_does_not_change_length(self):
        table = RecordsMap()
        table.add_report((1, 2), 10)

        with pytest.raises(KeyError):
            table[(3, 4)]

        assert len(table) == 1

    def test_contains_existing_position(self):
        table = RecordsMap()
        table.add_report((1, 2), 10)

        assert (1, 2) in table

    def test_contains_missing_position(self):
        table = RecordsMap()
        table.add_report((1, 2), 10)

        assert (3, 4) not in table

    def test_contains_rounded_position(self):
        table = RecordsMap()
        table.add_report((10.2, 20.3), 10)

        assert (10.4, 20.1) in table

    def test_length_does_not_increase_for_duplicate_positions(self):
        table = RecordsMap()

        for temperature in [10, 20, 30, 40, 50]:
            table.add_report((1, 2), temperature)

        assert len(table) == 1

    def test_length_increases_only_for_unique_positions(self):
        table = RecordsMap()
        table.add_report((1, 2), 10)
        table.add_report((1, 2), 20)
        table.add_report((3, 4), 30)
        table.add_report((5, 6), 40)
        table.add_report((3, 4), 50)

        assert len(table) == 3

    def test_multiple_records_preserve_independent_temperatures(self):
        table = RecordsMap()
        table.add_report((1, 2), 10)
        table.add_report((3, 4), 20)
        table.add_report((5, 6), 30)

        table.add_report((1, 2), 5)
        table.add_report((3, 4), 25)
        table.add_report((5, 6), 35)

        assert table[(1, 2)] == (5, 10)
        assert table[(3, 4)] == (20, 25)
        assert table[(5, 6)] == (30, 35)

    def test_hash_collisions_preserve_all_records(self, monkeypatch):
        table = RecordsMap()

        # Force every position into the same bucket.
        monkeypatch.setattr(table, "_hash", lambda pos: 0)

        positions = [(1, 2), (3, 4), (5, 6), (7, 8)]

        for i, pos in enumerate(positions):
            table.add_report(pos, i * 10)

        assert len(table) == 4

        for i, pos in enumerate(positions):
            assert pos in table
            assert table[pos] == (i * 10, i * 10)

    def test_collisions_do_not_overwrite_existing_records(self, monkeypatch):
        table = RecordsMap()
        monkeypatch.setattr(table, "_hash", lambda pos: 0)

        table.add_report((1, 2), 10)
        table.add_report((3, 4), 20)
        table.add_report((1, 2), 5)

        assert len(table) == 2
        assert table[(1, 2)] == (5, 10)
        assert table[(3, 4)] == (20, 20)

    def test_resize_preserves_all_existing_records(self):
        table = RecordsMap(capacity=8)

        positions = [
            (1, 2),
            (3, 4),
            (5, 6),
            (7, 8),
            (9, 10),
            (11, 12)
        ]

        for i, pos in enumerate(positions):
            table.add_report(pos, i * 10)

        assert len(table) == 6

        for i, pos in enumerate(positions):
            assert pos in table
            assert table[pos] == (i * 10, i * 10)

    def test_resize_preserves_minimum_and_maximum_temperatures(self):
        table = RecordsMap(capacity=8)

        table.add_report((1, 2), 10)
        table.add_report((1, 2), 30)
        table.add_report((3, 4), -10)
        table.add_report((3, 4), 20)
        table.add_report((5, 6), 0)
        table.add_report((5, 6), 15)

        # Adding another unique position causes the load factor
        # to exceed 0.7.
        table.add_report((7, 8), 100)

        assert table[(1, 2)] == (10, 30)
        assert table[(3, 4)] == (-10, 20)
        assert table[(5, 6)] == (0, 15)
        assert table[(7, 8)] == (100, 100)

        assert len(table) == 4

    def test_updates_after_resizing(self):
        table = RecordsMap(capacity=8)

        for i in range(7):
            table.add_report((i, i + 1), i * 10)

        table.add_report((0, 1), -50)
        table.add_report((0, 1), 100)

        assert len(table) == 7
        assert table[(0, 1)] == (-50, 100)

    def test_duplicate_positions_after_resizing(self):
        table = RecordsMap(capacity=8)

        for i in range(7):
            table.add_report((i, i + 1), i * 10)

        table.add_report((0.2, 1.2), 100)

        assert len(table) == 7
        assert table[(0, 1)] == (0, 100)

    def test_multiple_resizes_preserve_records(self):
        table = RecordsMap(capacity=4)

        positions = [(i, i + 1) for i in range(30)]

        for i, pos in enumerate(positions):
            table.add_report(pos, i - 15)

        assert len(table) == 30

        for i, pos in enumerate(positions):
            assert pos in table
            assert table[pos] == (i - 15, i - 15)

    def test_multiple_resizes_preserve_updated_extremes(self):
        table = RecordsMap(capacity=4)

        table.add_report((100, 200), -20)
        table.add_report((100, 200), 40)

        for i in range(30):
            table.add_report((i, i + 1), i)

        assert table[(100, 200)] == (-20, 40)
        assert len(table) == 31

    def test_collisions_during_resizing(self, monkeypatch):
        table = RecordsMap(capacity=4)
        monkeypatch.setattr(table, "_hash", lambda pos: 0)

        for i in range(10):
            table.add_report((i, i + 1), i * 5)

        assert len(table) == 10

        for i in range(10):
            assert table[(i, i + 1)] == (i * 5, i * 5)

    def test_repeated_updates_do_not_trigger_additional_records(self):
        table = RecordsMap(capacity=8)

        for i in range(100):
            table.add_report((1, 2), i - 50)

        assert len(table) == 1
        assert table[(1, 2)] == (-50, 49)

    def test_all_records_remain_accessible_after_many_updates(self):
        table = RecordsMap(capacity=4)

        for i in range(20):
            table.add_report((i, i + 1), i)

        for i in range(20):
            table.add_report((i, i + 1), -i)

        assert len(table) == 20

        for i in range(20):
            assert table[(i, i + 1)] == (-i, i)

    def test_lookup_does_not_modify_record(self):
        table = RecordsMap()
        table.add_report((1, 2), 10)
        table.add_report((1, 2), 30)

        first_lookup = table[(1, 2)]
        second_lookup = table[(1, 2)]

        assert first_lookup == second_lookup
        assert len(table) == 1

    def test_inserting_new_position_after_updates(self):
        table = RecordsMap()
        table.add_report((1, 2), 10)
        table.add_report((1, 2), 20)
        table.add_report((3, 4), 30)

        assert len(table) == 2
        assert table[(1, 2)] == (10, 20)
        assert table[(3, 4)] == (30, 30)
