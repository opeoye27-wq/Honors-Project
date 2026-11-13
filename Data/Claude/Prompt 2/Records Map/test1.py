
"""
Unit tests (pytest) for a hash table that stores min/max temperature records
keyed by geographic position.

==============================  ASSUMPTIONS  ==============================
The description does not give names or signatures, so everything the tests
depend on is isolated in the CONFIGURATION / ADAPTER section. Edit those
constants to match the real program; the tests themselves should not need
to change.

A1. Module / class: `temperature_table.TemperatureHashTable`.
A2. Constructor: default constructor works. If INITIAL_CAPACITY_KWARG is set
    (e.g. "capacity"), the constructor accepts an initial capacity under that
    keyword. Tests needing a specific small capacity are skipped if it is None.
A3. Reporting a temperature is `table.<METHOD_REPORT>(x, y, temp)`. Positions
    are passed as two arguments (set POSITION_AS_TUPLE = True if passed as one
    (x, y) tuple).
A4. Lookups are `table.<METHOD_GET_MIN>(x, y)` and `table.<METHOD_GET_MAX>(x, y)`.
A5. Membership is `table.<METHOD_CONTAINS>(x, y)`, or the `in` operator when
    METHOD_CONTAINS is None (the key is then an (x, y) tuple).
A6. Unique-position count is `table.<METHOD_SIZE>()`, or len(table) when
    METHOD_SIZE is None.
A7. Capacity is observable via attribute `CAPACITY_ATTR` (an int, the number of
    buckets). Resize tests are skipped if it is not observable.
A8. Rounding: "nearest whole number". Python's round() uses banker's rounding
    (round(0.5) == 0, round(1.5) == 2) while "round half up" gives different
    ties. The description is ambiguous for exact .5 ties, so tests NEVER assert
    which integer a tie maps to; they only assert determinism/consistency.
    All other rounding tests avoid ties.
A9. Load factor = unique_positions / capacity. "Exceeds 0.7" means strictly
    greater than 0.7, so a load of exactly 0.7 must NOT trigger a resize.
A10. The resize check happens right after an insertion of a NEW position, so
     after every insertion size / capacity <= 0.7. (If the real program checks
     before inserting, the "invariant after every insert" test is the one to
     revisit.)
A11. Capacity never shrinks. The growth factor is unspecified, so tests only
     require capacity to strictly increase when a resize happens.
A12. Updating an existing position (even many times) does not change the
     unique count and does not itself trigger a resize.
A13. contains() on a missing position returns False (does not raise) and, like
     lookups of missing positions, never inserts anything.
A14. Non-numeric coordinates or temperatures raise TypeError or ValueError.
     The description does not specify this; those tests accept either.
A15. Temperatures may be ints or floats and may be negative or zero. NaN, inf
     and bool inputs are unspecified and not tested.
=============================================================================
"""

import random

import pytest

# ---------------------------------------------------------------------------
# CONFIGURATION / ADAPTER  (edit to match the real program)
# ---------------------------------------------------------------------------
from RecordsMap import RecordsMap  # noqa: E402

INITIAL_CAPACITY_KWARG = "capacity"   # or None if the constructor takes no capacity
METHOD_REPORT = "add_report"          # table.add_report((x, y), temp)
METHOD_GET_MIN = None                 # RecordsMap lookup returns (min, max)
METHOD_GET_MAX = None                 # RecordsMap lookup returns (min, max)
METHOD_CONTAINS = None                # use `(x, y) in table`
METHOD_SIZE = None                    # len(table)
CAPACITY_ATTR = "capacity"            # or None if capacity is not observable
POSITION_AS_TUPLE = True              # methods take one (x, y) tuple

LOAD_FACTOR_LIMIT = 0.7


def _pos(x, y):
    return ((x, y),) if POSITION_AS_TUPLE else (x, y)


def make_table(capacity=None):
    if capacity is None:
        return RecordsMap()
    if INITIAL_CAPACITY_KWARG is None:
        pytest.skip("Constructor does not accept an initial capacity (assumption A2)")
    return RecordsMap(**{INITIAL_CAPACITY_KWARG: capacity})


def report(table, x, y, temp):
    return table.add_report((x, y), temp)


def get_min(table, x, y):
    return table[(x, y)][0]


def get_max(table, x, y):
    return table[(x, y)][1]


def contains(table, x, y):
    return (x, y) in table


def size(table):
    return len(table)


