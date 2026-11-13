import pytest

# ==============================================================================
# EXPLICIT ASSUMPTIONS BASED ON PROGRAM DESCRIPTION:
# 1. The hash table class is named `TemperatureHashTable`.
# 2. Geographic positions are represented as (latitude, longitude) tuples of floats,
#    where latitude ranges from -90 to 90 and longitude from -180 to 180.
# 3. Temperature records consist of a minimum and maximum temperature (floats).
# 4. Methods assumed:
#    - `insert(position, min_temp, max_temp)`: stores or updates temperature records.
#    - `get(position)`: returns a tuple `(min_temp, max_temp)` or `None` if not found.
#    - `delete(position)`: removes the record for a given position.
# 5. Invalid inputs (such as min_temp > max_temp or out-of-range coordinates) 
#    are expected to raise an exception (e.g., ValueError, TypeError).
# ==============================================================================

try:
    from RecordsMap import RecordsMap
except ImportError:
    RecordsMap = None


@pytest.fixture
def hash_table():
    if RecordsMap is None:
        pytest.skip("TemperatureHashTable implementation not found.")
    return RecordsMap()


def test_normal_insertion_and_retrieval(hash_table):
    pos = (40.7128, -74.0060)  # New York City
    min_temp, max_temp = 12.5, 25.0

    hash_table.add_report(pos, min_temp, max_temp)
    result = hash_table[pos]

    assert result == (min_temp, max_temp)


def test_update_existing_position(hash_table):
    pos = (34.0522, -118.2437)  # Los Angeles
    hash_table.add_report(pos, 15.0, 30.0)

    # Update with new min/max temperatures for the same location
    hash_table.add_report(pos, 18.2, 32.5)
    result = hash_table[pos]

    assert result == (18.2, 32.5)


def test_get_non_existent_position(hash_table):
    pos = (0.0, 0.0)
    result = hash_table[pos]
    assert result is None or result == ()


@pytest.mark.parametrize("lat, lon", [
    (90.0, 0.0),    # North Pole
    (-90.0, 0.0),   # South Pole
    (0.0, 180.0),   # International Date Line East
    (0.0, -180.0),  # International Date Line West
    (0.0, 0.0),     # Null Island
])
def test_boundary_geographic_positions(hash_table, lat, lon):
    pos = (lat, lon)
    hash_table.add_report(pos, -10.0, 10.0)
    assert hash_table[pos] == (-10.0, 10.0)


def test_boundary_temperatures(hash_table):
    pos = (51.5074, -0.1278)  # London
    # Absolute zero and high atmospheric temperature extremes
    min_temp, max_temp = -273.15, 60.0
    hash_table.add_report(pos, min_temp, max_temp)
    assert hash_table[pos] == (min_temp, max_temp)


def test_invalid_temperature_range(hash_table):
    pos = (48.8566, 2.3522)  # Paris
    # Minimum temperature cannot exceed maximum temperature
    with pytest.raises((ValueError, KeyError)):
        hash_table.add_report(pos, 30.0, 10.0)


def test_deletion(hash_table):
    pos = (35.6762, 139.6503)  # Tokyo
    hash_table.add_report(pos, 5.0, 15.0)

    if hasattr(hash_table, 'delete'):
        hash_table.delete(pos)
        assert hash_table[pos] is None


@pytest.mark.parametrize("invalid_pos", [
    ("invalid_lat", "invalid_lon"),  # Non-numeric types
    (95.0, 0.0),                     # Latitude > 90
    (-95.0, 0.0),                    # Latitude < -90
    (0.0, 190.0),                    # Longitude > 180
    (0.0, -190.0),                   # Longitude < -180
    (40.7128,),                      # Malformed coordinate tuple
])
def test_invalid_geographic_positions(hash_table, invalid_pos):
    with pytest.raises((ValueError, TypeError, KeyError, IndexError)):
        hash_table.add_report(invalid_pos, 10.0, 20.0)