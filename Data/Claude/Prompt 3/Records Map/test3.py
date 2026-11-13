"""
Unit tests (pytest) for a hash table that stores min/max temperature records
keyed by geographic position (latitude, longitude).

The description does not specify the API, so the assumptions below are made
explicit. If your program differs, change only the ADAPTER section.

ASSUMPTIONS
-----------
A1. Module is `temperature_table`, class is `TemperatureHashTable`,
    constructed with no arguments.
A2. insert(lat, lon, min_temp, max_temp) adds a record. Inserting an existing
    position OVERWRITES the old record (it does not merge or raise).
A3. get(lat, lon) returns a (min_temp, max_temp) tuple, or None if absent.
A4. remove(lat, lon) returns True if a record was removed, False if absent.
A5. `(lat, lon) in table` and len(table) are supported.
A6. Valid latitude is [-90, 90]; valid longitude is [-180, 180] (inclusive).
    Out-of-range values raise ValueError.
A7. min_temp > max_temp raises ValueError; min_temp == max_temp is allowed.
A8. Non-numeric (str, None, list) coordinates or temperatures raise TypeError.
    NaN and +/-infinity raise ValueError.
A9. Temperatures are in any unit (no physical lower or upper bound is enforced).
A10. Keys are exact-match on the float values (no rounding or tolerance).
A11. Positions (lat, lon) and (lon, lat) are different keys.
"""

import math

import pytest

# ----------------------------- ADAPTER --------------------------------------
from RecordsMap import RecordsMap  # noqa: E402  (A1)


def make_table():
    return RecordsMap()


def insert(t, lat, lon, tmin, tmax):
    t.add_report((lat, lon), tmin)
    return t.add_report((lat, lon), tmax)


def get(t, lat, lon):
    try:
        return t[(lat, lon)]
    except KeyError:
        return None


def remove(t, lat, lon):
    return t.remove(lat, lon)
# ----------------------------------------------------------------------------


@pytest.fixture
def table():
    return make_table()


# ------------------------------ Normal cases --------------------------------

class TestNormalOperation:
    def test_new_table_is_empty(self, table):
        assert len(table) == 0

    def test_insert_and_get_single_record(self, table):
        insert(table, 41.8077, -72.2540, -5.0, 12.5)
        assert get(table, 41.8077, -72.2540) == (-5.0, 12.5)
        assert len(table) == 1

    def test_insert_multiple_distinct_positions(self, table):
        insert(table, 10.0, 20.0, 1.0, 2.0)
        insert(table, 30.0, 40.0, 3.0, 4.0)
        insert(table, 50.0, 60.0, 5.0, 6.0)
        assert len(table) == 3
        assert get(table, 10.0, 20.0) == (1.0, 2.0)
        assert get(table, 30.0, 40.0) == (3.0, 4.0)
        assert get(table, 50.0, 60.0) == (5.0, 6.0)

    def test_contains_true_for_present_position(self, table):
        insert(table, 1.0, 2.0, 0.0, 10.0)
        assert (1.0, 2.0) in table

    def test_contains_false_for_absent_position(self, table):
        insert(table, 1.0, 2.0, 0.0, 10.0)
        assert (2.0, 1.0) not in table

    def test_get_missing_returns_none(self, table):
        assert get(table, 5.0, 5.0) is None

    def test_get_does_not_modify_table(self, table):
        insert(table, 5.0, 5.0, 0.0, 1.0)
        get(table, 5.0, 5.0)
        get(table, 9.0, 9.0)
        assert len(table) == 1

    def test_integer_coordinates_and_temperatures_accepted(self, table):
        insert(table, 10, 20, -3, 7)
        assert get(table, 10, 20) == (-3, 7)

    def test_int_and_float_equivalent_keys_match(self, table):
        # A10: 10 and 10.0 are equal and should hash identically
        insert(table, 10, 20, 0, 1)
        assert get(table, 10.0, 20.0) == (0, 1)


# ----------------------------- Update semantics -----------------------------

