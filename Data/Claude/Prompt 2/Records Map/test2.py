
"""
Unit tests (pytest) for a hash table storing min/max temperature records by position.

The description does not define the public API, so every name below is an ASSUMPTION.
If your program uses different names, edit ONLY the adapter section.

ASSUMPTIONS
A1. Module `temperature_table` exposes class `TemperatureHashTable`, constructible with no arguments.
A2. Reporting a temperature: `table.report(x, y, temperature)`. Positions are two numeric args.
A3. Lookups: `table.get_min(x, y)` and `table.get_max(x, y)`. Both raise KeyError if the
    (rounded) position has no record.
A4. Membership: `(x, y) in table` returns True/False and never raises for missing positions.
A5. Unique position count: `len(table)`.
A6. Current bucket count: `table.capacity` (int). The description mentions capacity but
    gives no attribute name.
A7. Resizing is performed so that after every completed `report`, len/capacity <= 0.7.
    (The description says capacity grows when the load factor "exceeds 0.7"; whether the check
    happens before or after insertion is ambiguous. I assume after.)
A8. Rounding "to the nearest whole number" at exact .5 ties is ambiguous (Python's round() uses
    banker's rounding, half-up differs). Tie values (x.5) are therefore NOT tested.
A9. Behavior for non-numeric coordinates or temperatures is unspecified. One test below
    assumes TypeError or ValueError; delete it if your program differs.
A10. Hash collisions cannot be forced without knowing the hash function. They are exercised by
     inserting a large number of positions (collisions are then effectively unavoidable), and
     by a dense grid of nearby integer positions.
"""

import pytest

from RecordsMap import RecordsMap  # noqa: E402


# ----------------------------------------------------------------------------
# Adapter section: change only these if your API differs
# ----------------------------------------------------------------------------
def report(table, x, y, temp):
    table.add_report((x, y), temp)


def get_min(table, x, y):
    return table[(x, y)][0]


def get_max(table, x, y):
    return table[(x, y)][1]


def has(table, x, y):
    return (x, y) in table


def size(table):
    return len(table)


def capacity(table):
    return table.capacity


MAX_LOAD = 0.7


@pytest.fixture
def table():
    return RecordsMap()


# ----------------------------------------------------------------------------
# Empty table
# ----------------------------------------------------------------------------
class TestEmptyTable:
    def test_size_is_zero(self, table):
        assert size(table) == 0

    def test_contains_is_false(self, table):
        assert has(table, 0, 0) is False
        assert has(table, 5, -7) is False

    def test_get_min_raises_key_error(self, table):
        with pytest.raises(KeyError):
            get_min(table, 0, 0)

    def test_get_max_raises_key_error(self, table):
        with pytest.raises(KeyError):
            get_max(table, 0, 0)

    def test_capacity_is_positive(self, table):
        assert capacity(table) > 0


# ----------------------------------------------------------------------------
# Creating new records
# ----------------------------------------------------------------------------
class TestNewRecords:
    def test_first_report_sets_min_and_max_to_reported_value(self, table):
        report(table, 10, 20, 15)
        assert get_min(table, 10, 20) == 15
        assert get_max(table, 10, 20) == 15

    def test_first_report_creates_one_record(self, table):
        report(table, 10, 20, 15)
        assert size(table) == 1
        assert has(table, 10, 20) is True

    @pytest.mark.parametrize("temp", [-100, -40.5, -1, 0, 0.0, 1, 25.75, 1000])
    def test_new_record_with_various_temperatures(self, table, temp):
        report(table, 3, 4, temp)
        assert get_min(table, 3, 4) == temp
        assert get_max(table, 3, 4) == temp

    def test_zero_temperature_record_is_stored_not_treated_as_missing(self, table):
        report(table, 1, 1, 0)
        assert has(table, 1, 1) is True
        assert get_min(table, 1, 1) == 0
        assert get_max(table, 1, 1) == 0
        assert size(table) == 1

    def test_negative_temperature_record(self, table):
        report(table, 1, 1, -30)
        assert get_min(table, 1, 1) == -30
        assert get_max(table, 1, 1) == -30

    def test_origin_position(self, table):
        report(table, 0, 0, 5)
        assert has(table, 0, 0) is True
        assert get_min(table, 0, 0) == 5

    def test_negative_coordinates(self, table):
        report(table, -45, -170, 12)
        assert has(table, -45, -170) is True
        assert get_min(table, -45, -170) == 12
        assert get_max(table, -45, -170) == 12

    def test_distinct_positions_create_distinct_records(self, table):
        report(table, 1, 2, 10)
        report(table, 3, 4, 20)
        assert size(table) == 2
        assert get_min(table, 1, 2) == 10
        assert get_max(table, 1, 2) == 10
        assert get_min(table, 3, 4) == 20
        assert get_max(table, 3, 4) == 20

    def test_swapped_coordinates_are_different_positions(self, table):
        report(table, 1, 2, 10)
        report(table, 2, 1, 99)
        assert size(table) == 2
        assert get_max(table, 1, 2) == 10
        assert get_max(table, 2, 1) == 99

    def test_sign_flipped_coordinates_are_different_positions(self, table):
        report(table, 5, 5, 1)
        report(table, -5, 5, 2)
        report(table, 5, -5, 3)
        report(table, -5, -5, 4)
        assert size(table) == 4
        assert get_min(table, 5, 5) == 1
        assert get_min(table, -5, 5) == 2
        assert get_min(table, 5, -5) == 3
        assert get_min(table, -5, -5) == 4


