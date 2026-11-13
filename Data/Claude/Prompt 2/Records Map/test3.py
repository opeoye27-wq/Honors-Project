"""
Unit tests (pytest) for a hash table that stores min/max temperature records
keyed by rounded (x, y) geographic positions.

ASSUMPTIONS (the description does not fix these, so they are explicit and
isolated in the adapter section below; change only that section if your API differs):

A1. Module/class: `from RecordsMap import RecordsMap`,
    constructed with no arguments.
A2. Reporting a temperature: table.add_report((x, y), temperature)
    The position is passed as a single 2-tuple.
A3. Lookup: table[(x, y)] -> (min_temp, max_temp); raises KeyError if absent.
A4. Membership: `(x, y) in table` (i.e. __contains__); never raises, never inserts.
A5. Number of unique positions: len(table).
A6. Current bucket count is exposed as `table.capacity` (an int).
A7. Resizing is triggered by the insertion that pushes size/capacity above 0.7,
    so after every public operation size/capacity <= 0.7. The description says
    only "when its load factor exceeds 0.7", so the exact moment of the check
    (before vs. after inserting) is ambiguous. Tests using this are marked [A7].
A8. Rounding of exact .5 ties (round-half-even vs. round-half-up) is NOT
    specified. Tests therefore avoid ties for equality checks and only assert
    that ties are handled deterministically and consistently.
A9. Non-numeric coordinates or temperatures are expected to raise TypeError or
    ValueError (the description does not say; marked [A9]).
A10. Collision tests patch `RecordsMap._hash(self, key)` to a constant.
     If the implementation has no such method, those tests are skipped; the
     randomized stress test still exercises collisions statistically.
"""

import random

import pytest

from RecordsMap import RecordsMap


# ---------------------------------------------------------------------------
# Adapter layer (the only place that knows the concrete API; see A1-A6)
# ---------------------------------------------------------------------------

def make_table():
    return RecordsMap()


def report(table, x, y, temp):
    table.add_report((x, y), temp)


def lookup(table, x, y):
    return table[(x, y)]


def has(table, x, y):
    return (x, y) in table


def size(table):
    return len(table)


def capacity(table):
    return table.capacity


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def table():
    return make_table()


@pytest.fixture
def colliding_table(monkeypatch):
    """Table whose hash function maps every key to the same value (A10)."""
    if not hasattr(RecordsMap, "_hash"):
        pytest.skip("Implementation exposes no _hash hook; cannot force collisions.")
    monkeypatch.setattr(RecordsMap, "_hash", lambda self, key: 0)
    return make_table()


# ---------------------------------------------------------------------------
# Empty table
# ---------------------------------------------------------------------------

class TestEmptyTable:
    def test_new_table_has_zero_records(self, table):
        assert size(table) == 0

    def test_new_table_contains_nothing(self, table):
        assert not has(table, 0, 0)
        assert not has(table, 10, -10)

    def test_lookup_on_empty_table_raises_key_error(self, table):
        with pytest.raises(KeyError):
            lookup(table, 0, 0)

    def test_initial_capacity_is_positive(self, table):
        assert capacity(table) > 0

    def test_failed_lookup_does_not_create_record(self, table):
        with pytest.raises(KeyError):
            lookup(table, 3, 4)
        assert size(table) == 0
        assert not has(table, 3, 4)

    def test_membership_check_does_not_create_record(self, table):
        has(table, 3, 4)
        assert size(table) == 0


# ---------------------------------------------------------------------------
# First report at a position
# ---------------------------------------------------------------------------

