"""
Unit tests (pytest) for a hash table that stores minimum and maximum
temperature records at geographic positions (latitude, longitude).

The description does not give the API, so everything below that is not
stated in it is an explicit assumption. The names an adapter needs are
isolated in the CONFIGURATION block, so a mismatch is a one-line change.

ASSUMPTIONS
 A1. The module is `temperature_table`, the class is `TemperatureHashTable`,
     and the constructor takes no arguments.
 A2. put(lat, lon, min_temp, max_temp) inserts a record, or overwrites the
     existing record at that position (it does not merge or compare).
 A3. get(lat, lon) returns the record for that position. A record exposes
     its minimum and maximum as a 2-tuple (min, max), a dict, or an object
     with min/max or min_temp/max_temp attributes. For a missing position,
     get returns None or raises KeyError (both are accepted).
 A4. remove(lat, lon) deletes the record. Removing a missing position
     either does nothing or raises KeyError (both are accepted).
 A5. len(table) is the number of distinct stored positions.
 A6. A position is identified by the exact (lat, lon) pair. There is no
     tolerance, so 45.0 and 45.0000001 are different positions. Numeric
     equality applies, so 10 == 10.0 and 0.0 == -0.0.
 A7. Valid latitude is [-90, 90] and valid longitude is [-180, 180],
     both inclusive. Out-of-range, NaN, infinite or non-numeric
     coordinates raise ValueError or TypeError, and a rejected put leaves
     the table unchanged. Set VALIDATES_INPUT = False to skip these tests
     if the program does not validate.
 A8. min_temp <= max_temp. Equal values are allowed. min_temp > max_temp,
     NaN, or non-numeric temperatures raise ValueError or TypeError.
 A9. Temperature units are not specified, so tests use plausible Celsius
     values and never assume an absolute-zero bound.
 A10. Whether longitude -180 and +180 (the same meridian) are the same key
      is unspecified, so the tests only check that both are accepted.
 A11. A lookup with invalid coordinates returns None or raises
      ValueError/TypeError/KeyError. It must not raise anything else.
"""

import importlib
import math
import random

import pytest

# ----------------------------- CONFIGURATION -----------------------------
MODULE_NAME = "RecordsMap"
CLASS_NAME = "RecordsMap"
PUT, GET, REMOVE = "add_report", "__getitem__", "remove"
VALIDATES_INPUT = True
# -------------------------------------------------------------------------

INVALID_EXC = (ValueError, TypeError)


# ------------------------------- adapter ---------------------------------
def _table_class():
    return getattr(importlib.import_module(MODULE_NAME), CLASS_NAME)


def _min_max(rec):
    if isinstance(rec, (tuple, list)) and len(rec) == 2:
        return rec[0], rec[1]
    names = (("min", "max"), ("min_temp", "max_temp"), ("minimum", "maximum"))
    if isinstance(rec, dict):
        for lo, hi in names:
            if lo in rec and hi in rec:
                return rec[lo], rec[hi]
    for lo, hi in names:
        if hasattr(rec, lo) and hasattr(rec, hi):
            return getattr(rec, lo), getattr(rec, hi)
    raise AssertionError(f"Cannot extract (min, max) from record {rec!r}")


def put(t, lat, lon, mn, mx):
    t.add_report((lat, lon), mn)
    return t.add_report((lat, lon), mx)


def lookup(t, lat, lon):
    """Return (min, max) or None if the position is absent (A3)."""
    try:
        rec = t[(lat, lon)]
    except KeyError:
        return None
    return None if rec is None else _min_max(rec)


def remove(t, lat, lon):
    """Remove a position; a missing position is tolerated (A4)."""
    try:
        return getattr(t, REMOVE)(lat, lon)
    except KeyError:
        return None


@pytest.fixture
def table():
    return _table_class()()