class TestOverwrite:
    def test_insert_same_position_overwrites_values(self, table):  # A2
        insert(table, 10.0, 20.0, 0.0, 5.0)
        insert(table, 10.0, 20.0, -2.0, 9.0)
        assert get(table, 10.0, 20.0) == (-2.0, 9.0)

    def test_overwrite_does_not_increase_size(self, table):  # A2
        insert(table, 10.0, 20.0, 0.0, 5.0)
        insert(table, 10.0, 20.0, 1.0, 6.0)
        assert len(table) == 1

    def test_overwrite_does_not_affect_other_records(self, table):
        insert(table, 1.0, 1.0, 0.0, 1.0)
        insert(table, 2.0, 2.0, 0.0, 2.0)
        insert(table, 1.0, 1.0, 5.0, 6.0)
        assert get(table, 2.0, 2.0) == (0.0, 2.0)


# --------------------------------- Removal ----------------------------------

class TestRemove:
    def test_remove_existing_returns_true(self, table):  # A4
        insert(table, 1.0, 2.0, 0.0, 1.0)
        assert remove(table, 1.0, 2.0) is True

    def test_remove_deletes_record(self, table):
        insert(table, 1.0, 2.0, 0.0, 1.0)
        remove(table, 1.0, 2.0)
        assert get(table, 1.0, 2.0) is None
        assert len(table) == 0

    def test_remove_missing_returns_false(self, table):  # A4
        assert remove(table, 1.0, 2.0) is False

    def test_remove_twice_second_returns_false(self, table):
        insert(table, 1.0, 2.0, 0.0, 1.0)
        assert remove(table, 1.0, 2.0) is True
        assert remove(table, 1.0, 2.0) is False

    def test_remove_leaves_other_records_intact(self, table):
        insert(table, 1.0, 1.0, 0.0, 1.0)
        insert(table, 2.0, 2.0, 0.0, 2.0)
        remove(table, 1.0, 1.0)
        assert get(table, 2.0, 2.0) == (0.0, 2.0)
        assert len(table) == 1

    def test_reinsert_after_remove(self, table):
        insert(table, 1.0, 2.0, 0.0, 1.0)
        remove(table, 1.0, 2.0)
        insert(table, 1.0, 2.0, 3.0, 4.0)
        assert get(table, 1.0, 2.0) == (3.0, 4.0)
        assert len(table) == 1

    def test_remove_from_empty_table(self, table):
        assert remove(table, 0.0, 0.0) is False
        assert len(table) == 0


# --------------------------- Boundary coordinates ---------------------------

