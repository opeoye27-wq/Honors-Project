"""
Unit tests for a hash table storing min/max temperature records by geographic position.

ASSUMPTIONS (no source or API was provided, so each of these is explicit and can be
changed in the CONFIG section below):

 A1. The module is `temperature_table` and the class is `TemperatureHashTable`,
     constructed with no arguments.
 A2. A position is a (latitude, longitude) pair of numbers. Latitude must be in
     [-90, 90] and longitude in [-180, 180] (inclusive).
 A3. A record is (min_temp, max_temp). The table stores it, and `get` returns it as
     something equal to the tuple (min_temp, max_temp).
 A4. Methods: insert(lat, lon, min_temp, max_temp), get(lat, lon), remove(lat, lon),
     `(lat, lon) in table` is NOT assumed. Use contains(lat, lon), and len(table).
 A5. Inserting at an existing position overwrites the old record (no duplicate keys,
     size unchanged).
 A6. get() on a missing position returns None.
 A7. remove() on a missing position returns False. A successful remove returns True.
 A8. min_temp > max_temp raises ValueError. Out-of-range or NaN/inf coordinates
     raise ValueError. NaN temperatures raise ValueError. Non-numeric arguments
     raise TypeError.
 A9. min_temp == max_temp is valid.
 A10. Positions are exact-match keys: no rounding or tolerance. 1 and 1.0 are the
      same key, and 0.0 and -0.0 are the same key (they compare equal in Python).
 A11. No physical-plausibility check on temperatures (for example, below absolute
      zero) is assumed, since the description does not mention one.
 A12. The table grows as needed. No capacity limit exists, so thousands of records
      must all be retrievable.

If your implementation differs, change the CONFIG section only.
"""

import math

import pytest

from RecordsMap import RecordsMap

# ----------------------------------------------------------------------------
# CONFIG: adapt here if your API names/behaviors differ from the assumptions
# ----------------------------------------------------------------------------
INSERT = "add_report"
GET = "__getitem__"
REMOVE = "remove"
CONTAINS = "__contains__"
MISSING = None                  # A6: what get() returns for a missing position
RANGE_ERROR = ValueError        # A8
TYPE_ERROR = TypeError          # A8


def put(t, lat, lon, tmin, tmax):
    getattr(t, INSERT)((lat, lon), tmin)
    return getattr(t, INSERT)((lat, lon), tmax)


def fetch(t, lat, lon):
    try:
        return getattr(t, GET)((lat, lon))
    except KeyError:
        return MISSING


def delete(t, lat, lon):
    return getattr(t, REMOVE)(lat, lon)


def has(t, lat, lon):
    return getattr(t, CONTAINS)((lat, lon))


def rec(t, lat, lon):
    """Fetch a record and normalize to a tuple (or MISSING)."""
    r = fetch(t, lat, lon)
    return r if r is MISSING else tuple(r)


@pytest.fixture
def table():
    return RecordsMap()


# ----------------------------------------------------------------------------
# Empty table
# ----------------------------------------------------------------------------
class TestEmptyTable:
    def test_new_table_has_length_zero(self, table):
        assert len(table) == 0

    def test_get_on_empty_table_returns_missing(self, table):
        assert fetch(table, 10.0, 20.0) is MISSING

    def test_contains_on_empty_table_is_false(self, table):
        assert has(table, 10.0, 20.0) is False

    def test_remove_on_empty_table_returns_false(self, table):  # A7
        assert delete(table, 10.0, 20.0) is False
        assert len(table) == 0