# ----------------------------------------------------------------------------
# Updating min / max, repeated reports
# ----------------------------------------------------------------------------
class TestUpdates:
    def test_repeated_identical_reports_keep_one_record(self, table):
        for _ in range(10):
            report(table, 7, 7, 20)
        assert size(table) == 1
        assert get_min(table, 7, 7) == 20
        assert get_max(table, 7, 7) == 20

    def test_lower_temperature_updates_min_only(self, table):
        report(table, 0, 0, 10)
        report(table, 0, 0, 3)
        assert get_min(table, 0, 0) == 3
        assert get_max(table, 0, 0) == 10
        assert size(table) == 1

    def test_higher_temperature_updates_max_only(self, table):
        report(table, 0, 0, 10)
        report(table, 0, 0, 18)
        assert get_min(table, 0, 0) == 10
        assert get_max(table, 0, 0) == 18
        assert size(table) == 1

    def test_temperature_between_min_and_max_changes_nothing(self, table):
        report(table, 0, 0, 0)
        report(table, 0, 0, 20)
        report(table, 0, 0, 10)
        assert get_min(table, 0, 0) == 0
        assert get_max(table, 0, 0) == 20

    def test_temperature_equal_to_current_min_or_max_changes_nothing(self, table):
        report(table, 0, 0, -5)
        report(table, 0, 0, 5)
        report(table, 0, 0, -5)
        report(table, 0, 0, 5)
        assert get_min(table, 0, 0) == -5
        assert get_max(table, 0, 0) == 5

    def test_sequence_of_updates(self, table):
        temps = [10, 12, 8, 15, 7, 9, 15, 7, 11]
        for t in temps:
            report(table, 4, 4, t)
        assert get_min(table, 4, 4) == min(temps)
        assert get_max(table, 4, 4) == max(temps)
        assert size(table) == 1

    def test_min_and_max_across_negative_zero_and_positive(self, table):
        for t in [0, -10, 10, -3, 3]:
            report(table, 2, 2, t)
        assert get_min(table, 2, 2) == -10
        assert get_max(table, 2, 2) == 10

    def test_all_negative_temperatures(self, table):
        for t in [-5, -20, -1, -12]:
            report(table, 9, 9, t)
        assert get_min(table, 9, 9) == -20
        assert get_max(table, 9, 9) == -1

    def test_all_zero_temperatures(self, table):
        for _ in range(3):
            report(table, 9, 9, 0)
        assert get_min(table, 9, 9) == 0
        assert get_max(table, 9, 9) == 0

    def test_float_temperatures(self, table):
        for t in [20.5, 19.25, 21.75, 20.0]:
            report(table, 1, 1, t)
        assert get_min(table, 1, 1) == pytest.approx(19.25)
        assert get_max(table, 1, 1) == pytest.approx(21.75)

    def test_updating_one_position_does_not_affect_another(self, table):
        report(table, 1, 1, 10)
        report(table, 2, 2, 50)
        report(table, 1, 1, -10)
        report(table, 1, 1, 30)
        assert get_min(table, 1, 1) == -10
        assert get_max(table, 1, 1) == 30
        assert get_min(table, 2, 2) == 50
        assert get_max(table, 2, 2) == 50
        assert size(table) == 2

    def test_very_large_and_small_temperatures(self, table):
        report(table, 0, 0, 1e9)
        report(table, 0, 0, -1e9)
        assert get_max(table, 0, 0) == 1e9
        assert get_min(table, 0, 0) == -1e9

    def test_update_does_not_change_count_of_other_records(self, table):
        for i in range(5):
            report(table, i, i, i)
        before = size(table)
        for _ in range(20):
            report(table, 2, 2, 100)
        assert size(table) == before