# ------------------------------ normal cases -----------------------------
class TestNormalUsage:
    def test_new_table_is_empty(self, table):
        assert len(table) == 0

    def test_lookup_in_empty_table_returns_nothing(self, table):
        assert lookup(table, 41.8, -72.2) is None

    def test_insert_then_get(self, table):
        put(table, 41.8077, -72.2540, -5.5, 31.2)
        assert lookup(table, 41.8077, -72.2540) == (-5.5, 31.2)
        assert len(table) == 1

    def test_multiple_distinct_positions_are_independent(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        put(table, -10.0, -20.0, -3.0, -1.0)
        put(table, 55.5, 120.25, 5.0, 25.0)
        assert lookup(table, 10.0, 20.0) == (1.0, 2.0)
        assert lookup(table, -10.0, -20.0) == (-3.0, -1.0)
        assert lookup(table, 55.5, 120.25) == (5.0, 25.0)
        assert len(table) == 3

    def test_lookup_of_absent_position_among_others(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        assert lookup(table, 10.0, 21.0) is None
        assert lookup(table, 11.0, 20.0) is None

    def test_overwrite_replaces_record_and_keeps_size(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        put(table, 10.0, 20.0, -4.0, 9.0)
        assert lookup(table, 10.0, 20.0) == (-4.0, 9.0)
        assert len(table) == 1

    def test_overwrite_with_narrower_range_is_not_merged(self, table):
        # A2: put overwrites; it does not widen or merge ranges.
        put(table, 10.0, 20.0, -10.0, 30.0)
        put(table, 10.0, 20.0, 0.0, 5.0)
        assert lookup(table, 10.0, 20.0) == (0.0, 5.0)

    def test_overwrite_does_not_affect_other_positions(self, table):
        put(table, 1.0, 1.0, 0.0, 1.0)
        put(table, 2.0, 2.0, 0.0, 2.0)
        put(table, 1.0, 1.0, -9.0, 9.0)
        assert lookup(table, 2.0, 2.0) == (0.0, 2.0)

    def test_remove_existing_position(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        remove(table, 10.0, 20.0)
        assert lookup(table, 10.0, 20.0) is None
        assert len(table) == 0

    def test_remove_leaves_other_positions(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        put(table, 30.0, 40.0, 3.0, 4.0)
        remove(table, 10.0, 20.0)
        assert lookup(table, 30.0, 40.0) == (3.0, 4.0)
        assert len(table) == 1

    def test_reinsert_after_remove(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        remove(table, 10.0, 20.0)
        put(table, 10.0, 20.0, 7.0, 8.0)
        assert lookup(table, 10.0, 20.0) == (7.0, 8.0)
        assert len(table) == 1

    def test_remove_missing_position_is_harmless(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        remove(table, 99.0, 99.0)  # A4: no-op or KeyError, both tolerated
        assert len(table) == 1
        assert lookup(table, 10.0, 20.0) == (1.0, 2.0)

    def test_double_remove_is_harmless(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        remove(table, 10.0, 20.0)
        remove(table, 10.0, 20.0)
        assert len(table) == 0


# ---------------------------- boundary / edge ----------------------------
class TestBoundaries:
    @pytest.mark.parametrize(
        "lat, lon",
        [
            (90.0, 0.0), (-90.0, 0.0),
            (0.0, 180.0), (0.0, -180.0),
            (90.0, 180.0), (90.0, -180.0),
            (-90.0, 180.0), (-90.0, -180.0),
            (0.0, 0.0),
        ],
    )
    def test_extreme_valid_coordinates_are_accepted(self, table, lat, lon):
        put(table, lat, lon, -1.0, 1.0)
        assert lookup(table, lat, lon) == (-1.0, 1.0)

    def test_poles_with_different_longitudes_stored_as_distinct_keys(self, table):
        # Assumes distinct (lat, lon) pairs are distinct keys (A6), even
        # though physically the pole is a single point.
        put(table, 90.0, 0.0, -30.0, -20.0)
        put(table, 90.0, 90.0, -31.0, -21.0)
        assert lookup(table, 90.0, 0.0) == (-30.0, -20.0)
        assert lookup(table, 90.0, 90.0) == (-31.0, -21.0)

    def test_both_antimeridian_longitudes_accepted(self, table):
        # A10: only checks acceptance, not whether they are the same key.
        put(table, 10.0, 180.0, 1.0, 2.0)
        put(table, 10.0, -180.0, 3.0, 4.0)
        assert lookup(table, 10.0, 180.0) is not None
        assert lookup(table, 10.0, -180.0) is not None

    def test_min_equals_max(self, table):
        put(table, 5.0, 5.0, 12.5, 12.5)
        assert lookup(table, 5.0, 5.0) == (12.5, 12.5)

    def test_zero_and_negative_temperatures(self, table):
        put(table, 1.0, 1.0, 0.0, 0.0)
        put(table, 2.0, 2.0, -40.0, -40.0)
        assert lookup(table, 1.0, 1.0) == (0.0, 0.0)
        assert lookup(table, 2.0, 2.0) == (-40.0, -40.0)

    def test_record_temperature_extremes(self, table):
        put(table, 36.0, -116.8, -89.2, 56.7)
        assert lookup(table, 36.0, -116.8) == (-89.2, 56.7)

    def test_integer_temperatures_are_accepted(self, table):
        put(table, 1.0, 1.0, -3, 7)
        assert lookup(table, 1.0, 1.0) == (-3, 7)

    def test_integer_and_float_coordinates_are_same_key(self, table):
        # A6: numeric equality, 10 == 10.0
        put(table, 10, 20, 1.0, 2.0)
        assert lookup(table, 10.0, 20.0) == (1.0, 2.0)
        put(table, 10.0, 20.0, 3.0, 4.0)
        assert len(table) == 1

    def test_negative_zero_equals_zero(self, table):
        # A6: 0.0 == -0.0
        put(table, 0.0, 0.0, 1.0, 2.0)
        assert lookup(table, -0.0, -0.0) == (1.0, 2.0)
        put(table, -0.0, -0.0, 3.0, 4.0)
        assert len(table) == 1

    def test_very_close_coordinates_are_distinct(self, table):
        # A6: no tolerance is applied to coordinates.
        put(table, 45.0, 45.0, 1.0, 2.0)
        put(table, 45.0000001, 45.0, 3.0, 4.0)
        put(table, 45.0, 45.0000001, 5.0, 6.0)
        assert len(table) == 3
        assert lookup(table, 45.0, 45.0) == (1.0, 2.0)
        assert lookup(table, 45.0000001, 45.0) == (3.0, 4.0)
        assert lookup(table, 45.0, 45.0000001) == (5.0, 6.0)

    def test_many_decimal_places(self, table):
        put(table, 41.80771234567, -72.25401234567, 1.0, 2.0)
        assert lookup(table, 41.80771234567, -72.25401234567) == (1.0, 2.0)


# ------------------- collisions, ordering, symmetry bugs -----------------
class TestCollisionResistance:
    def test_swapped_latitude_longitude_are_distinct(self, table):
        # Catches symmetric hash functions such as lat + lon or lat ^ lon.
        put(table, 10.0, 20.0, 1.0, 2.0)
        put(table, 20.0, 10.0, 3.0, 4.0)
        assert len(table) == 2
        assert lookup(table, 10.0, 20.0) == (1.0, 2.0)
        assert lookup(table, 20.0, 10.0) == (3.0, 4.0)

    def test_same_coordinate_sum_are_distinct(self, table):
        pts = [(0.0, 30.0), (30.0, 0.0), (15.0, 15.0), (10.0, 20.0), (-10.0, 40.0)]
        for i, (la, lo) in enumerate(pts):
            put(table, la, lo, float(i), float(i) + 0.5)
        assert len(table) == len(pts)
        for i, (la, lo) in enumerate(pts):
            assert lookup(table, la, lo) == (float(i), float(i) + 0.5)

    def test_sign_flipped_positions_are_distinct(self, table):
        pts = [(10.0, 20.0), (-10.0, 20.0), (10.0, -20.0), (-10.0, -20.0)]
        for i, (la, lo) in enumerate(pts):
            put(table, la, lo, float(i), float(i) + 1)
        assert len(table) == 4
        for i, (la, lo) in enumerate(pts):
            assert lookup(table, la, lo) == (float(i), float(i) + 1)

    def test_remove_one_of_many_does_not_hide_others(self, table):
        # Guards against broken probing/chaining when deleting.
        pts = [(float(i), float(i)) for i in range(50)]
        for la, lo in pts:
            put(table, la, lo, la - 1, la + 1)
        for la, lo in pts[::2]:
            remove(table, la, lo)
        for idx, (la, lo) in enumerate(pts):
            expected = None if idx % 2 == 0 else (la - 1, la + 1)
            assert lookup(table, la, lo) == expected
        assert len(table) == 25

    def test_reinsert_after_removing_in_a_crowded_table(self, table):
        pts = [(float(i % 90), float(i // 90)) for i in range(300)]
        for la, lo in pts:
            put(table, la, lo, 0.0, 1.0)
        for la, lo in pts[:100]:
            remove(table, la, lo)
        for la, lo in pts[:100]:
            put(table, la, lo, -2.0, 2.0)
        assert len(table) == 300
        for la, lo in pts[:100]:
            assert lookup(table, la, lo) == (-2.0, 2.0)
        for la, lo in pts[100:]:
            assert lookup(table, la, lo) == (0.0, 1.0)


# ---------------------------- scale / resizing ---------------------------
class TestScale:
    def test_many_distinct_positions_all_retrievable(self, table):
        n = 5000
        pts = [(-90.0 + (i % 181), -180.0 + (i // 181)) for i in range(n)]
        assert len(set(pts)) == n
        for i, (la, lo) in enumerate(pts):
            put(table, la, lo, -i / 100.0, i / 100.0)
        assert len(table) == n
        for i, (la, lo) in enumerate(pts):
            assert lookup(table, la, lo) == (-i / 100.0, i / 100.0)

    def test_many_overwrites_of_one_position(self, table):
        for i in range(2000):
            put(table, 12.0, 34.0, float(-i), float(i))
        assert len(table) == 1
        assert lookup(table, 12.0, 34.0) == (-1999.0, 1999.0)

    def test_fill_then_empty_then_reuse(self, table):
        pts = [(float(i % 91), float(i // 91)) for i in range(1000)]
        for la, lo in pts:
            put(table, la, lo, 0.0, 1.0)
        for la, lo in pts:
            remove(table, la, lo)
        assert len(table) == 0
        for la, lo in pts:
            assert lookup(table, la, lo) is None
        put(table, 1.0, 1.0, 5.0, 6.0)
        assert lookup(table, 1.0, 1.0) == (5.0, 6.0)
        assert len(table) == 1

    def test_randomized_operations_match_reference_dict(self, table):
        # Differential test against a plain dict; a small key space
        # forces many overwrites, removals and collisions.
        rng = random.Random(20261102)
        lats = [-90.0, -45.5, -1.0, 0.0, 1.0, 45.5, 90.0]
        lons = [-180.0, -90.25, -0.5, 0.0, 0.5, 90.25, 180.0]
        model = {}
        for step in range(6000):
            la, lo = rng.choice(lats), rng.choice(lons)
            op = rng.random()
            if op < 0.5:
                mn = round(rng.uniform(-50, 20), 2)
                mx = round(mn + rng.uniform(0, 40), 2)
                put(table, la, lo, mn, mx)
                model[(la, lo)] = (mn, mx)
            elif op < 0.75:
                remove(table, la, lo)
                model.pop((la, lo), None)
            else:
                assert lookup(table, la, lo) == model.get((la, lo)), f"step {step}"
            assert len(table) == len(model), f"step {step}"
        for (la, lo), rec in model.items():
            assert lookup(table, la, lo) == rec


# ---------------------------- invalid inputs -----------------------------
@pytest.mark.skipif(not VALIDATES_INPUT, reason="program does not validate input (A7/A8)")
class TestInvalidInputs:
    @pytest.mark.parametrize(
        "lat, lon",
        [
            (90.0001, 0.0), (-90.0001, 0.0), (91, 0), (-91, 0), (1e9, 0),
            (0.0, 180.0001), (0.0, -180.0001), (0, 181), (0, -181), (0, 1e9),
            (float("nan"), 0.0), (0.0, float("nan")),
            (float("inf"), 0.0), (float("-inf"), 0.0),
            (0.0, float("inf")), (0.0, float("-inf")),
        ],
    )
    def test_out_of_range_or_non_finite_coordinates_rejected(self, table, lat, lon):
        with pytest.raises(INVALID_EXC):
            put(table, lat, lon, 0.0, 1.0)
        assert len(table) == 0

    @pytest.mark.parametrize(
        "lat, lon",
        [("10", 20.0), (10.0, "20"), (None, 20.0), (10.0, None),
         ([10.0], 20.0), (10.0, (20.0,)), ({}, 20.0), ("", "")],
    )
    def test_non_numeric_coordinates_rejected(self, table, lat, lon):
        with pytest.raises(INVALID_EXC):
            put(table, lat, lon, 0.0, 1.0)
        assert len(table) == 0

    def test_min_greater_than_max_rejected(self, table):
        with pytest.raises(INVALID_EXC):
            put(table, 10.0, 20.0, 5.0, -5.0)
        assert len(table) == 0

    @pytest.mark.parametrize(
        "mn, mx",
        [(float("nan"), 1.0), (0.0, float("nan")),
         (float("nan"), float("nan")),
         ("0", 1.0), (0.0, "1"), (None, 1.0), (0.0, None),
         ([0.0], 1.0), (0.0, [1.0])],
    )
    def test_invalid_temperature_values_rejected(self, table, mn, mx):
        with pytest.raises(INVALID_EXC):
            put(table, 10.0, 20.0, mn, mx)
        assert len(table) == 0

    def test_rejected_overwrite_keeps_existing_record(self, table):
        put(table, 10.0, 20.0, 1.0, 2.0)
        with pytest.raises(INVALID_EXC):
            put(table, 10.0, 20.0, 9.0, -9.0)
        assert lookup(table, 10.0, 20.0) == (1.0, 2.0)
        assert len(table) == 1

    def test_rejected_put_among_valid_puts_leaves_others_intact(self, table):
        put(table, 1.0, 1.0, 0.0, 1.0)
        with pytest.raises(INVALID_EXC):
            put(table, 200.0, 1.0, 0.0, 1.0)
        put(table, 2.0, 2.0, 0.0, 2.0)
        assert len(table) == 2
        assert lookup(table, 1.0, 1.0) == (0.0, 1.0)
        assert lookup(table, 2.0, 2.0) == (0.0, 2.0)

    def test_put_with_missing_arguments_raises_typeerror(self, table):
        with pytest.raises(TypeError):
            getattr(table, PUT)(10.0, 20.0)
        with pytest.raises(TypeError):
            getattr(table, PUT)()

    @pytest.mark.parametrize(
        "lat, lon",
        [(91.0, 0.0), (0.0, 181.0), (float("nan"), 0.0), ("a", "b"), (None, None)],
    )
    def test_lookup_with_invalid_coordinates_fails_cleanly(self, table, lat, lon):
        # A11: absent result or ValueError/TypeError/KeyError only.
        try:
            rec = table[(lat, lon)]
        except (ValueError, TypeError, KeyError):
            return
        assert rec is None

    @pytest.mark.parametrize(
        "lat, lon",
        [(91.0, 0.0), (0.0, 181.0), (float("nan"), 0.0), ("a", "b"), (None, None)],
    )
    def test_remove_with_invalid_coordinates_fails_cleanly(self, table, lat, lon):
        put(table, 1.0, 1.0, 0.0, 1.0)
        try:
            getattr(table, REMOVE)(lat, lon)
        except (ValueError, TypeError, KeyError):
            pass
        assert len(table) == 1
        assert lookup(table, 1.0, 1.0) == (0.0, 1.0)


# ------------------------------ unusual inputs ---------------------------
class TestUnusualButValidInputs:
    def test_tables_are_independent_instances(self):
        a, b = _table_class()(), _table_class()()
        put(a, 1.0, 1.0, 0.0, 1.0)
        assert lookup(b, 1.0, 1.0) is None
        assert len(a) == 1 and len(b) == 0

    def test_subnormal_and_tiny_coordinates(self, table):
        put(table, 5e-324, 5e-324, 0.0, 1.0)
        put(table, 1e-12, 1e-12, 2.0, 3.0)
        assert lookup(table, 5e-324, 5e-324) == (0.0, 1.0)
        assert lookup(table, 1e-12, 1e-12) == (2.0, 3.0)

    def test_large_magnitude_valid_temperatures(self, table):
        put(table, 1.0, 1.0, -1e6, 1e6)
        assert lookup(table, 1.0, 1.0) == (-1e6, 1e6)

    def test_lookup_does_not_modify_table(self, table):
        put(table, 1.0, 1.0, 0.0, 1.0)
        for _ in range(10):
            lookup(table, 1.0, 1.0)
            lookup(table, 2.0, 2.0)
        assert len(table) == 1
        assert lookup(table, 1.0, 1.0) == (0.0, 1.0)

    def test_stored_temperatures_survive_unchanged(self, table):
        put(table, 1.0, 1.0, -0.1, 0.1)
        mn, mx = lookup(table, 1.0, 1.0)
        assert mn == -0.1 and mx == 0.1
        assert not math.isnan(mn) and not math.isnan(mx)