def capacity_of(table):
    if CAPACITY_ATTR is None or not hasattr(table, CAPACITY_ATTR):
        pytest.skip("Capacity is not observable (assumption A7)")
    value = getattr(table, CAPACITY_ATTR)
    return value() if callable(value) else value


def assert_record(table, x, y, expected_min, expected_max):
    assert contains(table, x, y) is True
    assert get_min(table, x, y) == expected_min
    assert get_max(table, x, y) == expected_max


@pytest.fixture
def table():
    return make_table()


# ---------------------------------------------------------------------------
# Empty table
# ---------------------------------------------------------------------------
class TestEmptyTable:
    def test_new_table_has_zero_unique_positions(self, table):
        assert size(table) == 0

    def test_contains_is_false_on_empty_table(self, table):
        assert contains(table, 0, 0) is False
        assert contains(table, 10, -10) is False

    def test_get_min_on_empty_table_raises_key_error(self, table):
        with pytest.raises(KeyError):
            get_min(table, 1, 1)

    def test_get_max_on_empty_table_raises_key_error(self, table):
        with pytest.raises(KeyError):
            get_max(table, 1, 1)

    def test_failed_lookup_does_not_insert(self, table):
        with pytest.raises(KeyError):
            get_min(table, 3, 4)
        with pytest.raises(KeyError):
            get_max(table, 3, 4)
        assert size(table) == 0
        assert contains(table, 3, 4) is False

    def test_contains_does_not_insert(self, table):
        contains(table, 5, 5)
        assert size(table) == 0


# ---------------------------------------------------------------------------
# Creating records
# ---------------------------------------------------------------------------
class TestNewRecords:
    def test_first_report_sets_min_and_max_to_that_temperature(self, table):
        report(table, 10, 20, 15.5)
        assert_record(table, 10, 20, 15.5, 15.5)
        assert size(table) == 1

    def test_integer_temperature(self, table):
        report(table, 1, 1, 7)
        assert_record(table, 1, 1, 7, 7)

    def test_zero_temperature_creates_valid_record(self, table):
        # Guards against falsy-zero bugs ("if not temp" / "if not record").
        report(table, 2, 2, 0)
        assert contains(table, 2, 2) is True
        assert_record(table, 2, 2, 0, 0)
        assert size(table) == 1

    def test_negative_temperature(self, table):
        report(table, 2, 3, -12.5)
        assert_record(table, 2, 3, -12.5, -12.5)

    def test_origin_position_is_a_valid_key(self, table):
        # Guards against falsy-zero bugs on coordinates.
        report(table, 0, 0, 3)
        assert contains(table, 0, 0) is True
        assert_record(table, 0, 0, 3, 3)
        assert size(table) == 1

    def test_negative_coordinates(self, table):
        report(table, -45, -170, 9)
        assert_record(table, -45, -170, 9, 9)

    def test_float_coordinates_that_are_already_whole(self, table):
        report(table, 5.0, 6.0, 1)
        assert_record(table, 5, 6, 1, 1)

    def test_very_large_coordinates(self, table):
        report(table, 10**9, -10**9, 4)
        assert_record(table, 10**9, -10**9, 4, 4)

    def test_distinct_positions_get_independent_records(self, table):
        report(table, 1, 1, 10)
        report(table, 2, 2, 20)
        report(table, 3, 3, 30)
        assert size(table) == 3
        assert_record(table, 1, 1, 10, 10)
        assert_record(table, 2, 2, 20, 20)
        assert_record(table, 3, 3, 30, 30)

    def test_coordinate_order_matters(self, table):
        report(table, 1, 2, 10)
        report(table, 2, 1, 50)
        assert size(table) == 2
        assert_record(table, 1, 2, 10, 10)
        assert_record(table, 2, 1, 50, 50)

    def test_sign_of_coordinates_matters(self, table):
        report(table, 3, 4, 1)
        report(table, -3, 4, 2)
        report(table, 3, -4, 3)
        report(table, -3, -4, 4)
        assert size(table) == 4
        assert_record(table, 3, 4, 1, 1)
        assert_record(table, -3, 4, 2, 2)
        assert_record(table, 3, -4, 3, 3)
        assert_record(table, -3, -4, 4, 4)