class TestCoordinateBoundaries:
    @pytest.mark.parametrize("lat", [-90.0, 90.0, 0.0])
    def test_latitude_boundaries_accepted(self, table, lat):  # A6
        insert(table, lat, 0.0, 0.0, 1.0)
        assert get(table, lat, 0.0) == (0.0, 1.0)

    @pytest.mark.parametrize("lon", [-180.0, 180.0, 0.0])
    def test_longitude_boundaries_accepted(self, table, lon):  # A6
        insert(table, 0.0, lon, 0.0, 1.0)
        assert get(table, 0.0, lon) == (0.0, 1.0)

    def test_all_four_corners(self, table):
        corners = [(-90.0, -180.0), (-90.0, 180.0), (90.0, -180.0), (90.0, 180.0)]
        for i, (la, lo) in enumerate(corners):
            insert(table, la, lo, float(i), float(i + 1))
        assert len(table) == 4
        for i, (la, lo) in enumerate(corners):
            assert get(table, la, lo) == (float(i), float(i + 1))

    @pytest.mark.parametrize("lat", [90.0001, -90.0001, 91, -91, 1000, -1000])
    def test_latitude_out_of_range_rejected(self, table, lat):  # A6
        with pytest.raises(ValueError):
            insert(table, lat, 0.0, 0.0, 1.0)
        assert len(table) == 0

    @pytest.mark.parametrize("lon", [180.0001, -180.0001, 181, -181, 1000, -1000])
    def test_longitude_out_of_range_rejected(self, table, lon):  # A6
        with pytest.raises(ValueError):
            insert(table, 0.0, lon, 0.0, 1.0)
        assert len(table) == 0

    def test_negative_zero_equals_positive_zero(self, table):  # A10
        insert(table, 0.0, 0.0, 0.0, 1.0)
        assert get(table, -0.0, -0.0) == (0.0, 1.0)

    def test_very_close_coordinates_are_distinct_keys(self, table):  # A10
        insert(table, 10.0, 20.0, 0.0, 1.0)
        insert(table, 10.000001, 20.0, 5.0, 6.0)
        assert len(table) == 2
        assert get(table, 10.0, 20.0) == (0.0, 1.0)
        assert get(table, 10.000001, 20.0) == (5.0, 6.0)

    def test_swapped_lat_lon_are_distinct_keys(self, table):  # A11
        insert(table, 10.0, 20.0, 0.0, 1.0)
        insert(table, 20.0, 10.0, 5.0, 6.0)
        assert len(table) == 2
        assert get(table, 10.0, 20.0) == (0.0, 1.0)
        assert get(table, 20.0, 10.0) == (5.0, 6.0)

    def test_sign_flipped_positions_are_distinct(self, table):
        insert(table, 10.0, 20.0, 0.0, 1.0)
        insert(table, -10.0, -20.0, 2.0, 3.0)
        insert(table, 10.0, -20.0, 4.0, 5.0)
        insert(table, -10.0, 20.0, 6.0, 7.0)
        assert len(table) == 4
        assert get(table, -10.0, 20.0) == (6.0, 7.0)

    def test_poles_at_different_longitudes(self, table):
        # Physically the same point, but A10 says keys are matched exactly.
        insert(table, 90.0, 0.0, -50.0, -40.0)
        insert(table, 90.0, 120.0, -55.0, -45.0)
        assert len(table) == 2

    def test_antimeridian_both_sides_distinct(self, table):
        # Physically the same meridian, but A10 says keys are matched exactly.
        insert(table, 0.0, 180.0, 20.0, 30.0)
        insert(table, 0.0, -180.0, 21.0, 31.0)
        assert len(table) == 2


# ---------------------------- Temperature values ----------------------------

class TestTemperatureValues:
    def test_min_equals_max_allowed(self, table):  # A7
        insert(table, 1.0, 1.0, 15.0, 15.0)
        assert get(table, 1.0, 1.0) == (15.0, 15.0)

    def test_min_greater_than_max_rejected(self, table):  # A7
        with pytest.raises(ValueError):
            insert(table, 1.0, 1.0, 20.0, 10.0)
        assert len(table) == 0

    def test_min_slightly_greater_than_max_rejected(self, table):  # A7
        with pytest.raises(ValueError):
            insert(table, 1.0, 1.0, 10.0000001, 10.0)

    def test_failed_insert_does_not_overwrite_existing(self, table):
        insert(table, 1.0, 1.0, 0.0, 5.0)
        with pytest.raises(ValueError):
            insert(table, 1.0, 1.0, 9.0, 1.0)
        assert get(table, 1.0, 1.0) == (0.0, 5.0)

    def test_both_negative_temperatures(self, table):
        insert(table, 1.0, 1.0, -60.0, -20.0)
        assert get(table, 1.0, 1.0) == (-60.0, -20.0)

    def test_both_positive_temperatures(self, table):
        insert(table, 1.0, 1.0, 30.0, 55.0)
        assert get(table, 1.0, 1.0) == (30.0, 55.0)

    def test_zero_temperatures(self, table):
        insert(table, 1.0, 1.0, 0.0, 0.0)
        assert get(table, 1.0, 1.0) == (0.0, 0.0)

    def test_extreme_temperatures_accepted(self, table):  # A9
        insert(table, 1.0, 1.0, -273.15, 1e6)
        assert get(table, 1.0, 1.0) == (-273.15, 1e6)

    def test_float_precision_preserved(self, table):
        insert(table, 1.0, 1.0, -0.1, 0.30000000000000004)
        lo, hi = get(table, 1.0, 1.0)
        assert lo == -0.1
        assert hi == 0.30000000000000004

    def test_returned_values_unchanged_across_repeated_gets(self, table):
        insert(table, 1.0, 1.0, -4.5, 8.25)
        assert get(table, 1.0, 1.0) == get(table, 1.0, 1.0) == (-4.5, 8.25)