# ----------------------------------------------------------------------------
# Coordinate rounding (A8: exact .5 ties intentionally not tested)
# ----------------------------------------------------------------------------
class TestRounding:
    @pytest.mark.parametrize(
        "x, y",
        [
            (1.2, 2.3),
            (0.8, 1.9),
            (1.49, 2.01),
            (1.0, 2.0),
            (1, 2),
            (0.6, 2.4),
        ],
    )
    def test_coordinates_rounding_to_same_pair_share_one_record(self, table, x, y):
        report(table, 1, 2, 10)
        report(table, x, y, 20)
        assert size(table) == 1
        assert get_min(table, 1, 2) == 10
        assert get_max(table, 1, 2) == 20

    def test_lookup_with_unrounded_coordinates_finds_record(self, table):
        report(table, 1, 2, 10)
        assert has(table, 1.3, 1.8) is True
        assert get_min(table, 1.3, 1.8) == 10
        assert get_max(table, 1.3, 1.8) == 10

    def test_report_with_unrounded_coordinates_found_by_integer_lookup(self, table):
        report(table, 3.4, -7.6, 8)
        assert has(table, 3, -8) is True
        assert get_min(table, 3, -8) == 8

    def test_updates_via_different_unrounded_forms_merge(self, table):
        report(table, 5.1, 5.1, 10)
        report(table, 4.9, 4.9, 2)
        report(table, 5.4, 4.6, 30)
        assert size(table) == 1
        assert get_min(table, 5, 5) == 2
        assert get_max(table, 5, 5) == 30

    @pytest.mark.parametrize(
        "x, y",
        [
            (1.6, 2.0),  # x rounds to 2
            (1.0, 2.6),  # y rounds to 3
            (0.4, 2.0),  # x rounds to 0
            (1.0, 1.4),  # y rounds to 1
        ],
    )
    def test_coordinates_rounding_to_different_pair_are_distinct(self, table, x, y):
        report(table, 1, 2, 10)
        report(table, x, y, 99)
        assert size(table) == 2
        assert get_max(table, 1, 2) == 10
        assert get_max(table, x, y) == 99

    def test_negative_coordinates_rounding_to_same_pair(self, table):
        report(table, -1.2, -2.3, 10)
        report(table, -0.8, -1.9, 20)
        assert size(table) == 1
        assert get_min(table, -1, -2) == 10
        assert get_max(table, -1, -2) == 20

    def test_small_values_around_zero_round_to_origin(self, table):
        report(table, 0, 0, 1)
        report(table, 0.3, -0.3, 2)
        report(table, -0.4, 0.4, 3)
        assert size(table) == 1
        assert get_min(table, 0, 0) == 1
        assert get_max(table, 0, 0) == 3

    def test_negative_zero_equals_zero(self, table):
        report(table, 0.0, 0.0, 1)
        report(table, -0.0, -0.0, 2)
        assert size(table) == 1
        assert get_max(table, 0, 0) == 2

    def test_integer_and_float_forms_of_same_coordinate_match(self, table):
        report(table, 7, 8, 1)
        report(table, 7.0, 8.0, 2)
        assert size(table) == 1

    def test_large_coordinates(self, table):
        report(table, 1_000_000.2, -1_000_000.2, 5)
        assert has(table, 1_000_000, -1_000_000) is True
        assert get_min(table, 1_000_000, -1_000_000) == 5

    def test_rounding_collapses_many_inputs_into_one_record(self, table):
        for dx in (-0.4, -0.2, 0.0, 0.2, 0.4):
            for dy in (-0.4, -0.2, 0.0, 0.2, 0.4):
                report(table, 10 + dx, 20 + dy, 10 + dx * 10 + dy)
        assert size(table) == 1
        assert has(table, 10, 20) is True