# ----------------------------------------------------------------------------
# Normal usage
# ----------------------------------------------------------------------------
class TestBasicOperations:
    def test_insert_then_get(self, table):
        put(table, 41.8, -72.2, -5.0, 12.5)
        assert rec(table, 41.8, -72.2) == (-5.0, 12.5)

    def test_insert_increases_length(self, table):
        put(table, 1.0, 2.0, 0.0, 10.0)
        assert len(table) == 1
        put(table, 3.0, 4.0, 1.0, 11.0)
        assert len(table) == 2

    def test_contains_after_insert(self, table):
        put(table, 1.0, 2.0, 0.0, 10.0)
        assert has(table, 1.0, 2.0) is True
        assert has(table, 2.0, 1.0) is False

    def test_multiple_positions_are_independent(self, table):
        put(table, 10.0, 10.0, 1.0, 2.0)
        put(table, 20.0, 20.0, 3.0, 4.0)
        put(table, 30.0, 30.0, 5.0, 6.0)
        assert rec(table, 10.0, 10.0) == (1.0, 2.0)
        assert rec(table, 20.0, 20.0) == (3.0, 4.0)
        assert rec(table, 30.0, 30.0) == (5.0, 6.0)

    def test_get_missing_position_returns_missing(self, table):
        put(table, 10.0, 10.0, 1.0, 2.0)
        assert fetch(table, 11.0, 10.0) is MISSING

    def test_get_does_not_modify_table(self, table):
        put(table, 10.0, 10.0, 1.0, 2.0)
        fetch(table, 10.0, 10.0)
        fetch(table, 99.0, 99.0)
        assert len(table) == 1
        assert rec(table, 10.0, 10.0) == (1.0, 2.0)

    def test_integer_temperatures_and_coordinates(self, table):
        put(table, 45, 90, -10, 30)
        assert rec(table, 45, 90) == (-10, 30)

    def test_two_instances_do_not_share_state(self):
        a, b = RecordsMap(), RecordsMap()
        put(a, 1.0, 1.0, 0.0, 1.0)
        assert len(b) == 0
        assert fetch(b, 1.0, 1.0) is MISSING


# ----------------------------------------------------------------------------
# Overwrite semantics (A5)
# ----------------------------------------------------------------------------
class TestOverwrite:
    def test_insert_same_position_replaces_record(self, table):
        put(table, 5.0, 5.0, 0.0, 10.0)
        put(table, 5.0, 5.0, -3.0, 20.0)
        assert rec(table, 5.0, 5.0) == (-3.0, 20.0)

    def test_overwrite_does_not_change_length(self, table):
        put(table, 5.0, 5.0, 0.0, 10.0)
        put(table, 5.0, 5.0, 1.0, 11.0)
        assert len(table) == 1

    def test_overwrite_does_not_affect_other_records(self, table):
        put(table, 5.0, 5.0, 0.0, 10.0)
        put(table, 6.0, 6.0, 2.0, 12.0)
        put(table, 5.0, 5.0, 1.0, 11.0)
        assert rec(table, 6.0, 6.0) == (2.0, 12.0)

    def test_repeated_overwrites_keep_last_value(self, table):
        for i in range(100):
            put(table, 5.0, 5.0, float(i), float(i + 1))
        assert rec(table, 5.0, 5.0) == (99.0, 100.0)
        assert len(table) == 1


# ----------------------------------------------------------------------------
# Removal
# ----------------------------------------------------------------------------
class TestRemove:
    def test_remove_existing_returns_true(self, table):
        put(table, 1.0, 1.0, 0.0, 5.0)
        assert delete(table, 1.0, 1.0) is True

    def test_removed_record_is_gone(self, table):
        put(table, 1.0, 1.0, 0.0, 5.0)
        delete(table, 1.0, 1.0)
        assert fetch(table, 1.0, 1.0) is MISSING
        assert has(table, 1.0, 1.0) is False
        assert len(table) == 0

    def test_remove_missing_returns_false_and_keeps_others(self, table):
        put(table, 1.0, 1.0, 0.0, 5.0)
        assert delete(table, 2.0, 2.0) is False
        assert len(table) == 1
        assert rec(table, 1.0, 1.0) == (0.0, 5.0)

    def test_double_remove(self, table):
        put(table, 1.0, 1.0, 0.0, 5.0)
        assert delete(table, 1.0, 1.0) is True
        assert delete(table, 1.0, 1.0) is False
        assert len(table) == 0

    def test_reinsert_after_remove(self, table):
        put(table, 1.0, 1.0, 0.0, 5.0)
        delete(table, 1.0, 1.0)
        put(table, 1.0, 1.0, -1.0, 6.0)
        assert rec(table, 1.0, 1.0) == (-1.0, 6.0)
        assert len(table) == 1

    def test_remove_one_leaves_others_intact(self, table):
        for i in range(10):
            put(table, float(i), float(i), float(i), float(i + 1))
        delete(table, 5.0, 5.0)
        for i in range(10):
            if i == 5:
                assert fetch(table, 5.0, 5.0) is MISSING
            else:
                assert rec(table, float(i), float(i)) == (float(i), float(i + 1))
        assert len(table) == 9