# ---------------------------------------------------------------------------
# Updating min / max
# ---------------------------------------------------------------------------
class TestUpdates:
    def test_lower_temperature_updates_min_only(self, table):
        report(table, 1, 1, 10)
        report(table, 1, 1, 4)
        assert_record(table, 1, 1, 4, 10)

    def test_higher_temperature_updates_max_only(self, table):
        report(table, 1, 1, 10)
        report(table, 1, 1, 25)
        assert_record(table, 1, 1, 10, 25)

    def test_temperature_between_min_and_max_changes_nothing(self, table):
        report(table, 1, 1, 0)
        report(table, 1, 1, 20)
        report(table, 1, 1, 10)
        assert_record(table, 1, 1, 0, 20)

    def test_temperature_equal_to_existing_min_and_max(self, table):
        report(table, 1, 1, 10)
        report(table, 1, 1, 10)
        assert_record(table, 1, 1, 10, 10)

    def test_temperature_equal_to_min_after_range_established(self, table):
        report(table, 1, 1, 5)
        report(table, 1, 1, 15)
        report(table, 1, 1, 5)
        assert_record(table, 1, 1, 5, 15)

    def test_temperature_equal_to_max_after_range_established(self, table):
        report(table, 1, 1, 5)
        report(table, 1, 1, 15)
        report(table, 1, 1, 15)
        assert_record(table, 1, 1, 5, 15)

    def test_repeated_reports_do_not_increase_unique_count(self, table):
        for _ in range(50):
            report(table, 7, 8, 12)
        assert size(table) == 1
        assert_record(table, 7, 8, 12, 12)

    def test_sequence_of_updates_tracks_running_min_and_max(self, table):
        temps = [10, 3, 8, 15, -2, 15, 0, -2, 40, 39]
        for t in temps:
            report(table, 4, 4, t)
        assert size(table) == 1
        assert_record(table, 4, 4, min(temps), max(temps))

    def test_descending_sequence(self, table):
        for t in [5, 4, 3, 2, 1, 0, -1]:
            report(table, 0, 0, t)
        assert_record(table, 0, 0, -1, 5)

    def test_ascending_sequence(self, table):
        for t in [-1, 0, 1, 2, 3, 4, 5]:
            report(table, 0, 0, t)
        assert_record(table, 0, 0, -1, 5)

    def test_all_negative_temperatures(self, table):
        for t in [-5, -20, -1, -10]:
            report(table, 9, 9, t)
        assert_record(table, 9, 9, -20, -1)

    def test_negative_then_zero_then_positive(self, table):
        report(table, 1, 1, -3)
        report(table, 1, 1, 0)
        report(table, 1, 1, 3)
        assert_record(table, 1, 1, -3, 3)

    def test_zero_as_new_max_when_all_other_temps_negative(self, table):
        report(table, 1, 1, -3)
        report(table, 1, 1, 0)
        assert_record(table, 1, 1, -3, 0)

    def test_zero_as_new_min_when_all_other_temps_positive(self, table):
        report(table, 1, 1, 3)
        report(table, 1, 1, 0)
        assert_record(table, 1, 1, 0, 3)

    def test_float_temperatures(self, table):
        report(table, 1, 1, 10.25)
        report(table, 1, 1, 10.5)
        report(table, 1, 1, 10.125)
        assert_record(table, 1, 1, 10.125, 10.5)

    def test_mixed_int_and_float_temperatures(self, table):
        report(table, 1, 1, 10)
        report(table, 1, 1, 9.5)
        report(table, 1, 1, 10.5)
        assert_record(table, 1, 1, 9.5, 10.5)

    def test_updating_one_position_does_not_affect_others(self, table):
        report(table, 1, 1, 10)
        report(table, 2, 2, 20)
        report(table, 1, 1, -50)
        report(table, 1, 1, 90)
        assert_record(table, 1, 1, -50, 90)
        assert_record(table, 2, 2, 20, 20)
        assert size(table) == 2

    def test_interleaved_updates_across_positions(self, table):
        report(table, 1, 1, 5)
        report(table, 2, 2, 50)
        report(table, 1, 1, 1)
        report(table, 2, 2, 60)
        report(table, 1, 1, 9)
        report(table, 2, 2, 40)
        assert_record(table, 1, 1, 1, 9)
        assert_record(table, 2, 2, 40, 60)
        assert size(table) == 2

    def test_min_never_exceeds_max(self, table):
        rng = random.Random(1)
        for _ in range(200):
            report(table, 3, 3, rng.uniform(-100, 100))
            assert get_min(table, 3, 3) <= get_max(table, 3, 3)