class TestNewRecord:
    def test_first_report_sets_min_and_max_to_reported_value(self, table):
        report(table, 1, 2, 20.5)
        assert lookup(table, 1, 2) == (20.5, 20.5)

    def test_first_report_increments_size(self, table):
        report(table, 1, 2, 20)
        assert size(table) == 1

    def test_first_report_makes_position_present(self, table):
        report(table, 1, 2, 20)
        assert has(table, 1, 2)

    def test_other_positions_remain_absent(self, table):
        report(table, 1, 2, 20)
        assert not has(table, 2, 1)
        assert not has(table, 1, 3)
        assert not has(table, 0, 2)

    def test_lookup_of_missing_position_raises_key_error_when_others_exist(self, table):
        report(table, 1, 2, 20)
        with pytest.raises(KeyError):
            lookup(table, 5, 5)

    def test_swapped_coordinates_are_distinct_positions(self, table):
        report(table, 1, 2, 10)
        report(table, 2, 1, 30)
        assert size(table) == 2
        assert lookup(table, 1, 2) == (10, 10)
        assert lookup(table, 2, 1) == (30, 30)

    def test_positions_differing_in_one_coordinate_are_distinct(self, table):
        report(table, 5, 5, 1)
        report(table, 5, 6, 2)
        report(table, 6, 5, 3)
        assert size(table) == 3
        assert lookup(table, 5, 5) == (1, 1)
        assert lookup(table, 5, 6) == (2, 2)
        assert lookup(table, 6, 5) == (3, 3)


# ---------------------------------------------------------------------------
# Temperature values: negative, zero, floats, extremes
# ---------------------------------------------------------------------------

class TestTemperatureValues:
    def test_zero_temperature(self, table):
        report(table, 0, 0, 0)
        assert lookup(table, 0, 0) == (0, 0)

    def test_negative_temperature(self, table):
        report(table, 0, 0, -15.5)
        assert lookup(table, 0, 0) == (-15.5, -15.5)

    def test_zero_is_not_treated_as_missing_or_falsy_record(self, table):
        report(table, 4, 4, 0)
        assert has(table, 4, 4)
        assert size(table) == 1
        report(table, 4, 4, 5)
        assert lookup(table, 4, 4) == (0, 5)

    def test_negative_to_positive_range(self, table):
        report(table, 1, 1, -10)
        report(table, 1, 1, 10)
        assert lookup(table, 1, 1) == (-10, 10)

    def test_zero_then_negative_updates_min_only(self, table):
        report(table, 1, 1, 0)
        report(table, 1, 1, -3)
        assert lookup(table, 1, 1) == (-3, 0)

    def test_zero_then_positive_updates_max_only(self, table):
        report(table, 1, 1, 0)
        report(table, 1, 1, 3)
        assert lookup(table, 1, 1) == (0, 3)

    def test_all_negative_temperatures(self, table):
        for t in (-5, -20, -1, -12):
            report(table, 2, 2, t)
        assert lookup(table, 2, 2) == (-20, -1)

    def test_very_large_and_very_small_temperatures(self, table):
        report(table, 2, 2, 1e12)
        report(table, 2, 2, -1e12)
        assert lookup(table, 2, 2) == (-1e12, 1e12)

    def test_fractional_temperatures(self, table):
        report(table, 2, 2, 0.1)
        report(table, 2, 2, 0.2)
        assert lookup(table, 2, 2) == (0.1, 0.2)

    def test_mixed_int_and_float_temperatures(self, table):
        report(table, 2, 2, 5)
        report(table, 2, 2, 5.5)
        report(table, 2, 2, 4.5)
        assert lookup(table, 2, 2) == (4.5, 5.5)


# ---------------------------------------------------------------------------
# Repeated reports and min/max updates
# ---------------------------------------------------------------------------

