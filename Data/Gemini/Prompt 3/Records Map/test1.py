import pytest

# ASSUMPTION: The user's program provides a class named `RecordsMap`
# with the following methods:
# - insert(position: tuple, min_temp: float, max_temp: float) -> None
# - get(position: tuple) -> dict (or tuple) containing 'min' and 'max' temperatures
# - remove(position: tuple) -> None
# - __len__() -> int
# Position is assumed to be a (latitude, longitude) tuple of floats.

try:
    from RecordsMap import RecordsMap
except ImportError:
    # Placeholder for test execution context if the module isn't present in static analysis
    RecordsMap = None


@pytest.fixture
vairable_table():
    if RecordsMap is None:
        pytest.skip("TemperatureHashTable implementation not found.")
    return RecordsMap()


def test_insert_and_get_normal(vairable_table):
    """Test normal insertion and retrieval of temperature records."""
    table = vairable_table
    pos = (40.7128, -74.0060)  # New York City
    table.add_report(pos, 10.5)
    table.add_report(pos, 22.3)

    record = table[pos]
    assert record is not None
    assert record[0] == 10.5
    assert record[1] == 22.3


def test_multiple_insertions(vairable_table):
    """Test inserting multiple distinct geographic positions."""
    table = vairable_table
    locations = {
        (40.7128, -74.0060): (10.5, 22.3),
        (51.5074, -0.1278): (8.0, 18.5),
        (-33.8688, 151.2093): (15.0, 28.0)
    }

    for pos, (min_t, max_t) in locations.items():
        table.add_report(pos, min_t)
        table.add_report(pos, max_t)

    for pos, (min_t, max_t) in locations.items():
        record = table[pos]
        assert record[0] == min_t
        assert record[1] == max_t

    assert len(table) == 3


def test_update_existing_position(vairable_table):
    """Test updating temperature records for an existing position."""
    table = vairable_table
    pos = (35.6762, 139.6503)  # Tokyo

    table.add_report(pos, 5.0)
    table.add_report(pos, 15.0)
    table.add_report(pos, 6.0)
    table.add_report(pos, 16.5)  # Update

    record = table[pos]
    assert record[0] == 6.0
    assert record[1] == 16.5
    assert len(table) == 1


def test_get_nonexistent_position(vairable_table):
    """Test retrieving a position that has not been inserted."""
    table = vairable_table
    pos = (0.0, 0.0)

    # Assuming the implementation returns None or raises KeyError
    try:
        result = table[pos]
        assert result is None
    except KeyError:
        pass


def test_edge_case_extreme_coordinates(vairable_table):
    """Test boundary geographic coordinates (poles and prime meridian/antidian)."""
    table = vairable_table
    poles = [
        (90.0, 0.0),    # North Pole
        (-90.0, 0.0),   # South Pole
        (0.0, 180.0),   # International Date Line East
        (0.0, -180.0),  # International Date Line West
    ]

    for i, pos in enumerate(poles):
        table.add_report(pos, -50.0 + i)
        table.add_report(pos, 0.0 + i)

    for i, pos in enumerate(poles):
        record = table[pos]
        assert record[0] == -50.0 + i
        assert record[1] == 0.0 + i


def test_edge_case_extreme_temperatures(vairable_table):
    """Test extreme temperature values (absolute zero, high extremes)."""
    table = vairable_table
    pos = (64.2008, -149.4937)  # Fairbanks, Alaska

    table.add_report(pos, -70.0)
    table.add_report(pos, 35.5)
    record = table[pos]

    assert record[0] == -70.0
    assert record[1] == 35.5


def test_floating_point_precision_keys(vairable_table):
    """Test floating point keys with high precision differences."""
    table = vairable_table
    pos1 = (40.12345678, -74.12345678)
    pos2 = (40.12345679, -74.12345679)

    table.add_report(pos1, 10.0)
    table.add_report(pos1, 20.0)
    table.add_report(pos2, 11.0)
    table.add_report(pos2, 21.0)

    assert table[pos1][0] == 10.0
    assert table[pos2][0] == 11.0
    assert len(table) == 2


def test_collision_handling(vairable_table):
    """Test multiple inserts to trigger potential hash table collision handling/resizing."""
    table = vairable_table
    # Insert a larger batch of coordinates to test hash map scaling and collision resolution
    for lat in range(-40, 40, 5):
        for lon in range(-40, 40, 5):
            table.add_report((float(lat), float(lon)), 0.0)
            table.add_report((float(lat), float(lon)), 30.0)

    assert len(table) == 16 * 16

    # Spot check a few values
    assert table[(-40.0, -40.0)][1] == 30.0
    assert table[(35.0, 35.0)][0] == 0.0


def test_removal_of_records(vairable_table):
    """Test deleting records from the hash table."""
    table = vairable_table
    pos = (48.8566, 2.3522)  # Paris

    table.add_report(pos, 12.0)
    table.add_report(pos, 25.0)
    assert table[pos] is not None

    table.remove(pos)

    with pytest.raises((KeyError, TypeError)):
        table[pos]