# ------------------------------ Invalid inputs ------------------------------

class TestInvalidInputs:
    @pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
    def test_non_finite_latitude_rejected(self, table, bad):  # A8
        with pytest.raises(ValueError):
            insert(table, bad, 0.0, 0.0, 1.0)

    @pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
    def test_non_finite_longitude_rejected(self, table, bad):  # A8
        with pytest.raises(ValueError):
            insert(table, 0.0, bad, 0.0, 1.0)

    @pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
    def test_non_finite_min_temp_rejected(self, table, bad):  # A8
        with pytest.raises(ValueError):
            insert(table, 0.0, 0.0, bad, 10.0)

    @pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
    def test_non_finite_max_temp_rejected(self, table, bad):  # A8
        with pytest.raises(ValueError):
            insert(table, 0.0, 0.0, 0.0, bad)

    @pytest.mark.parametrize("bad", ["10.0", None, [10.0], (10.0,), {}, object()])
    def test_non_numeric_latitude_rejected(self, table, bad):  # A8
        with pytest.raises(TypeError):
            insert(table, bad, 0.0, 0.0, 1.0)

    @pytest.mark.parametrize("bad", ["10.0", None, [10.0], (10.0,), {}, object()])
    def test_non_numeric_longitude_rejected(self, table, bad):  # A8
        with pytest.raises(TypeError):
            insert(table, 0.0, bad, 0.0, 1.0)

    @pytest.mark.parametrize("bad", ["5", None, [5], object()])
    def test_non_numeric_min_temp_rejected(self, table, bad):  # A8
        with pytest.raises(TypeError):
            insert(table, 0.0, 0.0, bad, 10.0)

    @pytest.mark.parametrize("bad", ["5", None, [5], object()])
    def test_non_numeric_max_temp_rejected(self, table, bad):  # A8
        with pytest.raises(TypeError):
            insert(table, 0.0, 0.0, 0.0, bad)

    def test_get_with_non_numeric_key_rejected_or_missing(self, table):
        # Ambiguous: get() with invalid key may raise TypeError (A8) or return None.
        try:
            result = get(table, "a", "b")
        except TypeError:
            return
        assert result is None

    def test_get_with_out_of_range_key_rejected_or_missing(self, table):
        # Ambiguous: get() with out-of-range key may raise ValueError (A6) or return None.
        try:
            result = get(table, 999.0, 999.0)
        except ValueError:
            return
        assert result is None

    def test_remove_with_non_numeric_key_rejected_or_false(self, table):
        # Ambiguous: remove() with invalid key may raise TypeError (A8) or return False.
        try:
            result = remove(table, None, None)
        except TypeError:
            return
        assert result is False

    def test_contains_with_malformed_key_does_not_crash_unexpectedly(self, table):
        # Ambiguous: `in` with a non-pair may be False or raise TypeError/ValueError.
        try:
            result = "not a position" in table
        except (TypeError, ValueError):
            return
        assert result is False

    def test_missing_arguments_raise_type_error(self, table):
        with pytest.raises(TypeError):
            table.add_report((1.0, 2.0))  # missing max_temp

    def test_failed_insert_leaves_table_unchanged(self, table):
        insert(table, 1.0, 1.0, 0.0, 1.0)
        with pytest.raises((ValueError, TypeError)):
            insert(table, 500.0, 1.0, 0.0, 1.0)
        assert len(table) == 1
        assert get(table, 1.0, 1.0) == (0.0, 1.0)


# ------------------------- Collisions, scale, resizing ----------------------