class TestUpdates:
    def test_same_temperature_repeated_keeps_min_equal_max(self, table):
        for _ in range(5):
            report(table, 3, 3, 7)
        assert lookup(table, 3, 3) == (7, 7)

    def test_repeated_reports_do_not_increase_size(self, table):
        for t in (1, 2, 3, 4, 5):
            report(table, 3, 3, t)
        assert size(table) == 1

    def test_higher_temperature_updates_max_only(self, table):
        report(table, 3, 3, 10)
        report(table, 3, 3, 15)
        assert lookup(table, 3, 3) == (10, 15)

    def test_lower_temperature_updates_min_only(self, table):
        report(table, 3, 3, 10)
        report(table, 3, 3, 5)
        assert lookup(table, 3, 3) == (5, 10)

    def test_temperature_between_min_and_max_changes_nothing(self, table):
        report(table, 3, 3, 0)
        report(table, 3, 3, 20)
        report(table, 3, 3, 10)
        assert lookup(table, 3, 3) == (0, 20)

    def test_temperature_equal_to_current_min_or_max_changes_nothing(self, table):
        report(table, 3, 3, 0)
        report(table, 3, 3, 20)
        report(table, 3, 3, 0)
        report(table, 3, 3, 20)
        assert lookup(table, 3, 3) == (0, 20)

    def test_min_and_max_each_updated_over_time(self, table):
        for t in (10, 12, 8, 15, 3, 9):
            report(table, 3, 3, t)
        assert lookup(table, 3, 3) == (3, 15)

    def test_monotonically_increasing_sequence(self, table):
        for t in range(-5, 6):
            report(table, 0, 0, t)
        assert lookup(table, 0, 0) == (-5, 5)

    def test_monotonically_decreasing_sequence(self, table):
        for t in range(5, -6, -1):
            report(table, 0, 0, t)
        assert lookup(table, 0, 0) == (-5, 5)

    def test_updates_at_one_position_do_not_affect_another(self, table):
        report(table, 1, 1, 10)
        report(table, 2, 2, 50)
        report(table, 1, 1, 0)
        report(table, 1, 1, 20)
        assert lookup(table, 1, 1) == (0, 20)
        assert lookup(table, 2, 2) == (50, 50)

    def test_interleaved_reports_across_positions(self, table):
        report(table, 1, 1, 5)
        report(table, 2, 2, 6)
        report(table, 1, 1, 7)
        report(table, 2, 2, 4)
        assert lookup(table, 1, 1) == (5, 7)
        assert lookup(table, 2, 2) == (4, 6)
        assert size(table) == 2

    def test_lookup_is_idempotent_and_does_not_mutate(self, table):
        report(table, 1, 1, 5)
        first = lookup(table, 1, 1)
        second = lookup(table, 1, 1)
        assert first == second == (5, 5)
        assert size(table) == 1


# ---------------------------------------------------------------------------
# Rounding rule (nearest whole number) and position identity
# ---------------------------------------------------------------------------

class TestRounding:
    def test_coordinates_rounding_down_map_to_same_record(self, table):
        report(table, 1.2, 2.4, 10)
        report(table, 1.0, 2.0, 20)
        assert size(table) == 1
        assert lookup(table, 1, 2) == (10, 20)

    def test_coordinates_rounding_up_map_to_same_record(self, table):
        report(table, 1.8, 2.6, 10)
        report(table, 2.0, 3.0, 20)
        assert size(table) == 1
        assert lookup(table, 2, 3) == (10, 20)

    def test_float_and_int_equivalents_match(self, table):
        report(table, 1, 1, 10)
        report(table, 1.0, 1.0, 12)
        assert size(table) == 1
        assert lookup(table, 1, 1) == (10, 12)

    def test_lookup_uses_rounded_coordinates(self, table):
        report(table, 4, 5, 10)
        assert lookup(table, 4.3, 4.7) == (10, 10)
        assert has(table, 3.6, 5.4)

    def test_report_with_rounded_coordinates_visible_via_exact_integers(self, table):
        report(table, 9.4, -3.4, 10)
        assert has(table, 9, -3)
        assert lookup(table, 9, -3) == (10, 10)

    def test_values_just_below_and_above_half_boundary(self, table):
        # 1.49 -> 1, 1.51 -> 2 (neither is a tie)
        report(table, 1.49, 0, 10)
        report(table, 1.51, 0, 20)
        assert size(table) == 2
        assert lookup(table, 1, 0) == (10, 10)
        assert lookup(table, 2, 0) == (20, 20)

    def test_negative_coordinates_round_to_nearest(self, table):
        report(table, -1.4, -2.6, 10)
        report(table, -1.0, -3.0, 20)
        assert size(table) == 1
        assert lookup(table, -1, -3) == (10, 20)

    def test_small_values_of_both_signs_round_to_origin(self, table):
        report(table, 0.4, -0.4, 10)
        report(table, -0.3, 0.2, 5)
        report(table, 0, 0, 20)
        assert size(table) == 1
        assert lookup(table, 0, 0) == (5, 20)

    def test_negative_zero_equals_zero(self, table):
        report(table, -0.0, -0.0, 10)
        report(table, 0, 0, 20)
        assert size(table) == 1
        assert lookup(table, 0, 0) == (10, 20)

    def test_negative_and_positive_one_are_distinct(self, table):
        report(table, -1, -1, 10)
        report(table, 1, 1, 20)
        assert size(table) == 2
        assert lookup(table, -1, -1) == (10, 10)
        assert lookup(table, 1, 1) == (20, 20)

    def test_many_coordinates_resolving_to_one_position(self, table):
        xs = [4.6, 5.0, 5.4, 4.51, 5.49]
        for i, x in enumerate(xs):
            report(table, x, 7.2, i)
        assert size(table) == 1
        assert lookup(table, 5, 7) == (0, 4)

    def test_rounding_applies_to_each_axis_independently(self, table):
        report(table, 1.4, 1.6, 10)  # -> (1, 2)
        assert has(table, 1, 2)
        assert not has(table, 1, 1)
        assert not has(table, 2, 2)

    def test_large_coordinate_values(self, table):
        report(table, 1e9 + 0.3, -1e9 - 0.3, 10)
        assert has(table, 1e9, -1e9)
        assert lookup(table, 1e9, -1e9) == (10, 10)

    def test_tie_values_are_handled_consistently_A8(self, table):
        # Round-half-even and round-half-up disagree, so only assert determinism
        # and that the tie resolves to one of the two neighbouring integers.
        report(table, 0.5, 0.5, 10)
        report(table, 0.5, 0.5, 20)
        assert size(table) == 1
        low, high = has(table, 0, 0), has(table, 1, 1)
        assert low != high  # exactly one of the two neighbours
        pos = (0, 0) if low else (1, 1)
        assert lookup(table, *pos) == (10, 20)

    def test_tie_handling_is_consistent_between_report_and_lookup_A8(self, table):
        report(table, 2.5, 2.5, 10)
        assert has(table, 2.5, 2.5)
        assert lookup(table, 2.5, 2.5) == (10, 10)


