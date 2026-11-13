
import pytest
from unittest.mock import patch
import math

# Replace "your_module" with the name of the Python file containing the program.
from basic_counting import generate_lists, find_common, find_common_efficient, measure_time


# -------------------------
# Tests for generate_lists
# -------------------------

def test_generate_lists_normal_size():
    list1, list2 = generate_lists(10)

    assert len(list1) == 10
    assert len(list2) == 10
    assert len(set(list1)) == 10
    assert len(set(list2)) == 10
    assert all(0 <= x < 20 for x in list1)
    assert all(0 <= x < 20 for x in list2)


def test_generate_lists_size_one():
    list1, list2 = generate_lists(1)

    assert len(list1) == 1
    assert len(list2) == 1
    assert 0 <= list1[0] < 2
    assert 0 <= list2[0] < 2


def test_generate_lists_zero_size():
    list1, list2 = generate_lists(0)

    assert list1 == []
    assert list2 == []


def test_generate_lists_negative_size():
    with pytest.raises(ValueError):
        generate_lists(-1)


@pytest.mark.parametrize("size", [1.5, "5", None, [], {}])
def test_generate_lists_invalid_size_types(size):
    with pytest.raises((TypeError, ValueError)):
        generate_lists(size)


def test_generate_lists_full_range_size():
    size = 100
    list1, list2 = generate_lists(size)

    assert len(list1) == size
    assert len(list2) == size
    assert len(set(list1)) == size
    assert len(set(list2)) == size
    assert set(list1).issubset(set(range(size * 2)))
    assert set(list2).issubset(set(range(size * 2)))


# -------------------------
# Tests for find_common
# -------------------------

@pytest.mark.parametrize(
    "list1, list2, expected",
    [
        ([], [], 0),
        ([1], [1], 1),
        ([1], [2], 0),
        ([1, 2, 3], [3, 4, 5], 1),
        ([1, 2, 3], [4, 5, 6], 0),
        ([1, 2, 3], [1, 2, 3], 3),
        ([0, -1, -2], [-2, 0, 5], 2),
        ([1, 1, 2], [1, 1, 2], 5),
        ([1, 1, 1], [1], 3),
        ([1], [1, 1, 1], 3),
        ([1, 2, 3], [], 0),
        ([], [1, 2, 3], 0),
        ([1.0, 2.5], [2.5, 3.5], 1),
        (["a", "b"], ["b", "c"], 1),
        ([True, False], [1, 0], 2),
    ],
)
def test_find_common_cases(list1, list2, expected):
    assert find_common(list1, list2) == expected


def test_find_common_duplicate_counts():
    # Each matching pair contributes to the result.
    assert find_common([1, 1, 1], [1, 1]) == 6


def test_find_common_large_lists():
    list1 = list(range(500))
    list2 = list(range(250, 750))

    assert find_common(list1, list2) == 250


def test_find_common_does_not_modify_inputs():
    list1 = [1, 2, 2, 3]
    list2 = [2, 2, 4]
    original1 = list1.copy()
    original2 = list2.copy()

    find_common(list1, list2)

    assert list1 == original1
    assert list2 == original2


@pytest.mark.parametrize(
    "list1, list2",
    [
        (None, [1, 2]),
        ([1, 2], None),
        (None, None),
        (5, [1, 2]),
        ([1, 2], 5),
    ],
)
def test_find_common_invalid_inputs(list1, list2):
    with pytest.raises(TypeError):
        find_common(list1, list2)


# -------------------------
# Tests for find_common_efficient
# -------------------------

@pytest.mark.parametrize(
    "list1, list2, expected",
    [
        ([], [], 0),
        ([1], [1], 1),
        ([1], [2], 0),
        ([1, 2, 3], [3, 4, 5], 1),
        ([1, 2, 3], [4, 5, 6], 0),
        ([1, 2, 3], [1, 2, 3], 3),
        ([0, -1, -2], [-2, 0, 5], 2),
        ([1, 1, 2], [1, 1, 2], 2),
        ([1, 1, 1], [1], 1),
        ([1], [1, 1, 1], 1),
        ([1, 2, 3], [], 0),
        ([], [1, 2, 3], 0),
        ([1.0, 2.5], [2.5, 3.5], 1),
        (["a", "b"], ["b", "c"], 1),
        ([True, False], [1, 0], 2),
    ],
)
def test_find_common_efficient_cases(list1, list2, expected):
    assert find_common_efficient(list1, list2) == expected