# ---------------------------------------------------------------------------
# Rounding rule
# ---------------------------------------------------------------------------
class TestRounding:
    @pytest.mark.parametrize(
        "x, y",
        [
            (1.2, 2.2),
            (0.8, 1.8),
            (1.4, 2.4),
            (0.6, 1.6),
            (1.49, 2.49),
            (0.51, 1.51),
            (1.0, 2.0),
        ],
    )
    def test_coordinates_rounding_to_same_pair_share_a_record(self, table, x, y):
        report(table, 1, 2, 10)
        report(table, x, y, 20)
        assert size(table) == 1
        assert_record(table, 1, 2, 10, 20)

    def test_lookup_uses_rounded_coordinates(self, table):
        report(table, 1, 2, 10)
        assert get_min(table, 1.3, 1.7) == 10
        assert get_max(table, 0.9, 2.4) == 10

    def test_contains_uses_rounded_coordinates(self, table):
        report(table, 1, 2, 10)
        assert contains(table, 1.3, 1.7) is True
        assert contains(table, 0.8, 2.2) is True

    def test_report_with_unrounded_coordinates_found_via_whole_coordinates(self, table):
        report(table, 3.2, 4.4, 8)
        assert_record(table, 3, 4, 8, 8)

    @pytest.mark.parametrize(
        "x, y",
        [
            (2.0, 2.0),    # different integer pair
            (1.0, 3.0),
            (0.0, 2.0),
            (1.6, 2.0),    # x rounds to 2
            (1.0, 2.6),    # y rounds to 3
            (0.4, 1.6),    # x rounds to 0
        ],
    )
    def test_coordinates_rounding_to_different_pair_are_distinct(self, table, x, y):
        report(table, 1, 2, 10)
        report(table, x, y, 99)
        assert size(table) == 2
        assert_record(table, 1, 2, 10, 10)

    def test_small_positive_and_negative_fractions_round_to_origin(self, table):
        report(table, 0.4, 0.4, 10)
        report(table, -0.4, -0.4, 20)
        report(table, 0, 0, 5)
        report(table, 0.4, -0.4, 30)
        report(table, -0.4, 0.4, 1)
        assert size(table) == 1
        assert_record(table, 0, 0, 1, 30)

    def test_negative_zero_is_same_as_zero(self, table):
        report(table, -0.0, -0.0, 10)
        report(table, 0, 0, 20)
        assert size(table) == 1
        assert_record(table, 0, 0, 10, 20)

    def test_negative_coordinates_round_to_nearest(self, table):
        report(table, -2, -3, 10)
        report(table, -2.4, -3.4, 20)
        report(table, -1.6, -2.6, 5)
        assert size(table) == 1
        assert_record(table, -2, -3, 5, 20)

    def test_negative_fractions_near_boundary_stay_distinct_from_neighbor(self, table):
        report(table, -2, -2, 10)
        report(table, -2.6, -2.6, 20)  # rounds to (-3, -3)
        assert size(table) == 2
        assert_record(table, -2, -2, 10, 10)
        assert_record(table, -3, -3, 20, 20)

    def test_just_below_and_above_half_go_to_different_integers(self, table):
        report(table, 0.49, 0.49, 10)  # -> (0, 0)
        report(table, 0.51, 0.51, 20)  # -> (1, 1)
        assert size(table) == 2
        assert_record(table, 0, 0, 10, 10)
        assert_record(table, 1, 1, 20, 20)

    def test_integer_and_float_forms_of_same_value_match(self, table):
        report(table, 7, 7, 1)
        report(table, 7.0, 7.0, 2)
        assert size(table) == 1
        assert_record(table, 7, 7, 1, 2)

    def test_many_coordinates_collapse_to_one_record(self, table):
        offsets = [-0.45, -0.3, -0.1, 0.0, 0.1, 0.3, 0.45]
        for i, dx in enumerate(offsets):
            for j, dy in enumerate(offsets):
                report(table, 10 + dx, 20 + dy, i * 10 + j)
        assert size(table) == 1
        assert_record(table, 10, 20, 0, 66)

    def test_large_float_coordinates_round_consistently(self, table):
        report(table, 123456.4, -98765.4, 10)
        report(table, 123456.0, -98765.0, 20)
        assert size(table) == 1
        assert_record(table, 123456, -98765, 10, 20)

    # --- exact .5 ties: behavior ambiguous (A8), assert only consistency ---
    def test_exact_tie_is_deterministic_for_repeated_reports(self, table):
        report(table, 0.5, 0.5, 10)
        report(table, 0.5, 0.5, 20)
        assert size(table) == 1
        assert get_min(table, 0.5, 0.5) == 10
        assert get_max(table, 0.5, 0.5) == 20

    def test_exact_tie_maps_to_one_of_the_two_neighbouring_integers(self, table):
        report(table, 0.5, 0.5, 10)
        assert contains(table, 0, 0) or contains(table, 1, 1)

    def test_negative_exact_tie_is_deterministic(self, table):
        report(table, -2.5, -2.5, 10)
        report(table, -2.5, -2.5, -10)
        assert size(table) == 1
        assert_record(table, -2.5, -2.5, -10, 10)