# ---------------------------------------------------------------------------
# Special coordinates
# ---------------------------------------------------------------------------

class TestCoordinateRange:
    @pytest.mark.parametrize(
        "x, y",
        [
            (0, 0),
            (-180, -90),
            (180, 90),
            (-180, 90),
            (180, -90),
            (0, 90),
            (-180, 0),
        ],
    )
    def test_geographic_extreme_positions(self, table, x, y):
        report(table, x, y, 12.5)
        assert has(table, x, y)
        assert lookup(table, x, y) == (12.5, 12.5)
        assert size(table) == 1

    def test_distinct_extreme_positions_are_distinct_records(self, table):
        corners = [(-180, -90), (180, 90), (-180, 90), (180, -90), (0, 0)]
        for i, (x, y) in enumerate(corners):
            report(table, x, y, i)
        assert size(table) == len(corners)
        for i, (x, y) in enumerate(corners):
            assert lookup(table, x, y) == (i, i)


# ---------------------------------------------------------------------------
# Hash collisions
# ---------------------------------------------------------------------------

class TestCollisions:
    def test_forced_collisions_keep_records_separate(self, colliding_table):
        t = colliding_table
        report(t, 1, 1, 10)
        report(t, 2, 2, 20)
        report(t, 3, 3, 30)
        assert size(t) == 3
        assert lookup(t, 1, 1) == (10, 10)
        assert lookup(t, 2, 2) == (20, 20)
        assert lookup(t, 3, 3) == (30, 30)

    def test_forced_collisions_update_correct_record(self, colliding_table):
        t = colliding_table
        report(t, 1, 1, 10)
        report(t, 2, 2, 20)
        report(t, 1, 1, 5)
        report(t, 2, 2, 25)
        assert size(t) == 2
        assert lookup(t, 1, 1) == (5, 10)
        assert lookup(t, 2, 2) == (20, 25)

    def test_forced_collisions_missing_key_raises_key_error(self, colliding_table):
        t = colliding_table
        report(t, 1, 1, 10)
        report(t, 2, 2, 20)
        with pytest.raises(KeyError):
            lookup(t, 3, 3)
        assert not has(t, 3, 3)

    def test_forced_collisions_with_rounding(self, colliding_table):
        t = colliding_table
        report(t, 1.2, 1.2, 10)
        report(t, 2.0, 2.0, 20)
        report(t, 0.9, 1.1, 30)  # same record as (1, 1)
        assert size(t) == 2
        assert lookup(t, 1, 1) == (10, 30)
        assert lookup(t, 2, 2) == (20, 20)

    def test_forced_collisions_survive_resizing(self, colliding_table):
        t = colliding_table
        n = 60
        for i in range(n):
            report(t, i, -i, float(i))
        assert size(t) == n
        for i in range(n):
            assert lookup(t, i, -i) == (float(i), float(i))

    def test_forced_collisions_distinct_keys_never_merge(self, colliding_table):
        t = colliding_table
        for i in range(20):
            report(t, i, 0, i)
            report(t, 0, i + 100, -i)
        # (0, 0) is shared between the first iteration of both loops' x/y series
        # only when i == 0 for the first loop; the second loop uses y = i + 100.
        assert size(t) == 40
        assert lookup(t, 7, 0) == (7, 7)
        assert lookup(t, 0, 107) == (-7, -7)


