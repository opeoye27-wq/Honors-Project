import pytest
from BST import BSTSet


@pytest.fixture
def bst():
    return BSTSet()


def test_insert_single_key(bst):
    bst.put(10)
    assert bst.in_order() == [10]


def test_insert_multiple_keys(bst):
    for key in [10, 5, 15, 3, 7, 12, 18]:
        bst.put(key)
    assert bst.in_order() == [3, 5, 7, 10, 12, 15, 18]


def test_insert_keys_in_ascending_order(bst):
    for key in [1, 2, 3, 4, 5]:
        bst.put(key)
    assert bst.in_order() == [1, 2, 3, 4, 5]


def test_insert_keys_in_descending_order(bst):
    for key in [5, 4, 3, 2, 1]:
        bst.put(key)
    assert bst.in_order() == [1, 2, 3, 4, 5]


def test_insert_duplicate_key(bst):
    bst.put(10)
    bst.put(10)
    assert bst.in_order() == [10]


def test_insert_multiple_duplicates(bst):
    for key in [5, 3, 7, 5, 3, 7, 5]:
        bst.put(key)
    assert bst.in_order() == [3, 5, 7]


def test_insert_negative_keys(bst):
    for key in [-10, -5, -15, 0, 5]:
        bst.put(key)
    assert bst.in_order() == [-15, -10, -5, 0, 5]


def test_insert_zero(bst):
    bst.put(0)
    assert bst.in_order() == [0]


def test_insert_large_integer_keys(bst):
    keys = [10**100, -(10**100), 0]
    for key in keys:
        bst.put(key)
    assert bst.in_order() == [-(10**100), 0, 10**100]


def test_inorder_traversal(bst):
    for key in [8, 4, 12, 2, 6, 10, 14]:
        bst.put(key)
    assert bst.in_order() == [2, 4, 6, 8, 10, 12, 14]


def test_preorder_traversal(bst):
    for key in [8, 4, 12, 2, 6, 10, 14]:
        bst.put(key)
    assert bst.pre_order() == [8, 4, 2, 6, 12, 10, 14]


def test_postorder_traversal(bst):
    for key in [8, 4, 12, 2, 6, 10, 14]:
        bst.put(key)
    assert bst.post_order() == [2, 6, 4, 10, 14, 12, 8]


def test_traversals_on_single_node(bst):
    bst.put(42)
    assert bst.in_order() == [42]
    assert bst.pre_order() == [42]
    assert bst.post_order() == [42]


def test_traversals_on_empty_tree(bst):
    assert bst.in_order() == []
    assert bst.pre_order() == []
    assert bst.post_order() == []


def test_traversals_after_multiple_insertions(bst):
    for key in [20, 10, 30, 5, 15]:
        bst.put(key)

    assert bst.in_order() == [5, 10, 15, 20, 30]
    assert bst.pre_order() == [20, 10, 5, 15, 30]
    assert bst.post_order() == [5, 15, 10, 30, 20]


def test_traversals_do_not_modify_tree(bst):
    for key in [10, 5, 15, 3, 7]:
        bst.put(key)

    expected = [3, 5, 7, 10, 15]

    bst.pre_order()
    bst.post_order()
    bst.in_order()

    assert bst.in_order() == expected


def test_insert_after_traversal(bst):
    bst.put(10)
    bst.in_order()
    bst.put(5)
    bst.pre_order()
    bst.put(15)

    assert bst.in_order() == [5, 10, 15]


def test_insert_same_key_repeatedly(bst):
    for _ in range(100):
        bst.put(7)
    assert bst.in_order() == [7]


def test_insert_many_unique_keys(bst):
    keys = list(range(1000))
    for key in keys:
        bst.put(key)

    assert bst.in_order() == keys
    assert len(bst.in_order()) == len(set(keys))


def test_insert_mixed_integer_values(bst):
    keys = [0, -1, 1, -100, 100, -50, 50]
    for key in keys:
        bst.put(key)

    assert bst.in_order() == [-100, -50, -1, 0, 1, 50, 100]


def test_traversals_contain_all_unique_keys(bst):
    keys = [15, 10, 20, 8, 12, 17, 25, 10, 20]

    for key in keys:
        bst.put(key)

    expected = sorted(set(keys))

    assert sorted(bst.in_order()) == expected
    assert sorted(bst.pre_order()) == expected
    assert sorted(bst.post_order()) == expected


def test_traversal_lengths_match_unique_key_count(bst):
    keys = [10, 5, 15, 5, 10, 20]

    for key in keys:
        bst.put(key)

    expected_length = len(set(keys))

    assert len(bst.in_order()) == expected_length
    assert len(bst.pre_order()) == expected_length
    assert len(bst.post_order()) == expected_length


def test_insert_float_keys_if_supported(bst):
    # Assumption: The tree accepts comparable numeric keys,
    # not exclusively integers.
    for key in [2.5, 1.5, 3.5]:
        bst.put(key)

    assert bst.in_order() == [1.5, 2.5, 3.5]


def test_insert_string_keys_if_supported(bst):
    # Assumption: The tree supports mutually comparable strings.
    for key in ["banana", "apple", "cherry"]:
        bst.put(key)

    assert bst.in_order() == ["apple", "banana", "cherry"]


def test_insert_none_rejected_if_unsupported(bst):
    # Assumption: None is not a valid key.
    with pytest.raises((TypeError, ValueError)):
        bst.put(None)


def test_insert_incomparable_key_rejected(bst):
    # Assumption: Keys must be mutually comparable.
    bst.put(10)

    with pytest.raises((TypeError, ValueError)):
        bst.put("ten")


def test_tree_remains_valid_after_rejected_input(bst):
    bst.put(10)
    bst.put(5)

    try:
        bst.put("invalid")
    except (TypeError, ValueError):
        pass

    assert bst.in_order() == [5, 10]