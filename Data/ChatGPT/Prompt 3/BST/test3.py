import pytest
from BST import BSTSet


@pytest.fixture
def bst():
    return BSTSet()


# -------------------------
# Insertion Tests
# -------------------------

def test_insert_single_key(bst):
    bst.put(10)
    assert bst.in_order() == [10]


def test_insert_multiple_keys(bst):
    for key in [10, 5, 15, 3, 7, 12, 18]:
        bst.put(key)

    assert bst.in_order() == [3, 5, 7, 10, 12, 15, 18]


def test_insert_sorted_keys(bst):
    for key in [1, 2, 3, 4, 5]:
        bst.put(key)

    assert bst.in_order() == [1, 2, 3, 4, 5]


def test_insert_reverse_sorted_keys(bst):
    for key in [5, 4, 3, 2, 1]:
        bst.put(key)

    assert bst.in_order() == [1, 2, 3, 4, 5]


def test_insert_negative_keys(bst):
    for key in [-10, -5, -15, -2]:
        bst.put(key)

    assert bst.in_order() == [-15, -10, -5, -2]


def test_insert_zero(bst):
    bst.put(0)
    assert bst.in_order() == [0]


def test_insert_mixed_positive_and_negative(bst):
    for key in [0, -10, 10, -5, 5]:
        bst.put(key)

    assert bst.in_order() == [-10, -5, 0, 5, 10]


# -------------------------
# Duplicate Insertion Tests
# -------------------------

def test_insert_duplicate_key(bst):
    bst.put(10)
    bst.put(10)

    assert bst.in_order() == [10]


def test_insert_multiple_duplicates(bst):
    for key in [10, 5, 15, 10, 5, 15, 10]:
        bst.put(key)

    assert bst.in_order() == [5, 10, 15]


def test_insert_duplicate_does_not_change_traversals(bst):
    for key in [10, 5, 15]:
        bst.put(key)

    original = (
        bst.in_order(),
        bst.pre_order(),
        bst.post_order()
    )

    bst.put(10)
    bst.put(5)
    bst.put(15)

    assert (
        bst.in_order(),
        bst.pre_order(),
        bst.post_order()
    ) == original


# -------------------------
# Traversal Tests
# -------------------------

def test_empty_tree_traversals(bst):
    assert bst.in_order() == []
    assert bst.pre_order() == []
    assert bst.post_order() == []


def test_single_node_traversals(bst):
    bst.put(42)

    assert bst.in_order() == [42]
    assert bst.pre_order() == [42]
    assert bst.post_order() == [42]


def test_balanced_tree_traversals(bst):
    for key in [4, 2, 6, 1, 3, 5, 7]:
        bst.put(key)

    assert bst.in_order() == [1, 2, 3, 4, 5, 6, 7]
    assert bst.pre_order() == [4, 2, 1, 3, 6, 5, 7]
    assert bst.post_order() == [1, 3, 2, 5, 7, 6, 4]


def test_left_skewed_tree_traversals(bst):
    for key in [5, 4, 3, 2, 1]:
        bst.put(key)

    assert bst.in_order() == [1, 2, 3, 4, 5]
    assert bst.pre_order() == [5, 4, 3, 2, 1]
    assert bst.post_order() == [1, 2, 3, 4, 5]


def test_right_skewed_tree_traversals(bst):
    for key in [1, 2, 3, 4, 5]:
        bst.put(key)

    assert bst.in_order() == [1, 2, 3, 4, 5]
    assert bst.pre_order() == [1, 2, 3, 4, 5]
    assert bst.post_order() == [5, 4, 3, 2, 1]


def test_traversals_visit_each_unique_key_once(bst):
    keys = [8, 3, 10, 1, 6, 14, 4, 7, 13]

    for key in keys:
        bst.put(key)

    expected = sorted(set(keys))

    assert sorted(bst.in_order()) == expected
    assert sorted(bst.pre_order()) == expected
    assert sorted(bst.post_order()) == expected


# -------------------------
# Boundary and Unusual Inputs
# -------------------------

def test_insert_large_integer(bst):
    bst.put(10**100)

    assert bst.in_order() == [10**100]


def test_insert_very_small_integer(bst):
    bst.put(-(10**100))

    assert bst.in_order() == [-(10**100)]


def test_insert_repeated_zero(bst):
    for _ in range(10):
        bst.put(0)

    assert bst.in_order() == [0]


def test_insert_float_keys(bst):
    for key in [3.5, 1.2, 5.7, 2.8]:
        bst.put(key)

    assert bst.in_order() == [1.2, 2.8, 3.5, 5.7]


def test_insert_mixed_integer_and_float_keys(bst):
    for key in [3, 1.5, 2, 4.5]:
        bst.put(key)

    assert bst.in_order() == [1.5, 2, 3, 4.5]


def test_insert_string_keys(bst):
    for key in ["banana", "apple", "cherry"]:
        bst.put(key)

    assert bst.in_order() == ["apple", "banana", "cherry"]


# -------------------------
# Invalid Input Tests
# -------------------------

@pytest.mark.parametrize("invalid_key", [None, [], {}, set()])
def test_insert_unorderable_keys(bst, invalid_key):
    # Assumption: Keys must be mutually orderable.
    # Invalid keys should raise TypeError.
    with pytest.raises(TypeError):
        bst.put(invalid_key)


def test_insert_incompatible_key_types(bst):
    # Assumption: Incompatible types cannot be compared.
    bst.put(10)

    with pytest.raises(TypeError):
        bst.put("hello")


def test_insert_nan(bst):
    # NaN does not behave like an ordinary ordered numeric key.
    # Expected behavior is intentionally unspecified by the description.
    # This test checks that insertion does not crash.
    bst.put(float("nan"))


# -------------------------
# Tree Independence Tests
# -------------------------

def test_multiple_trees_are_independent():
    tree1 = BSTSet()
    tree2 = BSTSet()

    tree1.put(10)
    tree1.put(5)

    tree2.put(20)
    tree2.put(15)

    assert tree1.in_order() == [5, 10]
    assert tree2.in_order() == [15, 20]


def test_repeated_traversals_do_not_modify_tree(bst):
    for key in [10, 5, 15, 3, 7]:
        bst.put(key)

    expected = [3, 5, 7, 10, 15]

    for _ in range(5):
        assert bst.in_order() == expected

    assert bst.in_order() == expected


def test_insert_after_traversal(bst):
    for key in [10, 5, 15]:
        bst.put(key)

    bst.in_order()
    bst.pre_order()
    bst.post_order()

    bst.put(12)

    assert bst.in_order() == [5, 10, 12, 15]


# -------------------------
# Larger Input Tests
# -------------------------

def test_insert_many_keys(bst):
    keys = list(range(100))

    for key in keys:
        bst.put(key)

    assert bst.in_order() == keys


def test_insert_many_keys_in_random_order(bst):
    keys = [50, 25, 75, 10, 40, 60, 90, 5, 15, 35, 45]

    for key in keys:
        bst.put(key)

    assert bst.in_order() == sorted(keys)


def test_large_number_of_duplicate_insertions(bst):
    for _ in range(1000):
        bst.put(42)

    assert bst.in_order() == [42]