# ---------------------------------------------------------------------------
# Missing positions
# ---------------------------------------------------------------------------
class TestMissingPositions:
    def test_get_min_missing_position_raises_key_error(self, table):
        report(table, 1, 1, 10)
        with pytest.raises(KeyError):
            get_min(table, 2, 2)

    def test_get_max_missing_position_raises_key_error(self, table):
        report(table, 1, 1, 10)
        with pytest.raises(KeyError):
            get_max(table, 2, 2)

    def test_contains_missing_position_is_false(self, table):
        report(table, 1, 1, 10)
        assert contains(table, 2, 2) is False

    def test_missing_lookup_does_not_change_size_or_existing_data(self, table):
        report(table, 1, 1, 10)
        for _ in range(3):
            with pytest.raises(KeyError):
                get_min(table, 9, 9)
            with pytest.raises(KeyError):
                get_max(table, 9, 9)
        assert size(table) == 1
        assert_record(table, 1, 1, 10, 10)

    def test_neighbouring_position_after_rounding_is_missing(self, table):
        report(table, 1, 1, 10)
        with pytest.raises(KeyError):
            get_min(table, 1.6, 1.0)  # rounds to (2, 1)

    def test_swapped_coordinates_are_missing(self, table):
        report(table, 1, 2, 10)
        assert contains(table, 2, 1) is False
        with pytest.raises(KeyError):
            get_max(table, 2, 1)

    def test_origin_missing_when_only_other_positions_exist(self, table):
        report(table, 1, 1, 10)
        assert contains(table, 0, 0) is False
        with pytest.raises(KeyError):
            get_min(table, 0, 0)

    def test_negated_position_is_missing(self, table):
        report(table, 5, 5, 10)
        assert contains(table, -5, -5) is False
        with pytest.raises(KeyError):
            get_min(table, -5, -5)

    def test_key_error_for_missing_position_after_lookups_of_present_ones(self, table):
        report(table, 1, 1, 10)
        assert get_min(table, 1, 1) == 10
        with pytest.raises(KeyError):
            get_min(table, 1, 2)


