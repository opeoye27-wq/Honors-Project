import pytest

# ==============================================================================
# EXPLICIT ASSUMPTIONS ABOUT THE PROGRAM'S API:
# Since the exact class and method names were not provided in the description, 
# these unit tests assume a class named `TemperatureHashTable` with the following 
# interface:
# 
# 1. Constructor: 
#    - TemperatureHashTable()
# 2. Methods:
#    - insert(latitude: float, longitude: float, min_temp: float, max_temp) -> None
#    - get(latitude: float, longitude: float) -> dict (returns {"min": float, "max": float})
#    - delete(latitude: float, longitude: float) -> None
# 
# Geographic coordinate bounds assumed:
# - Latitude: -90.0 to 90.0
# - Longitude: -180.0 to 180.0
# ==============================================================================

# Attempting to import the implementation (assumed to be named 'temperature_table.py')
try:
    from RecordsMap import RecordsMap
except ImportError:
    # Placeholder stub so the test structure is fully valid syntactically for static analysis
    RecordsMap = None


@pytest.fixture
def table():
    if RecordsMap is None:
        pytest.skip("TemperatureHashTable implementation not found.")
    return RecordsMap()


def test_insert_and_get_normal(table):
    """Test normal insertion and retrieval of temperature records."""
    table.add_report((34.0522, -118.2437), 15.5)
    table.add_report((34.0522, -118.2437), 32.1)
    record = table[(34.0522, -118.2437)]

    assert record is not None
    assert record[0] == 15.5
    assert record[1] == 32.1


def test_update_existing_record(table):
    """Test updating temperature records for an already stored geographic position."""
    table.add_report((40.7128, -74.0060), 10.0)
    table.add_report((40.7128, -74.0060), 25.0)
    # Update with new values
    table.add_report((40.7128, -74.0060), 12.0)
    table.add_report((40.7128, -74.0060), 28.5)

    record = table[(40.7128, -74.0060)]
    assert record[0] == 12.0
    assert record[1] == 28.5


def test_boundary_coordinates(table):
    """Test boundary conditions for valid geographic coordinates (poles, equator, prime meridian)."""
    # North Pole
    table.add_report((90.0, 0.0), -45.0)
    table.add_report((90.0, 0.0), -10.0)
    # South Pole
    table.add_report((-90.0, 0.0), -60.0)
    table.add_report((-90.0, 0.0), -20.0)
    # Equator & Prime Meridian intersection
    table.add_report((0.0, 0.0), 22.0)
    table.add_report((0.0, 0.0), 35.0)
    # International Date Line limit
    table.add_report((0.0, 180.0), 20.0)
    table.add_report((0.0, 180.0), 30.0)
    table.add_report((0.0, -180.0), 20.0)
    table.add_report((0.0, -180.0), 30.0)

    assert table[(90.0, 0.0)] == {"min": -45.0, "max": -10.0}
    assert table[(-90.0, 0.0)] == {"min": -60.0, "max": -20.0}
    assert table[(0.0, 0.0)] == {"min": 22.0, "max": 35.0}
    assert table[(0.0, 180.0)] == {"min": 20.0, "max": 30.0}
    assert table[(0.0, -180.0)] == {"min": 20.0, "max": 30.0}


def test_extreme_temperatures(table):
    """Test extreme temperature values (record highs, lows, and absolute zero context)."""
    # Absolute lowest theoretical temperature / extreme highs
    table.add_report((51.5074, -0.1278), -273.15)
    table.add_report((51.5074, -0.1278), 56.7)
    record = table[(51.5074, -0.1278)]

    assert record[0] == -273.15
    assert record[1] == 56.7


def test_get_nonexistent_location(table):
    """Test retrieving a geographic position that has not been inserted."""
    # Depending on implementation, this should either return None, raise KeyError, or raise ValueError
    with pytest.raises((KeyError, ValueError)):
        table[(45.0, 45.0)]


def test_invalid_latitude_out_of_bounds(table):
    """Test handling of invalid latitude values exceeding [-90, 90]."""
    with pytest.raises(ValueError):
        table.add_report((91.0, 0.0), 10.0)
        table.add_report((91.0, 0.0), 20.0)

    with pytest.raises(ValueError):
        table.add_report((-91.0, 0.0), 10.0)
        table.add_report((-91.0, 0.0), 20.0)


def test_invalid_longitude_out_of_bounds(table):
    """Test handling of invalid longitude values exceeding [-180, 180]."""
    with pytest.raises(ValueError):
        table.add_report((0.0, 181.0), 10.0)
        table.add_report((0.0, 181.0), 20.0)

    with pytest.raises(ValueError):
        table.add_report((0.0, -181.0), 10.0)
        table.add_report((0.0, -181.0), 20.0)


def test_invalid_temperature_range(table):
    """Test invalid temperature inputs where minimum temperature exceeds maximum temperature."""
    with pytest.raises(ValueError):
        table.add_report((10.0, 10.0), 30.0)
        table.add_report((10.0, 10.0), 20.0)  # min > max


def test_unusual_input_types(table):
    """Test handling of unexpected or invalid data types for coordinates and temperatures."""
    with pytest.raises((TypeError, ValueError)):
        table.add_report(("invalid_lat", "invalid_lon"), "hot")
        table.add_report(("invalid_lat", "invalid_lon"), "cold")


def test_hash_collision_handling(table):
    """Test inserting multiple locations that might induce hash collisions (if internal bucket size is small)."""
    # Inserting multiple points to test resilience under heavy load/collisions
    for i in range(-80, 80, 10):
        table.add_report((float(i), float(i)), float(i))
        table.add_report((float(i), float(i)), float(i + 5))

    # Verify records can still be accurately retrieved after potential collisions
    for i in range(-80, 80, 10):
        record = table[(float(i), float(i))]
        assert record[0] == float(i)
        assert record[1] == float(i + 5)