# ---------------------------------------------------------------------------
# Resizing and rehashing
# ---------------------------------------------------------------------------

class TestResizing:
    def test_capacity_unchanged_for_single_record(self, table):
        before = capacity(table)
        report(table, 1, 1, 10)
        assert capacity(table) == before

    def test_capacity_grows_when_many_records_added(self, table):
        before = capacity(table)
        for i in range(max(100, before * 3)):
            report(table, i, i, i)
        assert capacity(table) > before

    def test_capacity_never_decreases(self, table):
        previous = capacity(table)
        for i in range(200):
            report(table, i, 2 * i, i)
            current = capacity(table)
            assert current >= previous
            previous = current

    def test_load_factor_stays_at_or_below_threshold_A7(self, table):
        for i in range(300):
            report(table, i, -i, i)
            assert size(table) / capacity(table) <= 0.7

    def test_repeated_reports_do_not_trigger_growth(self, table):
        report(table, 1, 1, 0)
        before = capacity(table)
        for t in range(1000):
            report(table, 1, 1, t)
        assert capacity(table) == before
        assert size(table) == 1

    def test_all_records_preserved_after_resize(self, table):
        n = 150
        for i in range(n):
            report(table, i, i + 1, float(i) - 50)
        assert size(table) == n
        for i in range(n):
            assert lookup(table, i, i + 1) == (float(i) - 50, float(i) - 50)

    def test_min_max_preserved_across_resize(self, table):
        # Build records with distinct min/max BEFORE any resize.
        keys = [(i, 2 * i) for i in range(3)]
        for i, (x, y) in enumerate(keys):
            report(table, x, y, i * 10)
            report(table, x, y, i * 10 - 5)
            report(table, x, y, i * 10 + 5)
        start_capacity = capacity(table)

        # Force at least one resize with many additional records.
        for j in range(100, 100 + max(150, start_capacity * 3)):
            report(table, j, j, 0)
        assert capacity(table) > start_capacity

        for i, (x, y) in enumerate(keys):
            assert lookup(table, x, y) == (i * 10 - 5, i * 10 + 5)

    def test_updates_after_resize_work(self, table):
        for i in range(120):
            report(table, i, i, 10)
        report(table, 5, 5, -4)
        report(table, 5, 5, 40)
        assert lookup(table, 5, 5) == (-4, 40)
        assert lookup(table, 6, 6) == (10, 10)
        assert size(table) == 120

    def test_new_records_after_resize_are_stored(self, table):
        for i in range(100):
            report(table, i, 0, 1)
        report(table, 1000, 1000, 99)
        assert size(table) == 101
        assert lookup(table, 1000, 1000) == (99, 99)

    def test_rounding_equivalence_survives_resize(self, table):
        report(table, 1.2, 1.2, 10)
        for i in range(2, 150):
            report(table, i, i, 0)
        report(table, 0.9, 1.1, 30)  # rounds to (1, 1)
        assert lookup(table, 1, 1) == (10, 30)
        assert size(table) == 149

    def test_missing_positions_still_missing_after_resize(self, table):
        for i in range(120):
            report(table, i, i, 0)
        assert not has(table, 500, 500)
        with pytest.raises(KeyError):
            lookup(table, 500, 500)
        assert size(table) == 120

    def test_negative_and_zero_temperatures_preserved_across_resize(self, table):
        temps = {}
        for i in range(130):
            t = (i % 7) - 3  # includes negatives and 0
            temps[(i, -i)] = t
            report(table, i, -i, t)
        for (x, y), t in temps.items():
            assert lookup(table, x, y) == (t, t)
        assert size(table) == 130

    def test_size_counts_unique_positions_not_reports_across_resize(self, table):
        for rep in range(3):
            for i in range(80):
                report(table, i, i, rep)
        assert size(table) == 80
        for i in range(80):
            assert lookup(table, i, i) == (0, 2)


