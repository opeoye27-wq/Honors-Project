import pytest
from BST import BSTSet


@pytest.fixture
def bst():
    return BSTSet()


def test_empty_tree_traversals(bst):
    assert bst.in_order() == []
    assert bst.pre_order() == []
    assert bst.post_order() == []


def test_insert_single_key(bst):
    bst.put(10)

    assert bst.in_order() == [10]
    assert bst.pre_order() == [10]
    assert bst.post_order() == [10]


def test_insert_multiple_keys(bst):
    for key in [50, 30, 70, 20, 40, 60, 80]:
        bst.put(key)

    assert bst.in_order() == [20, 30, 40, 50, 60, 70, 80]
    assert bst.pre_order() == [50, 30, 20, 40, 70, 60, 80]
    assert bst.post_order() == [20, 40, 30, 60, 80, 70, 50]


def test_inorder_returns_sorted_keys(bst):
    keys = [45, 15, 75, 10, 25, 60, 90, 20]

    for key in keys:
        bst.put(key)

    result = bst.in_order()

    assert result == sorted(keys)
    assert all(result[i] <= result[i + 1] for i in range(len(result) - 1))


def test_preorder_traversal(bst):
    for key in [40, 20, 60, 10, 30, 50, 70]:
        bst.put(key)

    assert bst.pre_order() == [40, 20, 10, 30, 60, 50, 70]


def test_postorder_traversal(bst):
    for key in [40, 20, 60, 10, 30, 50, 70]:
        bst.put(key)

    assert bst.post_order() == [10, 30, 20, 50, 70, 60, 40]


def test_duplicate_insertion(bst):
    bst.put(25)
    bst.put(25)
    bst.put(25)

    assert bst.in_order() == [25]


def test_duplicate_insertion_does_not_change_traversals(bst):
    for key in [50, 30, 70]:
        bst.put(key)

    original = (
        bst.in_order(),
        bst.pre_order(),
        bst.post_order()
    )

    bst.put(30)
    bst.put(50)
    bst.put(70)

    assert bst.in_order() == original[0]
    assert bst.pre_order() == original[1]
    assert bst.post_order() == original[2]


def test_insert_ascending_order(bst):
    for key in range(1, 11):
        bst.put(key)

    assert bst.in_order() == list(range(1, 11))


def test_insert_descending_order(bst):
    for key in range(10, 0, -1):
        bst.put(key)

    assert bst.in_order() == list(range(1, 11))


def test_left_skewed_tree(bst):
    for key in [50, 40, 30, 20, 10]:
        bst.put(key)

    assert bst.in_order() == [10, 20, 30, 40, 50]
    assert bst.pre_order() == [50, 40, 30, 20, 10]
    assert bst.post_order() == [10, 20, 30, 40, 50]


def test_right_skewed_tree(bst):
    for key in [10, 20, 30, 40, 50]:
        bst.put(key)

    assert bst.in_order() == [10, 20, 30, 40, 50]
    assert bst.pre_order() == [10, 20, 30, 40, 50]
    assert bst.post_order() == [50, 40, 30, 20, 10]


def test_negative_keys(bst):
    for key in [-10, -30, -5, -20, 0]:
        bst.put(key)

    assert bst.in_order() == [-30, -20, -10, -5, 0]


def test_zero_key(bst):
    bst.put(0)

    assert bst.in_order() == [0]


def test_mixed_positive_and_negative_keys(bst):
    keys = [-100, 50, -50, 0, 100, -1, 1]

    for key in keys:
        bst.put(key)

    assert bst.in_order() == sorted(keys)


def test_large_integer_keys(bst):
    keys = [10**100, -(10**100), 0, 10**50, -(10**50)]

    for key in keys:
        bst.put(key)

    assert bst.in_order() == sorted(keys)


def test_float_keys(bst):
    keys = [3.5, 1.2, 7.8, -2.4, 0.0]

    for key in keys:
        bst.put(key)

    assert bst.in_order() == sorted(keys)


def test_mixed_integer_and_float_keys(bst):
    keys = [3, 2.5, 1, 4.75, 0]

    for key in keys:
        bst.put(key)

    assert bst.in_order() == sorted(keys)


def test_string_keys(bst):
    keys = ["banana", "apple", "cherry", "date"]

    for key in keys:
        bst.put(key)

    assert bst.in_order() == sorted(keys)


def test_empty_string_key(bst):
    bst.put("")

    assert bst.in_order() == [""]