# ----------------------------------------------------------------------------
# Missing positions
# ----------------------------------------------------------------------------
class TestMissingPositions:
    def test_get_min_missing_raises_key_error(self, table):
        report(table, 1, 1, 10)
        with pytest.raises(KeyError):
            get_min(table, 2, 2)

    def test_get_max_missing_raises_key_error(self, table):
        report(table, 1, 1, 10)
        with pytest.raises(KeyError):
            get_max(table, 2, 2)

    def test_contains_missing_is_false(self, table):
        report(table, 1, 1, 10)
        assert has(table, 2, 2) is False

    def test_neighbor_that_rounds_differently_is_missing(self, table):
        report(table, 1, 1, 10)
        assert has(table, 1.6, 1) is False
        with pytest.raises(KeyError):
            get_min(table, 1.6, 1)

    def test_failed_lookup_does_not_create_record(self, table):
        with pytest.raises(KeyError):
            get_min(table, 5, 5)
        assert size(table) == 0
        assert has(table, 5, 5) is False

    def test_contains_does_not_create_record(self, table):
        has(table, 5, 5)
        assert size(table) == 0

    def test_successful_lookups_do_not_change_values_or_count(self, table):
        report(table, 1, 1, 10)
        for _ in range(5):
            get_min(table, 1, 1)
            get_max(table, 1, 1)
            has(table, 1, 1)
        assert size(table) == 1
        assert get_min(table, 1, 1) == 10
        assert get_max(table, 1, 1) == 10

    def test_missing_position_with_same_x_or_y_as_existing(self, table):
        report(table, 1, 1, 10)
        assert has(table, 1, 2) is False
        assert has(table, 2, 1) is False

    def test_key_error_when_table_has_many_records(self, table):
        for i in range(100):
            report(table, i, i, i)
        with pytest.raises(KeyError):
            get_min(table, 1000, 1000)
        with pytest.raises(KeyError):
            get_max(table, -1, -1)


# ----------------------------------------------------------------------------
# Hash collisions (A10): large numbers of positions force bucket sharing
# ----------------------------------------------------------------------------
class TestCollisions:
    def test_dense_grid_all_records_retrievable(self, table):
        n = 30  # 900 positions
        for x in range(n):
            for y in range(n):
                report(table, x, y, x * 100 + y)
        assert size(table) == n * n
        for x in range(n):
            for y in range(n):
                assert get_min(table, x, y) == x * 100 + y
                assert get_max(table, x, y) == x * 100 + y

    def test_dense_grid_with_negative_coordinates(self, table):
        for x in range(-15, 15):
            for y in range(-15, 15):
                report(table, x, y, x - y)
        assert size(table) == 900
        for x in range(-15, 15):
            for y in range(-15, 15):
                assert get_min(table, x, y) == x - y
                assert get_max(table, x, y) == x - y

    def test_updates_stay_independent_among_many_positions(self, table):
        positions = [(x, y) for x in range(20) for y in range(20)]
        for (x, y) in positions:
            report(table, x, y, 50)
        for (x, y) in positions:
            report(table, x, y, 50 - (x + y))  # new min
            report(table, x, y, 50 + (x * y))  # new max
        assert size(table) == len(positions)
        for (x, y) in positions:
            assert get_min(table, x, y) == min(50, 50 - (x + y))
            assert get_max(table, x, y) == max(50, 50 + (x * y))

    def test_missing_lookup_still_raises_in_crowded_table(self, table):
        for x in range(30):
            for y in range(30):
                report(table, x, y, 1)
        with pytest.raises(KeyError):
            get_min(table, 30, 30)
        with pytest.raises(KeyError):
            get_max(table, -1, 0)
        assert has(table, 30, 30) is False

    def test_positions_with_equal_coordinate_sums_do_not_merge(self, table):
        # (a, b) with identical a + b are a common collision pattern for naive hashes.
        for a in range(0, 25):
            report(table, a, 24 - a, a)
        assert size(table) == 25
        for a in range(0, 25):
            assert get_min(table, a, 24 - a) == a

    def test_swapped_pairs_remain_distinct_in_crowded_table(self, table):
        # (a, b) and (b, a) are another common collision pattern for naive hashes.
        for a in range(15):
            for b in range(15):
                report(table, a, b, a * 1000 + b)
        for a in range(15):
            for b in range(15):
                assert get_max(table, a, b) == a * 1000 + b