def test_find_common_efficient_duplicate_counts():
    # Set intersection counts distinct common values, not matching pairs.
    assert find_common_efficient([1, 1, 1], [1, 1]) == 1


def test_find_common_efficient_large_lists():
    list1 = list(range(5000))
    list2 = list(range(2500, 7500))

    assert find_common_efficient(list1, list2) == 2500


def test_find_common_efficient_does_not_modify_inputs():
    list1 = [1, 2, 2, 3]
    list2 = [2, 2, 4]
    original1 = list1.copy()
    original2 = list2.copy()

    find_common_efficient(list1, list2)

    assert list1 == original1
    assert list2 == original2


@pytest.mark.parametrize(
    "list1, list2",
    [
        (None, [1, 2]),
        ([1, 2], None),
        (None, None),
        (5, [1, 2]),
        ([1, 2], 5),
    ],
)
def test_find_common_efficient_invalid_inputs(list1, list2):
    with pytest.raises(TypeError):
        find_common_efficient(list1, list2)


def test_find_common_efficient_unhashable_elements():
    with pytest.raises(TypeError):
        find_common_efficient([[1], [2]], [[2], [3]])


# -------------------------
# Cross-check both algorithms
# -------------------------

@pytest.mark.parametrize(
    "list1, list2",
    [
        ([], []),
        ([1, 2, 3], [2, 3, 4]),
        ([1, 1, 2], [1, 2, 2]),
        ([5, 6, 7], [8, 9, 10]),
    ],
)
def test_algorithms_agree_when_inputs_have_no_duplicates(list1, list2):
    assert find_common(list1, list2) == find_common_efficient(list1, list2)


# -------------------------
# Tests for measure_time
# -------------------------

def test_measure_time_prints_header_and_results(capsys):
    measure_time()

    output = capsys.readouterr().out

    assert "List Size" in output
    assert "find_common Time (s)" in output
    assert "find_common_efficiet Time (s)" in output

    for size in [10, 100, 1000, 10000]:
        assert str(size) in output


def test_measure_time_calls_generate_lists_for_each_size():
    with patch("basic_counting.generate_lists", return_value=([1], [1])) as mock_generate, \
         patch("basic_counting.find_common", return_value=1), \
         patch("basic_counting.find_common_efficient", return_value=1):

        measure_time()

        assert mock_generate.call_count == 4
        mock_generate.assert_any_call(10)
        mock_generate.assert_any_call(100)
        mock_generate.assert_any_call(1000)
        mock_generate.assert_any_call(10000)


def test_measure_time_calls_both_algorithms():
    with patch("basic_counting.generate_lists", return_value=([1], [1])), \
         patch("basic_counting.find_common") as mock_basic, \
         patch("basic_counting.find_common_efficient") as mock_efficient:

        measure_time()

        assert mock_basic.call_count == 4
        assert mock_efficient.call_count == 4


def test_measure_time_handles_empty_generated_lists():
    with patch("basic_counting.generate_lists", return_value=([], [])):
        measure_time()


# -------------------------
# Additional edge-case tests
# -------------------------

def test_find_common_with_mixed_numeric_types():
    assert find_common([1, 2.0, 3], [1.0, 2, 4]) == 2
    assert find_common_efficient([1, 2.0, 3], [1.0, 2, 4]) == 2


def test_find_common_with_none_elements():
    assert find_common([None, 1], [None, 2]) == 1
    assert find_common_efficient([None, 1], [None, 2]) == 1


def test_find_common_with_nan_values():
    nan1 = float("nan")
    nan2 = float("nan")

    assert find_common([nan1], [nan2]) == 0
    assert find_common_efficient([nan1], [nan2]) == 0


def test_find_common_with_infinity():
    assert find_common([float("inf"), float("-inf")], [float("inf")]) == 1
    assert find_common_efficient([float("inf"), float("-inf")], [float("inf")]) == 1