# ---------------------------------------------------------------------------
# Hash collisions
# ---------------------------------------------------------------------------
class TestCollisions:
    # Positions engineered to collide under naive hashes (x + y, x ^ y, x * y,
    # symmetric/commutative combos). They must always remain distinct records.
    SAME_SUM = [(1, 2), (2, 1), (3, 0), (0, 3), (-1, 4), (4, -1), (5, -2), (-2, 5)]
    SAME_PRODUCT = [(1, 12), (2, 6), (3, 4), (4, 3), (6, 2), (12, 1), (-3, -4), (-2, -6)]
    SAME_DIFFERENCE = [(5, 3), (6, 4), (7, 5), (8, 6), (0, -2), (-1, -3)]
    ZERO_AXES = [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0), (0, 100), (100, 0)]

    @pytest.mark.parametrize(
        "positions",
        [SAME_SUM, SAME_PRODUCT, SAME_DIFFERENCE, ZERO_AXES],
        ids=["same_sum", "same_product", "same_difference", "zero_axes"],
    )
    def test_similar_hash_positions_stay_distinct(self, table, positions):
        for i, (x, y) in enumerate(positions):
            report(table, x, y, i)
        assert size(table) == len(positions)
        for i, (x, y) in enumerate(positions):
            assert_record(table, x, y, i, i)

    @pytest.mark.parametrize(
        "positions",
        [SAME_SUM, SAME_PRODUCT, SAME_DIFFERENCE],
        ids=["same_sum", "same_product", "same_difference"],
    )
    def test_updates_to_colliding_positions_do_not_interfere(self, table, positions):
        for i, (x, y) in enumerate(positions):
            report(table, x, y, 100 + i)
        for i, (x, y) in enumerate(positions):
            report(table, x, y, -i)
            report(table, x, y, 1000 + i)
        assert size(table) == len(positions)
        for i, (x, y) in enumerate(positions):
            assert_record(table, x, y, -i, 1000 + i)

    def test_colliding_positions_all_found_when_queried_in_reverse_order(self, table):
        for i, (x, y) in enumerate(self.SAME_SUM):
            report(table, x, y, i)
        for i, (x, y) in reversed(list(enumerate(self.SAME_SUM))):
            assert_record(table, x, y, i, i)

    def test_missing_position_in_a_populated_colliding_neighbourhood(self, table):
        for i, (x, y) in enumerate(self.SAME_SUM):
            report(table, x, y, i)
        # Same sum (3) as the stored positions but never reported.
        assert contains(table, 6, -3) is False
        with pytest.raises(KeyError):
            get_min(table, 6, -3)

    def test_small_table_forces_collisions_by_pigeonhole(self):
        # With a tiny initial capacity and many positions, bucket sharing is
        # unavoidable before and during growth. All records must survive.
        t = make_table(capacity=2)
        n = 60
        for i in range(n):
            report(t, i, -i, i)
        assert size(t) == n
        for i in range(n):
            assert_record(t, i, -i, i, i)

    def test_grid_of_positions_all_retrievable(self, table):
        expected = {}
        for x in range(-12, 13):
            for y in range(-12, 13):
                temp = x * 100 + y
                report(table, x, y, temp)
                expected[(x, y)] = temp
        assert size(table) == len(expected) == 25 * 25
        for (x, y), temp in expected.items():
            assert_record(table, x, y, temp, temp)

    def test_removal_of_assumption_free_collision_with_rounded_duplicates(self, table):
        # Colliding positions mixed with rounded duplicates of those positions.
        for i, (x, y) in enumerate(self.SAME_SUM):
            report(table, x + 0.2, y - 0.2, i)       # rounds to (x, y)
        for i, (x, y) in enumerate(self.SAME_SUM):
            report(table, x, y, i + 50)
        assert size(table) == len(self.SAME_SUM)
        for i, (x, y) in enumerate(self.SAME_SUM):
            assert_record(table, x, y, i, i + 50)

    def test_colliding_positions_with_equal_temperatures(self, table):
        for x, y in self.SAME_SUM:
            report(table, x, y, 7)
        assert size(table) == len(self.SAME_SUM)
        for x, y in self.SAME_SUM:
            assert_record(table, x, y, 7, 7)

    def test_collision_with_zero_temperature_records(self, table):
        for x, y in self.SAME_SUM:
            report(table, x, y, 0)
        assert size(table) == len(self.SAME_SUM)
        for x, y in self.SAME_SUM:
            assert contains(table, x, y) is True
            assert_record(table, x, y, 0, 0)


# ---------------------------------------------------------------------------
# Unique-count tracking
# ---------------------------------------------------------------------------
class TestSize:
    def test_size_increments_only_for_new_positions(self, table):
        report(table, 1, 1, 1)
        assert size(table) == 1
        report(table, 1, 1, 2)
        assert size(table) == 1
        report(table, 2, 1, 2)
        assert size(table) == 2
        report(table, 2, 1, 3)
        assert size(table) == 2

    def test_size_ignores_rounded_duplicates(self, table):
        report(table, 1.1, 1.1, 1)
        report(table, 0.9, 0.9, 2)
        report(table, 1.4, 0.6, 3)
        assert size(table) == 1

    def test_size_after_many_mixed_operations(self, table):
        rng = random.Random(42)
        seen = set()
        for _ in range(500):
            x = rng.randint(-8, 8)
            y = rng.randint(-8, 8)
            report(table, x, y, rng.randint(-50, 50))
            seen.add((x, y))
            assert size(table) == len(seen)

    def test_size_is_not_affected_by_failed_lookups_or_contains(self, table):
        report(table, 1, 1, 1)
        contains(table, 5, 5)
        with pytest.raises(KeyError):
            get_min(table, 5, 5)
        assert size(table) == 1