# ----------------------------------------------------------------------------
# Resizing / rehashing
# ----------------------------------------------------------------------------
def _insert_until_capacity_grows(table, limit=10_000):
    """Insert distinct positions until capacity increases. Returns inserted records."""
    initial = capacity(table)
    inserted = {}
    i = 0
    while capacity(table) == initial and i < limit:
        temp = (i * 7) % 50 - 25
        report(table, i, -i, temp)
        inserted[(i, -i)] = temp
        i += 1
    return initial, inserted


class TestResizing:
    def test_capacity_increases_when_load_factor_exceeded(self, table):
        initial, inserted = _insert_until_capacity_grows(table)
        assert capacity(table) > initial, "capacity never grew despite many insertions"

    def test_growth_happens_only_after_load_factor_would_exceed_limit(self, table):
        # Capacity must not grow while the load factor stays at or below 0.7.
        initial = capacity(table)
        max_without_growth = int(initial * MAX_LOAD)
        for i in range(max_without_growth):
            report(table, i, i, i)
        assert capacity(table) == initial

    def test_records_preserved_after_resize(self, table):
        initial, inserted = _insert_until_capacity_grows(table)
        assert capacity(table) > initial
        assert size(table) == len(inserted)
        for (x, y), temp in inserted.items():
            assert has(table, x, y) is True
            assert get_min(table, x, y) == temp
            assert get_max(table, x, y) == temp

    def test_min_max_preserved_after_resize(self, table):
        # Give early records distinct min/max, then force at least one resize.
        for i in range(3):
            report(table, i, i, 10 + i)
            report(table, i, i, -(10 + i))
        initial = capacity(table)
        j = 100
        while capacity(table) == initial and j < 10_000:
            report(table, j, j, 0)
            j += 1
        assert capacity(table) > initial
        for i in range(3):
            assert get_min(table, i, i) == -(10 + i)
            assert get_max(table, i, i) == 10 + i

    def test_count_unchanged_by_resize(self, table):
        count_before_growth = 0
        initial = capacity(table)
        i = 0
        while capacity(table) == initial and i < 10_000:
            report(table, i, 0, i)
            i += 1
            count_before_growth = i
        assert size(table) == count_before_growth

    def test_load_factor_never_exceeds_limit_after_each_insertion(self, table):  # A7
        for i in range(500):
            report(table, i, i * 2, i)
            assert size(table) / capacity(table) <= MAX_LOAD + 1e-9

    def test_repeated_reports_do_not_trigger_growth(self, table):
        report(table, 1, 1, 0)
        initial = capacity(table)
        for t in range(1000):
            report(table, 1, 1, t)
        assert capacity(table) == initial
        assert size(table) == 1
        assert get_min(table, 1, 1) == 0
        assert get_max(table, 1, 1) == 999

    def test_rounding_duplicates_do_not_trigger_growth(self, table):
        report(table, 5, 5, 0)
        initial = capacity(table)
        for k in range(200):
            report(table, 5 + (k % 5) * 0.1, 5 - (k % 5) * 0.1, k)
        assert size(table) == 1
        assert capacity(table) == initial

    def test_updates_after_resize_work(self, table):
        initial, inserted = _insert_until_capacity_grows(table)
        assert capacity(table) > initial
        for (x, y), temp in inserted.items():
            report(table, x, y, temp - 100)
            report(table, x, y, temp + 100)
        assert size(table) == len(inserted)
        for (x, y), temp in inserted.items():
            assert get_min(table, x, y) == temp - 100
            assert get_max(table, x, y) == temp + 100

    def test_new_inserts_after_resize_work(self, table):
        initial, inserted = _insert_until_capacity_grows(table)
        assert capacity(table) > initial
        n = len(inserted)
        for k in range(50):
            report(table, 10_000 + k, 10_000 + k, k)
        assert size(table) == n + 50
        for k in range(50):
            assert get_min(table, 10_000 + k, 10_000 + k) == k
        for (x, y), temp in inserted.items():
            assert get_max(table, x, y) == temp

    def test_missing_lookup_still_raises_after_resize(self, table):
        initial, inserted = _insert_until_capacity_grows(table)
        assert capacity(table) > initial
        with pytest.raises(KeyError):
            get_min(table, 999_999, 999_999)
        assert has(table, 999_999, 999_999) is False

    def test_rounding_still_applies_after_resize(self, table):
        initial, inserted = _insert_until_capacity_grows(table)
        assert capacity(table) > initial
        x, y = next(iter(inserted))
        temp = inserted[(x, y)]
        assert has(table, x + 0.3, y - 0.3) is True
        report(table, x + 0.3, y - 0.3, temp + 1000)
        assert size(table) == len(inserted)
        assert get_max(table, x, y) == temp + 1000

    def test_multiple_consecutive_resizes_preserve_everything(self, table):
        expected = {}
        for i in range(2000):
            temp = (i * 31) % 97 - 48
            report(table, i, (i * 3) % 101, temp)
            expected[(i, (i * 3) % 101)] = temp
        assert size(table) == len(expected)
        for (x, y), temp in expected.items():
            assert get_min(table, x, y) == temp
            assert get_max(table, x, y) == temp
        assert size(table) / capacity(table) <= MAX_LOAD + 1e-9  # A7

    def test_capacity_never_decreases(self, table):
        last = capacity(table)
        for i in range(500):
            report(table, i, i, i)
            current = capacity(table)
            assert current >= last
            last = current

    def test_resize_with_zero_and_negative_temperatures_preserved(self, table):
        temps = {}
        for i in range(300):
            t = [0, -1, -50, 0.0, -0.5][i % 5]
            report(table, -i, i, t)
            temps[(-i, i)] = t
        for (x, y), t in temps.items():
            assert get_min(table, x, y) == t
            assert get_max(table, x, y) == t