def test_case_sensitive_string_keys(bst):
    keys = ["apple", "Apple", "APPLE"]

    for key in keys:
        bst.put(key)

    assert bst.in_order() == sorted(keys)


def test_insert_many_keys(bst):
    keys = list(range(1000, 0, -1))

    for key in keys:
        bst.put(key)

    assert bst.in_order() == list(range(1, 1001))


def test_repeated_traversals_are_consistent(bst):
    for key in [40, 20, 60, 10, 30, 50, 70]:
        bst.put(key)

    first = bst.in_order()
    second = bst.in_order()

    assert first == second


def test_traversals_do_not_modify_tree(bst):
    for key in [40, 20, 60, 10, 30, 50, 70]:
        bst.put(key)

    original = bst.in_order()

    bst.pre_order()
    bst.post_order()

    assert bst.in_order() == original


def test_inserting_after_traversal(bst):
    for key in [50, 30, 70]:
        bst.put(key)

    bst.in_order()
    bst.pre_order()
    bst.post_order()

    bst.put(40)

    assert bst.in_order() == [30, 40, 50, 70]


def test_inserting_same_keys_in_different_orders(bst):
    keys = [50, 30, 70, 20, 40, 60, 80]

    for key in keys:
        bst.put(key)

    expected = sorted(set(keys))

    assert bst.in_order() == expected


def test_duplicate_keys_in_large_input(bst):
    keys = [5, 3, 7, 3, 5, 7, 3, 5, 7]

    for key in keys:
        bst.put(key)

    assert bst.in_order() == [3, 5, 7]


@pytest.mark.parametrize(
    "key",
    [None, [], {}, set(), object()]
)
def test_unorderable_keys_raise_type_error(bst, key):
    with pytest.raises((TypeError, ValueError)):
        bst.put(key)


def test_inserting_incompatible_key_types(bst):
    bst.put(10)

    with pytest.raises(TypeError):
        bst.put("ten")


def test_inserting_none_into_nonempty_tree(bst):
    bst.put(10)

    with pytest.raises((TypeError, ValueError)):
        bst.put(None)


def test_tree_remains_valid_after_invalid_insertion(bst):
    bst.put(10)
    bst.put(5)
    bst.put(15)

    with pytest.raises((TypeError, ValueError)):
        bst.put(None)

    assert bst.in_order() == [5, 10, 15]


def test_duplicate_float_values(bst):
    bst.put(1.0)
    bst.put(1)

    assert len(bst.in_order()) == 1


def test_boolean_keys(bst):
    # Assumption: Python's normal comparison rules apply, so True == 1
    # and False == 0.
    bst.put(False)
    bst.put(True)

    assert len(bst.in_order()) == 2
    assert bst.in_order() == [False, True]


def test_tuple_keys(bst):
    keys = [(2, 3), (1, 5), (3, 1), (1, 2)]

    for key in keys:
        bst.put(key)

    assert bst.in_order() == sorted(keys)


def test_traversal_returns_list(bst):
    bst.put(10)

    assert isinstance(bst.in_order(), list)
    assert isinstance(bst.pre_order(), list)
    assert isinstance(bst.post_order(), list)


def test_tree_handles_alternating_insertions(bst):
    keys = [50, 10, 90, 20, 80, 30, 70, 40, 60]

    for key in keys:
        bst.put(key)

    assert bst.in_order() == sorted(keys)


def test_all_traversals_contain_same_elements(bst):
    keys = [50, 30, 70, 20, 40, 60, 80]

    for key in keys:
        bst.put(key)

    inorder = bst.in_order()
    preorder = bst.pre_order()
    postorder = bst.post_order()

    assert sorted(inorder) == sorted(preorder)
    assert sorted(inorder) == sorted(postorder)
    assert len(inorder) == len(preorder) == len(postorder)


def test_traversal_contains_no_duplicate_keys(bst):
    keys = [10, 5, 15, 5, 10, 15, 20]

    for key in keys:
        bst.put(key)

    for traversal in (
        bst.in_order(),
        bst.pre_order(),
        bst.post_order()
    ):
        assert len(traversal) == len(set(traversal))


def test_all_unique_keys_are_preserved(bst):
    keys = [13, 7, 21, 3, 9, 17, 25]

    for key in keys:
        bst.put(key)

    assert set(bst.in_order()) == set(keys)
    assert len(bst.in_order()) == len(set(keys))