# ---------------------------------------------------------------------------
# Randomized consistency check against a reference dictionary
# ---------------------------------------------------------------------------

class TestRandomizedAgainstReference:
    @pytest.mark.parametrize("seed", [0, 1, 2, 3, 42])
    def test_matches_reference_model(self, seed):
        rng = random.Random(seed)
        table = make_table()
        reference = {}

        for _ in range(1500):
            # Offsets in (-0.4, 0.4) avoid .5 ties, so rounding is unambiguous.
            bx, by = rng.randint(-15, 15), rng.randint(-15, 15)
            x = bx + rng.uniform(-0.4, 0.4)
            y = by + rng.uniform(-0.4, 0.4)
            temp = rng.randint(-50, 50)

            report(table, x, y, temp)
            lo, hi = reference.get((bx, by), (temp, temp))
            reference[(bx, by)] = (min(lo, temp), max(hi, temp))

        assert size(table) == len(reference)
        for (bx, by), (lo, hi) in reference.items():
            assert has(table, bx, by)
            assert lookup(table, bx, by) == (lo, hi)

        # Absent positions are still absent.
        assert not has(table, 1000, 1000)
        with pytest.raises(KeyError):
            lookup(table, 1000, 1000)

    def test_many_distinct_positions_all_retrievable(self):
        table = make_table()
        expected = {}
        for x in range(-20, 21):
            for y in range(-20, 21):
                temp = x * 3 - y
                report(table, x, y, temp)
                expected[(x, y)] = temp
        assert size(table) == len(expected)
        for (x, y), temp in expected.items():
            assert lookup(table, x, y) == (temp, temp)


# ---------------------------------------------------------------------------
# Missing positions / KeyError
# ---------------------------------------------------------------------------

class TestMissingPositions:
    def test_key_error_for_never_reported_position(self, table):
        report(table, 1, 1, 10)
        with pytest.raises(KeyError):
            lookup(table, 2, 2)

    def test_key_error_for_position_that_rounds_to_different_cell(self, table):
        report(table, 1, 1, 10)
        with pytest.raises(KeyError):
            lookup(table, 1.6, 1)  # rounds to (2, 1)

    def test_has_returns_false_not_error_for_missing(self, table):
        report(table, 1, 1, 10)
        assert has(table, 9, 9) is False

    def test_lookup_after_failed_lookup_still_works(self, table):
        report(table, 1, 1, 10)
        with pytest.raises(KeyError):
            lookup(table, 8, 8)
        assert lookup(table, 1, 1) == (10, 10)
        assert size(table) == 1


# ---------------------------------------------------------------------------
# Invalid input [A9]
# ---------------------------------------------------------------------------

class TestInvalidInput:
    @pytest.mark.parametrize("bad_x, bad_y", [("a", 1), (1, "b"), (None, 1), (1, None)])
    def test_non_numeric_coordinates_rejected_on_report_A9(self, table, bad_x, bad_y):
        with pytest.raises((TypeError, ValueError)):
            report(table, bad_x, bad_y, 10)
        assert size(table) == 0

    @pytest.mark.parametrize("bad_temp", ["hot", None, [10], {"t": 1}])
    def test_non_numeric_temperature_rejected_A9(self, table, bad_temp):
        with pytest.raises((TypeError, ValueError)):
            report(table, 1, 1, bad_temp)
        assert size(table) == 0

    def test_invalid_temperature_does_not_corrupt_existing_record_A9(self, table):
        report(table, 1, 1, 10)
        with pytest.raises((TypeError, ValueError)):
            report(table, 1, 1, "hot")
        assert lookup(table, 1, 1) == (10, 10)
        assert size(table) == 1