# ---------------------------------------------------------------------------
# Resizing / rehashing
# ---------------------------------------------------------------------------
class TestResize:
    def test_load_factor_never_exceeds_limit_after_inserts(self):
        # Assumption A10: resize check happens after inserting a new position.
        t = make_table()
        for i in range(300):
            report(t, i, i * 3, i)
            assert size(t) / capacity_of(t) <= LOAD_FACTOR_LIMIT + 1e-9

    def test_capacity_grows_when_load_factor_exceeded(self):
        t = make_table()
        initial = capacity_of(t)
        for i in range(initial * 2):
            report(t, i, 0, i)
        assert capacity_of(t) > initial

    def test_capacity_never_decreases(self):
        t = make_table()
        previous = capacity_of(t)
        for i in range(400):
            report(t, i, -i, i)
            current = capacity_of(t)
            assert current >= previous
            previous = current

    def test_load_factor_exactly_at_limit_does_not_trigger_resize(self):
        # Assumption A9: "exceeds 0.7" means strictly greater.
        t = make_table(capacity=10)
        initial = capacity_of(t)
        assert initial == 10
        for i in range(7):  # 7 / 10 == 0.7 exactly
            report(t, i, 0, i)
        assert size(t) == 7
        assert capacity_of(t) == 10

    def test_one_record_past_limit_triggers_resize(self):
        t = make_table(capacity=10)
        if capacity_of(t) != 10:
            pytest.skip("Initial capacity not honoured as requested")
        for i in range(8):  # 8 / 10 == 0.8 > 0.7
            report(t, i, 0, i)
        assert capacity_of(t) > 10

    def test_updating_existing_positions_does_not_trigger_resize(self):
        t = make_table(capacity=10)
        if capacity_of(t) != 10:
            pytest.skip("Initial capacity not honoured as requested")
        for i in range(7):
            report(t, i, 0, i)
        for rep in range(100):
            for i in range(7):
                report(t, i, 0, 1000 + rep)  # updates only
        assert capacity_of(t) == 10
        assert size(t) == 7

    def test_rounded_duplicates_do_not_trigger_resize(self):
        t = make_table(capacity=10)
        if capacity_of(t) != 10:
            pytest.skip("Initial capacity not honoured as requested")
        for i in range(7):
            report(t, i, 0, i)
        for i in range(7):
            report(t, i + 0.3, 0.2, 99)  # same rounded positions
        assert capacity_of(t) == 10
        assert size(t) == 7

    def test_all_records_and_values_preserved_across_resize(self):
        t = make_table()
        initial = capacity_of(t)
        count = initial * 3
        expected = {}
        for i in range(count):
            lo, hi = -i, i * 2
            report(t, i, -i, lo)
            report(t, i, -i, hi)
            expected[(i, -i)] = (lo, hi)
        assert capacity_of(t) > initial
        assert size(t) == count
        for (x, y), (lo, hi) in expected.items():
            assert_record(t, x, y, lo, hi)

    def test_records_preserved_after_each_individual_insert(self):
        t = make_table()
        expected = {}
        for i in range(120):
            x, y, temp = i % 17, i // 17, i - 60
            report(t, x, y, temp)
            lo, hi = expected.get((x, y), (temp, temp))
            expected[(x, y)] = (min(lo, temp), max(hi, temp))
            assert size(t) == len(expected)
            for (ex, ey), (elo, ehi) in expected.items():
                assert_record(t, ex, ey, elo, ehi)

    def test_zero_and_negative_temperatures_preserved_across_resize(self):
        t = make_table()
        n = 150
        for i in range(n):
            report(t, i, i, 0 if i % 3 == 0 else -i)
        for i in range(n):
            expected = 0 if i % 3 == 0 else -i
            assert contains(t, i, i) is True
            assert_record(t, i, i, expected, expected)

    def test_updates_after_resize_work(self):
        t = make_table()
        n = 100
        for i in range(n):
            report(t, i, 0, 50)
        for i in range(n):
            report(t, i, 0, 10 + i)   # new min
            report(t, i, 0, 100 + i)  # new max
        assert size(t) == n
        for i in range(n):
            assert_record(t, i, 0, 10 + i if 10 + i < 50 else 50, 100 + i)

    def test_rounding_still_applies_after_resize(self):
        t = make_table()
        for i in range(100):
            report(t, i, i, i)
        assert get_min(t, 40.3, 39.8) == 40
        report(t, 40.3, 39.8, -5)
        assert size(t) == 100
        assert_record(t, 40, 40, -5, 40)

    def test_missing_positions_still_missing_after_resize(self):
        t = make_table()
        for i in range(100):
            report(t, i, 0, i)
        assert contains(t, 1000, 1000) is False
        assert contains(t, 0, 1) is False
        with pytest.raises(KeyError):
            get_min(t, 1000, 1000)
        with pytest.raises(KeyError):
            get_max(t, 0, 1)
        assert size(t) == 100

    def test_multiple_consecutive_resizes(self):
        t = make_table()
        n = 2000
        for i in range(n):
            report(t, i % 50, i // 50, i)
        assert size(t) == n
        assert size(t) / capacity_of(t) <= LOAD_FACTOR_LIMIT + 1e-9
        for i in range(n):
            assert_record(t, i % 50, i // 50, i, i)

    def test_resize_with_colliding_positions(self):
        t = make_table()
        # Many (x, y) pairs sharing the same x + y.
        s = 40
        positions = [(x, s - x) for x in range(-60, 101)]
        for i, (x, y) in enumerate(positions):
            report(t, x, y, i)
        assert size(t) == len(positions)
        for i, (x, y) in enumerate(positions):
            assert_record(t, x, y, i, i)

    def test_resize_from_tiny_capacity(self):
        t = make_table(capacity=1)
        for i in range(30):
            report(t, i, 2 * i, i)
        assert size(t) == 30
        for i in range(30):
            assert_record(t, i, 2 * i, i, i)

    def test_matches_reference_model_under_random_workload(self):
        rng = random.Random(2024)
        t = make_table()
        model = {}
        for _ in range(3000):
            # Offsets in (-0.4, 0.4) avoid exact .5 ties (A8).
            bx, by = rng.randint(-30, 30), rng.randint(-30, 30)
            x = bx + rng.uniform(-0.4, 0.4)
            y = by + rng.uniform(-0.4, 0.4)
            temp = rng.randint(-40, 45)
            report(t, x, y, temp)
            lo, hi = model.get((bx, by), (temp, temp))
            model[(bx, by)] = (min(lo, temp), max(hi, temp))
        assert size(t) == len(model)
        for (bx, by), (lo, hi) in model.items():
            assert_record(t, bx, by, lo, hi)


# ---------------------------------------------------------------------------
# Invalid inputs  (assumption A14: TypeError or ValueError)
# ---------------------------------------------------------------------------
class TestInvalidInputs:
    @pytest.mark.parametrize("bad", ["a", None, [1], {"x": 1}, (1, 2)])
    def test_report_rejects_non_numeric_x(self, table, bad):
        with pytest.raises((TypeError, ValueError)):
            report(table, bad, 1, 10)
        assert size(table) == 0

    @pytest.mark.parametrize("bad", ["a", None, [1], {"y": 1}, (1, 2)])
    def test_report_rejects_non_numeric_y(self, table, bad):
        with pytest.raises((TypeError, ValueError)):
            report(table, 1, bad, 10)
        assert size(table) == 0

    @pytest.mark.parametrize("bad", ["hot", None, [10], {"t": 1}])
    def test_report_rejects_non_numeric_temperature(self, table, bad):
        with pytest.raises((TypeError, ValueError)):
            report(table, 1, 1, bad)
        assert size(table) == 0
        assert contains(table, 1, 1) is False

    def test_invalid_temperature_does_not_corrupt_existing_record(self, table):
        report(table, 1, 1, 10)
        with pytest.raises((TypeError, ValueError)):
            report(table, 1, 1, "hot")
        assert_record(table, 1, 1, 10, 10)
        assert size(table) == 1

    @pytest.mark.parametrize("bad", ["a", None, [1]])
    def test_lookup_rejects_non_numeric_coordinates(self, table, bad):
        report(table, 1, 1, 10)
        with pytest.raises((TypeError, ValueError)):
            get_min(table, bad, 1)
        with pytest.raises((TypeError, ValueError)):
            get_max(table, 1, bad)


# ---------------------------------------------------------------------------
# Table independence
# ---------------------------------------------------------------------------
class TestInstanceIsolation:
    def test_two_tables_do_not_share_state(self):
        a = make_table()
        b = make_table()
        report(a, 1, 1, 10)
        assert size(a) == 1
        assert size(b) == 0
        assert contains(b, 1, 1) is False
        with pytest.raises(KeyError):
            get_min(b, 1, 1)

    def test_same_position_in_two_tables_tracked_separately(self):
        a = make_table()
        b = make_table()
        report(a, 1, 1, 10)
        report(b, 1, 1, -10)
        assert_record(a, 1, 1, 10, 10)
        assert_record(b, 1, 1, -10, -10)