# ----------------------------------------------------------------------------
# Key identity: latitude/longitude handling (A10)
# ----------------------------------------------------------------------------
class TestKeyIdentity:
    def test_swapped_lat_lon_are_different_keys(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        put(table, 20.0, 10.0, 3.0, 4.0)
        assert rec(table, 10.0, 20.0) == (1.0, 2.0)
        assert rec(table, 20.0, 10.0) == (3.0, 4.0)
        assert len(table) == 2

    def test_same_lat_different_lon(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        put(table, 10.0, 21.0, 3.0, 4.0)
        assert rec(table, 10.0, 20.0) == (1.0, 2.0)
        assert rec(table, 10.0, 21.0) == (3.0, 4.0)

    def test_same_lon_different_lat(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        put(table, 11.0, 20.0, 3.0, 4.0)
        assert rec(table, 10.0, 20.0) == (1.0, 2.0)
        assert rec(table, 11.0, 20.0) == (3.0, 4.0)

    def test_int_and_float_equivalent_coordinates_are_same_key(self, table):
        put(table, 1, 2, 0.0, 1.0)
        put(table, 1.0, 2.0, 5.0, 6.0)
        assert len(table) == 1
        assert rec(table, 1, 2) == (5.0, 6.0)

    def test_negative_zero_equals_zero(self, table):
        put(table, 0.0, 0.0, 1.0, 2.0)
        assert rec(table, -0.0, -0.0) == (1.0, 2.0)
        put(table, -0.0, 0.0, 3.0, 4.0)
        assert len(table) == 1

    def test_very_close_coordinates_are_distinct(self, table):
        put(table, 10.0, 10.0, 1.0, 2.0)
        put(table, 10.0 + 1e-9, 10.0, 3.0, 4.0)
        assert len(table) == 2
        assert rec(table, 10.0, 10.0) == (1.0, 2.0)
        assert rec(table, 10.0 + 1e-9, 10.0) == (3.0, 4.0)

    def test_negative_and_positive_coordinates_are_distinct(self, table):
        put(table, 10.0, 10.0, 1.0, 2.0)
        put(table, -10.0, 10.0, 3.0, 4.0)
        put(table, 10.0, -10.0, 5.0, 6.0)
        put(table, -10.0, -10.0, 7.0, 8.0)
        assert len(table) == 4
        assert rec(table, -10.0, -10.0) == (7.0, 8.0)


# ----------------------------------------------------------------------------
# Boundary values
# ----------------------------------------------------------------------------
class TestBoundaries:
    @pytest.mark.parametrize(
        "lat, lon",
        [
            (90.0, 180.0),
            (90.0, -180.0),
            (-90.0, 180.0),
            (-90.0, -180.0),
            (0.0, 0.0),
            (90, 0),
            (-90, 0),
            (0, 180),
            (0, -180),
        ],
    )
    def test_extreme_valid_coordinates_are_accepted(self, table, lat, lon):
        put(table, lat, lon, -1.0, 1.0)
        assert rec(table, lat, lon) == (-1.0, 1.0)

    def test_min_equals_max_is_valid(self, table):  # A9
        put(table, 1.0, 1.0, 15.0, 15.0)
        assert rec(table, 1.0, 1.0) == (15.0, 15.0)

    def test_negative_temperatures(self, table):
        put(table, 1.0, 1.0, -60.0, -20.0)
        assert rec(table, 1.0, 1.0) == (-60.0, -20.0)

    def test_zero_temperatures(self, table):
        put(table, 1.0, 1.0, 0.0, 0.0)
        assert rec(table, 1.0, 1.0) == (0.0, 0.0)

    def test_temperature_spanning_zero(self, table):
        put(table, 1.0, 1.0, -0.1, 0.1)
        assert rec(table, 1.0, 1.0) == (-0.1, 0.1)

    def test_very_large_and_small_finite_temperatures(self, table):  # A11
        put(table, 1.0, 1.0, -1e6, 1e6)
        assert rec(table, 1.0, 1.0) == (-1e6, 1e6)

    def test_high_precision_temperatures_preserved(self, table):
        put(table, 1.0, 1.0, -12.345678901, 34.567890123)
        assert rec(table, 1.0, 1.0) == (-12.345678901, 34.567890123)

    def test_high_precision_coordinates_preserved(self, table):
        put(table, 41.80727123456, -72.24919876543, 0.0, 1.0)
        assert rec(table, 41.80727123456, -72.24919876543) == (0.0, 1.0)


# ----------------------------------------------------------------------------
# Scale, collisions, and resizing (A12)
# ----------------------------------------------------------------------------
class TestScaleAndCollisions:
    def test_many_records_all_retrievable(self, table):
        n = 5000
        for i in range(n):
            lat = (i % 180) - 90.0
            lon = (i // 180) * 0.5 - 180.0
            put(table, lat, lon, float(i), float(i) + 1.0)
        assert len(table) == n
        for i in range(n):
            lat = (i % 180) - 90.0
            lon = (i // 180) * 0.5 - 180.0
            assert rec(table, lat, lon) == (float(i), float(i) + 1.0)

    def test_grid_of_neighboring_positions(self, table):
        # Dense, regular grid is a likely source of hash collisions.
        for lat in range(-20, 21):
            for lon in range(-20, 21):
                put(table, float(lat), float(lon), float(lat), float(lon) + 100.0)
        assert len(table) == 41 * 41
        for lat in range(-20, 21):
            for lon in range(-20, 21):
                assert rec(table, float(lat), float(lon)) == (float(lat), float(lon) + 100.0)

    def test_symmetric_positions_that_could_collide(self, table):
        # (a, b) and (b, a), plus sign flips, stress naive symmetric hashes (e.g. lat + lon).
        pts = [(1.0, 2.0), (2.0, 1.0), (-1.0, -2.0), (-2.0, -1.0), (3.0, 0.0), (0.0, 3.0)]
        for i, (la, lo) in enumerate(pts):
            put(table, la, lo, float(i), float(i) + 1.0)
        assert len(table) == len(pts)
        for i, (la, lo) in enumerate(pts):
            assert rec(table, la, lo) == (float(i), float(i) + 1.0)

    def test_remove_half_then_remaining_still_retrievable(self, table):
        pts = [(float(i % 90), float(i // 90)) for i in range(1000)]
        for i, (la, lo) in enumerate(pts):
            put(table, la, lo, float(i), float(i) + 1.0)
        for i, (la, lo) in enumerate(pts):
            if i % 2 == 0:
                assert delete(table, la, lo) is True
        assert len(table) == 500
        for i, (la, lo) in enumerate(pts):
            if i % 2 == 0:
                assert fetch(table, la, lo) is MISSING
            else:
                assert rec(table, la, lo) == (float(i), float(i) + 1.0)

    def test_repeated_insert_remove_cycles(self, table):
        for cycle in range(50):
            for i in range(20):
                put(table, float(i), float(i), float(cycle), float(cycle) + 1.0)
            for i in range(20):
                assert delete(table, float(i), float(i)) is True
        assert len(table) == 0
        assert fetch(table, 5.0, 5.0) is MISSING

    def test_insert_after_many_removals_reuses_table_correctly(self, table):
        for i in range(500):
            put(table, float(i % 90), float(i // 90), 0.0, 1.0)
        for i in range(500):
            delete(table, float(i % 90), float(i // 90))
        put(table, 7.0, 7.0, -1.0, 2.0)
        assert len(table) == 1
        assert rec(table, 7.0, 7.0) == (-1.0, 2.0)


# ----------------------------------------------------------------------------
# Invalid inputs (A8)
# ----------------------------------------------------------------------------
class TestInvalidInputs:
    @pytest.mark.parametrize(
        "lat, lon",
        [
            (90.0001, 0.0),
            (-90.0001, 0.0),
            (0.0, 180.0001),
            (0.0, -180.0001),
            (91, 0),
            (0, 181),
            (1000.0, 1000.0),
            (-1000.0, -1000.0),
        ],
    )
    def test_out_of_range_coordinates_rejected_on_insert(self, table, lat, lon):
        with pytest.raises(RANGE_ERROR):
            put(table, lat, lon, 0.0, 1.0)
        assert len(table) == 0

    @pytest.mark.parametrize(
        "lat, lon",
        [
            (float("nan"), 0.0),
            (0.0, float("nan")),
            (float("inf"), 0.0),
            (0.0, float("-inf")),
        ],
    )
    def test_nan_and_infinite_coordinates_rejected(self, table, lat, lon):
        with pytest.raises(RANGE_ERROR):
            put(table, lat, lon, 0.0, 1.0)
        assert len(table) == 0

    def test_min_greater_than_max_rejected(self, table):
        with pytest.raises(RANGE_ERROR):
            put(table, 1.0, 1.0, 20.0, 10.0)
        assert len(table) == 0
        assert fetch(table, 1.0, 1.0) is MISSING

    def test_invalid_overwrite_does_not_clobber_existing_record(self, table):
        put(table, 1.0, 1.0, 0.0, 10.0)
        with pytest.raises(RANGE_ERROR):
            put(table, 1.0, 1.0, 50.0, 40.0)
        assert rec(table, 1.0, 1.0) == (0.0, 10.0)
        assert len(table) == 1

    @pytest.mark.parametrize(
        "tmin, tmax",
        [
            (float("nan"), 1.0),
            (0.0, float("nan")),
            (float("nan"), float("nan")),
        ],
    )
    def test_nan_temperatures_rejected(self, table, tmin, tmax):
        with pytest.raises(RANGE_ERROR):
            put(table, 1.0, 1.0, tmin, tmax)
        assert len(table) == 0

    @pytest.mark.parametrize(
        "lat, lon, tmin, tmax",
        [
            ("10", 20.0, 0.0, 1.0),
            (10.0, "20", 0.0, 1.0),
            (10.0, 20.0, "0", 1.0),
            (10.0, 20.0, 0.0, "1"),
            (None, 20.0, 0.0, 1.0),
            (10.0, None, 0.0, 1.0),
            (10.0, 20.0, None, 1.0),
            (10.0, 20.0, 0.0, None),
            ([10.0], 20.0, 0.0, 1.0),
            (10.0, 20.0, {}, 1.0),
        ],
    )
    def test_non_numeric_arguments_rejected_on_insert(self, table, lat, lon, tmin, tmax):
        with pytest.raises(TYPE_ERROR):
            put(table, lat, lon, tmin, tmax)
        assert len(table) == 0

    @pytest.mark.parametrize("lat, lon", [("10", 20.0), (10.0, "20"), (None, None)])
    def test_non_numeric_coordinates_rejected_on_get(self, table, lat, lon):
        with pytest.raises(TYPE_ERROR):
            fetch(table, lat, lon)

    def test_insert_with_missing_arguments_raises_type_error(self, table):
        with pytest.raises(TypeError):
            getattr(table, INSERT)(1.0, 1.0, 0.0)  # missing max_temp

    def test_get_with_missing_arguments_raises_type_error(self, table):
        with pytest.raises(TypeError):
            getattr(table, GET)(1.0)  # missing longitude


# ----------------------------------------------------------------------------
# Unusual but valid usage
# ----------------------------------------------------------------------------
class TestUnusualButValid:
    def test_numpy_style_numeric_types_if_available(self, table):
        np = pytest.importorskip("numpy")
        put(table, np.float64(10.5), np.float64(20.5), np.float64(-1.0), np.float64(2.0))
        assert rec(table, 10.5, 20.5) == (-1.0, 2.0)

    def test_denormal_and_tiny_coordinates(self, table):
        put(table, 5e-324, 5e-324, 0.0, 1.0)
        assert rec(table, 5e-324, 5e-324) == (0.0, 1.0)

    def test_float_arithmetic_result_as_key_matches_exact_literal_only_if_equal(self, table):
        # 0.1 + 0.2 != 0.3 in IEEE-754; with exact-match keys (A10) these are distinct.
        put(table, 0.3, 0.3, 1.0, 2.0)
        assert fetch(table, 0.1 + 0.2, 0.3) is MISSING

    def test_stored_record_not_affected_by_mutating_returned_value(self, table):
        put(table, 1.0, 1.0, 0.0, 10.0)
        r = fetch(table, 1.0, 1.0)
        try:
            r[0] = 999  # tuples raise TypeError; lists/objects may allow mutation
        except (TypeError, AttributeError):
            pass
        assert rec(table, 1.0, 1.0) == (0.0, 10.0)

    def test_interleaved_operations_consistency(self, table):
        put(table, 1.0, 1.0, 0.0, 1.0)
        put(table, 2.0, 2.0, 0.0, 2.0)
        delete(table, 1.0, 1.0)
        put(table, 3.0, 3.0, 0.0, 3.0)
        put(table, 1.0, 1.0, 9.0, 10.0)
        delete(table, 2.0, 2.0)
        assert len(table) == 2
        assert rec(table, 1.0, 1.0) == (9.0, 10.0)
        assert rec(table, 3.0, 3.0) == (0.0, 3.0)
        assert fetch(table, 2.0, 2.0) is MISSING