class TestCollisionsAndScale:
    def test_many_inserts_all_retrievable(self, table):
        n = 2000  # large enough to force any resizing / rehashing
        for i in range(n):
            lat = -90.0 + (i % 181)
            lon = -180.0 + (i // 181) * 0.5
            insert(table, lat, lon, float(i), float(i) + 1.0)
        assert len(table) == n
        for i in range(n):
            lat = -90.0 + (i % 181)
            lon = -180.0 + (i // 181) * 0.5
            assert get(table, lat, lon) == (float(i), float(i) + 1.0)

    def test_grid_of_integer_positions(self, table):
        count = 0
        for lat in range(-90, 91, 5):
            for lon in range(-180, 181, 5):
                insert(table, float(lat), float(lon), float(lat), float(lat) + abs(lon))
                count += 1
        assert len(table) == count
        assert get(table, 45.0, -90.0) == (45.0, 135.0)

    def test_colliding_style_keys_remain_separate(self, table):
        # Keys whose coordinate sums/products coincide, which naive hashes could collide on.
        pairs = [(10.0, 20.0), (20.0, 10.0), (15.0, 15.0), (0.0, 30.0), (30.0, 0.0),
                 (-10.0, 40.0), (40.0, -10.0)]
        for i, (la, lo) in enumerate(pairs):
            insert(table, la, lo, float(i), float(i) + 0.5)
        assert len(table) == len(pairs)
        for i, (la, lo) in enumerate(pairs):
            assert get(table, la, lo) == (float(i), float(i) + 0.5)

    def test_remove_in_collision_chain_does_not_lose_neighbours(self, table):
        pairs = [(float(i), float(-i)) for i in range(0, 60)]
        for i, (la, lo) in enumerate(pairs):
            insert(table, la, lo, float(i), float(i) + 1)
        for la, lo in pairs[::2]:
            assert remove(table, la, lo) is True
        for i, (la, lo) in enumerate(pairs):
            expected = None if i % 2 == 0 else (float(i), float(i) + 1)
            assert get(table, la, lo) == expected
        assert len(table) == len(pairs) // 2

    def test_insert_remove_cycle_many_times(self, table):
        for round_ in range(200):
            insert(table, 12.5, 34.5, float(round_), float(round_) + 1)
            assert get(table, 12.5, 34.5) == (float(round_), float(round_) + 1)
            assert remove(table, 12.5, 34.5) is True
        assert len(table) == 0

    def test_fill_then_empty_table(self, table):
        keys = [(float(i % 90), float(i % 180)) for i in range(500)]
        unique = set(keys)
        for k in unique:
            insert(table, k[0], k[1], 0.0, 1.0)
        assert len(table) == len(unique)
        for k in unique:
            assert remove(table, k[0], k[1]) is True
        assert len(table) == 0
        for k in unique:
            assert get(table, k[0], k[1]) is None

    def test_reuse_after_emptying(self, table):
        for i in range(100):
            insert(table, float(i % 90), float(i), 0.0, 1.0)
        for i in range(100):
            remove(table, float(i % 90), float(i))
        insert(table, 5.0, 5.0, 2.0, 3.0)
        assert len(table) == 1
        assert get(table, 5.0, 5.0) == (2.0, 3.0)


# ------------------------------ Isolation / state ---------------------------

class TestStateIsolation:
    def test_separate_tables_are_independent(self):
        a, b = make_table(), make_table()
        insert(a, 1.0, 1.0, 0.0, 1.0)
        assert get(b, 1.0, 1.0) is None
        assert len(b) == 0

    def test_len_tracks_inserts_and_removes(self, table):
        insert(table, 1.0, 1.0, 0.0, 1.0)
        insert(table, 2.0, 2.0, 0.0, 1.0)
        assert len(table) == 2
        remove(table, 1.0, 1.0)
        assert len(table) == 1
        remove(table, 99.0, 99.0)  # absent but in range (A6)
        assert len(table) == 1

    def test_returned_record_is_not_a_live_view(self, table):
        insert(table, 1.0, 1.0, 0.0, 1.0)
        rec = get(table, 1.0, 1.0)
        try:
            rec = list(rec)
            rec[0] = 999.0
        except TypeError:
            pass
        assert get(table, 1.0, 1.0) == (0.0, 1.0)

    def test_bool_coordinates_behaviour_is_consistent(self, table):
        # Ambiguous: bool is an int subclass in Python. True == 1 and hash(True) == hash(1).
        # We only assert consistency: if accepted, lookups by 1 and True must agree.
        try:
            insert(table, True, False, 0.0, 1.0)
        except (TypeError, ValueError):
            return
        assert get(table, 1, 0) == get(table, True, False)