# ----------------------------------------------------------------------------
# Mixed scenario
# ----------------------------------------------------------------------------
class TestIntegrationScenarios:
    def test_mixed_workload_matches_reference_model(self, table):
        reference = {}  # (rx, ry) -> [min, max]
        reports = []
        for i in range(1500):
            x = ((i * 13) % 40) - 20 + ((i % 3) - 1) * 0.3  # stays within +-0.3 of an integer
            y = ((i * 7) % 40) - 20 + ((i % 5) - 2) * 0.1
            t = ((i * 17) % 120) - 60
            reports.append((x, y, t))

        for x, y, t in reports:
            report(table, x, y, t)
            key = (round(x), round(y))  # safe: offsets never reach .5 ties
            if key in reference:
                reference[key][0] = min(reference[key][0], t)
                reference[key][1] = max(reference[key][1], t)
            else:
                reference[key] = [t, t]

        assert size(table) == len(reference)
        for (rx, ry), (mn, mx) in reference.items():
            assert get_min(table, rx, ry) == mn
            assert get_max(table, rx, ry) == mx

    def test_interleaved_reports_and_lookups(self, table):
        report(table, 1, 1, 5)
        assert get_max(table, 1, 1) == 5
        report(table, 2, 2, -5)
        assert get_min(table, 2, 2) == -5
        report(table, 1, 1, 8)
        assert get_max(table, 1, 1) == 8
        assert get_min(table, 1, 1) == 5
        assert size(table) == 2

    def test_independent_tables_do_not_share_state(self):
        a = RecordsMap()
        b = RecordsMap()
        report(a, 1, 1, 10)
        assert size(a) == 1
        assert size(b) == 0
        assert has(b, 1, 1) is False


# ----------------------------------------------------------------------------
# Invalid input (A9: behavior not specified in the description)
# ----------------------------------------------------------------------------
class TestInvalidInput:
    @pytest.mark.parametrize("bad_x, bad_y", [("a", 1), (1, "b"), (None, 1), (1, None)])
    def test_non_numeric_coordinates_rejected(self, table, bad_x, bad_y):  # A9
        with pytest.raises((TypeError, ValueError)):
            report(table, bad_x, bad_y, 10)
        assert size(table) == 0