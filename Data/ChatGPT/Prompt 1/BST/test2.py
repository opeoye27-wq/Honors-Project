import pytest
from BST import BSTSet, BSTNode

# Import BSTNode and BSTSet from your program
# from your_file import BSTNode, BSTSet


# ============================================================
# BSTNode: Initialization
# ============================================================

def test_node_initialization():
    node = BSTNode(10)

    assert node.key == 10
    assert node.left is None
    assert node.right is None


def test_node_initialization_with_children():
    left = BSTNode(5)
    right = BSTNode(15)

    node = BSTNode(10, left, right)

    assert node.left is left
    assert node.right is right


def test_node_initialization_with_negative_key():
    node = BSTNode(-10)

    assert node.key == -10


def test_node_initialization_with_string_key():
    node = BSTNode("hello")

    assert node.key == "hello"


def test_node_repr():
    node = BSTNode(10)

    assert repr(node) == "BSTNode(key=10)"


# ============================================================
# BSTNode: put()
# ============================================================

def test_put_into_empty_children():
    root = BSTNode(10)

    root.put(5)
    root.put(15)

    assert root.left.key == 5
    assert root.right.key == 15


def test_put_smaller_values():
    root = BSTNode(10)

    root.put(5)
    root.put(3)
    root.put(7)

    assert root.left.key == 5
    assert root.left.left.key == 3
    assert root.left.right.key == 7


def test_put_larger_values():
    root = BSTNode(10)

    root.put(15)
    root.put(20)
    root.put(17)

    assert root.right.key == 15
    assert root.right.right.key == 20
    assert root.right.right.left.key == 17


def test_put_mixed_values():
    root = BSTNode(10)

    for value in [5, 15, 3, 7, 12, 20]:
        root.put(value)

    assert list(root.in_order()) == [3, 5, 7, 10, 12, 15, 20]


def test_put_duplicate_root():
    root = BSTNode(10)

    root.put(10)

    assert root.left is None
    assert root.right is None


def test_put_duplicate_left_child():
    root = BSTNode(10)

    root.put(5)
    root.put(5)

    assert list(root.in_order()) == [5, 10]


def test_put_duplicate_right_child():
    root = BSTNode(10)

    root.put(15)
    root.put(15)

    assert list(root.in_order()) == [10, 15]


def test_put_multiple_duplicates():
    root = BSTNode(10)

    for value in [5, 15, 5, 15, 10, 5, 15]:
        root.put(value)

    assert list(root.in_order()) == [5, 10, 15]


def test_put_negative_values():
    root = BSTNode(0)

    for value in [-10, -5, -20, 5, 10]:
        root.put(value)

    assert list(root.in_order()) == [-20, -10, -5, 0, 5, 10]


def test_put_zero():
    root = BSTNode(10)

    root.put(0)

    assert root.left.key == 0


def test_put_float_values():
    root = BSTNode(10)

    for value in [5.5, 15.5, 2.5]:
        root.put(value)

    assert list(root.in_order()) == [2.5, 5.5, 10, 15.5]


def test_put_incompatible_types():
    root = BSTNode(10)

    with pytest.raises(TypeError):
        root.put("hello")


def test_put_none():
    root = BSTNode(10)

    with pytest.raises(TypeError):
        root.put(None)


# ============================================================
# BSTNode: in_order()
# ============================================================

def test_in_order_single_node():
    root = BSTNode(10)

    assert list(root.in_order()) == [10]


def test_in_order_empty_children():
    root = BSTNode(10)

    assert list(root.in_order()) == [10]


def test_in_order_left_child_only():
    root = BSTNode(10, BSTNode(5))

    assert list(root.in_order()) == [5, 10]


def test_in_order_right_child_only():
    root = BSTNode(10, None, BSTNode(15))

    assert list(root.in_order()) == [10, 15]


def test_in_order_complete_tree():
    root = BSTNode(
        10,
        BSTNode(5, BSTNode(3), BSTNode(7)),
        BSTNode(15, BSTNode(12), BSTNode(20))
    )

    assert list(root.in_order()) == [3, 5, 7, 10, 12, 15, 20]


def test_in_order_skewed_left_tree():
    root = BSTNode(10, BSTNode(8, BSTNode(5, BSTNode(2))))

    assert list(root.in_order()) == [2, 5, 8, 10]


def test_in_order_skewed_right_tree():
    root = BSTNode(1, None, BSTNode(3, None, BSTNode(5)))

    assert list(root.in_order()) == [1, 3, 5]


def test_in_order_generator():
    root = BSTNode(10)

    result = root.in_order()

    assert iter(result) is result
    assert next(result) == 10


def test_in_order_partial_iteration():
    root = BSTNode(10)
    root.put(5)
    root.put(15)

    result = root.in_order()

    assert next(result) == 5
    assert next(result) == 10
    assert next(result) == 15

    with pytest.raises(StopIteration):
        next(result)


def test_in_order_multiple_iterations():
    root = BSTNode(10)
    root.put(5)
    root.put(15)

    assert list(root.in_order()) == [5, 10, 15]
    assert list(root.in_order()) == [5, 10, 15]


# ============================================================
# BSTNode: pre_order()
# ============================================================

def test_pre_order_single_node():
    root = BSTNode(10)

    assert list(root.pre_order()) == [10]


def test_pre_order_complete_tree():
    root = BSTNode(
        10,
        BSTNode(5, BSTNode(3), BSTNode(7)),
        BSTNode(15, BSTNode(12), BSTNode(20))
    )

    assert list(root.pre_order()) == [10, 5, 3, 7, 15, 12, 20]


def test_pre_order_left_child_only():
    root = BSTNode(10, BSTNode(5))

    assert list(root.pre_order()) == [10, 5]


def test_pre_order_right_child_only():
    root = BSTNode(10, None, BSTNode(15))

    assert list(root.pre_order()) == [10, 15]


def test_pre_order_skewed_tree():
    root = BSTNode(10)
    root.put(8)
    root.put(6)
    root.put(4)

    assert list(root.pre_order()) == [10, 8, 6, 4]


def test_pre_order_generator():
    root = BSTNode(10)

    result = root.pre_order()

    assert iter(result) is result
    assert next(result) == 10


def test_pre_order_empty_children():
    root = BSTNode(10)

    assert list(root.pre_order()) == [10]


# ============================================================
# BSTNode: post_order()
# ============================================================

def test_post_order_single_node():
    root = BSTNode(10)

    assert list(root.post_order()) == [10]


def test_post_order_complete_tree():
    root = BSTNode(
        10,
        BSTNode(5, BSTNode(3), BSTNode(7)),
        BSTNode(15, BSTNode(12), BSTNode(20))
    )

    assert list(root.post_order()) == [3, 7, 5, 12, 20, 15, 10]


def test_post_order_left_child_only():
    root = BSTNode(10, BSTNode(5))

    assert list(root.post_order()) == [5, 10]


def test_post_order_right_child_only():
    root = BSTNode(10, None, BSTNode(15))

    assert list(root.post_order()) == [15, 10]


def test_post_order_skewed_tree():
    root = BSTNode(10)
    root.put(8)
    root.put(6)
    root.put(4)

    assert list(root.post_order()) == [4, 6, 8, 10]


def test_post_order_generator():
    root = BSTNode(10)

    result = root.post_order()

    assert iter(result) is result
    assert next(result) == 10


# ============================================================
# BSTNode: Classical Iterator
# ============================================================

def test_node_iterator_single_node():
    root = BSTNode(10)

    assert list(root) == [10]


def test_node_iterator_complete_tree():
    root = BSTNode(
        10,
        BSTNode(5, BSTNode(3), BSTNode(7)),
        BSTNode(15, BSTNode(12), BSTNode(20))
    )

    assert list(root) == [3, 5, 7, 10, 12, 15, 20]


def test_node_iterator_returns_keys_not_nodes():
    root = BSTNode(10)
    root.put(5)
    root.put(15)

    result = list(root)

    assert result == [5, 10, 15]
    assert all(not isinstance(item, BSTNode) for item in result)


def test_node_iterator_empty_after_completion():
    root = BSTNode(10)

    iterator = iter(root)

    assert next(iterator) == 10

    with pytest.raises(StopIteration):
        next(iterator)


def test_node_iterator_multiple_iterations():
    root = BSTNode(10)
    root.put(5)
    root.put(15)

    assert list(root) == [5, 10, 15]
    assert list(root) == [5, 10, 15]


def test_node_iterator_independent_iterators():
    root = BSTNode(10)
    root.put(5)
    root.put(15)

    iterator1 = iter(root)
    iterator2 = iter(root)

    assert next(iterator1) == 5
    assert next(iterator1) == 10
    assert next(iterator2) == 5


# ============================================================
# BSTSet: Initialization
# ============================================================

def test_set_initialization():
    bst = BSTSet()

    assert bst._head is None


# ============================================================
# BSTSet: put()
# ============================================================

def test_set_put_first_element():
    bst = BSTSet()

    bst.put(10)

    assert bst._head.key == 10


def test_set_put_multiple_elements():
    bst = BSTSet()

    for value in [10, 5, 15, 3, 7]:
        bst.put(value)

    assert list(bst.in_order()) == [3, 5, 7, 10, 15]


def test_set_put_duplicate_elements():
    bst = BSTSet()

    for value in [10, 5, 15, 10, 5, 15]:
        bst.put(value)

    assert list(bst.in_order()) == [5, 10, 15]


def test_set_put_negative_values():
    bst = BSTSet()

    for value in [-10, -5, 0, 5, 10]:
        bst.put(value)

    assert list(bst.in_order()) == [-10, -5, 0, 5, 10]


def test_set_put_float_values():
    bst = BSTSet()

    for value in [10.5, 5.5, 15.5]:
        bst.put(value)

    assert list(bst.in_order()) == [5.5, 10.5, 15.5]


def test_set_put_incompatible_types():
    bst = BSTSet()
    bst.put(10)

    with pytest.raises(TypeError):
        bst.put("hello")


def test_set_put_none():
    bst = BSTSet()
    bst.put(10)

    with pytest.raises(TypeError):
        bst.put(None)


def test_set_put_does_not_change_existing_values():
    bst = BSTSet()

    for value in [10, 5, 15]:
        bst.put(value)

    before = list(bst.in_order())

    bst.put(5)

    assert list(bst.in_order()) == before


# ============================================================
# BSTSet: in_order()
# ============================================================

def test_set_in_order_single_element():
    bst = BSTSet()
    bst.put(10)

    assert list(bst.in_order()) == [10]


def test_set_in_order_multiple_elements():
    bst = BSTSet()

    for value in [10, 5, 15, 3, 7, 12, 20]:
        bst.put(value)

    assert list(bst.in_order()) == [3, 5, 7, 10, 12, 15, 20]


def test_set_in_order_is_sorted():
    bst = BSTSet()

    values = [50, 20, 70, 10, 30, 60, 80, 25, 35]

    for value in values:
        bst.put(value)

    result = list(bst.in_order())

    assert result == sorted(set(values))


def test_set_in_order_generator():
    bst = BSTSet()
    bst.put(10)

    result = bst.in_order()

    assert iter(result) is result


def test_set_in_order_empty_tree():
    bst = BSTSet()

    # Potential bug: _head is None, so in_order() raises AttributeError.
    with pytest.raises(AttributeError):
        list(bst.in_order())


def test_set_in_order_multiple_iterations():
    bst = BSTSet()

    for value in [10, 5, 15]:
        bst.put(value)

    assert list(bst.in_order()) == [5, 10, 15]
    assert list(bst.in_order()) == [5, 10, 15]


# ============================================================
# BSTSet: pre_order()
# ============================================================

def test_set_pre_order_single_element():
    bst = BSTSet()
    bst.put(10)

    assert list(bst.pre_order()) == [10]


def test_set_pre_order_multiple_elements():
    bst = BSTSet()

    for value in [10, 5, 15, 3, 7, 12, 20]:
        bst.put(value)

    assert list(bst.pre_order()) == [10, 5, 3, 7, 15, 12, 20]


def test_set_pre_order_empty_tree():
    bst = BSTSet()

    assert list(bst.pre_order()) == []


def test_set_pre_order_generator():
    bst = BSTSet()
    bst.put(10)

    result = bst.pre_order()

    assert iter(result) is result


# ============================================================
# BSTSet: post_order()
# ============================================================

def test_set_post_order_single_element():
    bst = BSTSet()
    bst.put(10)

    assert list(bst.post_order()) == [10]


def test_set_post_order_multiple_elements():
    bst = BSTSet()

    for value in [10, 5, 15, 3, 7, 12, 20]:
        bst.put(value)

    assert list(bst.post_order()) == [3, 7, 5, 12, 20, 15, 10]


def test_set_post_order_empty_tree():
    bst = BSTSet()

    assert list(bst.post_order()) == []


def test_set_post_order_generator():
    bst = BSTSet()
    bst.put(10)

    result = bst.post_order()

    assert iter(result) is result


# ============================================================
# BSTSet: Classical Iterator
# ============================================================

def test_set_iterator_single_element():
    bst = BSTSet()
    bst.put(10)

    assert list(bst) == [10]


def test_set_iterator_multiple_elements():
    bst = BSTSet()

    for value in [10, 5, 15, 3, 7]:
        bst.put(value)

    assert list(bst) == [3, 5, 7, 10, 15]


def test_set_iterator_empty_tree():
    bst = BSTSet()

    # Potential bug: iter(None) raises TypeError.
    with pytest.raises(TypeError):
        list(bst)


def test_set_iterator_returns_keys():
    bst = BSTSet()

    for value in [10, 5, 15]:
        bst.put(value)

    result = list(bst)

    assert result == [5, 10, 15]
    assert all(not isinstance(item, BSTNode) for item in result)


def test_set_iterator_independent_iterators():
    bst = BSTSet()

    for value in [10, 5, 15]:
        bst.put(value)

    iterator1 = iter(bst)
    iterator2 = iter(bst)

    assert next(iterator1) == 5
    assert next(iterator2) == 5


# ============================================================
# BSTSet: Consistency Between Traversals
# ============================================================

def test_all_traversals_contain_same_elements():
    bst = BSTSet()

    values = [10, 5, 15, 3, 7, 12, 20]

    for value in values:
        bst.put(value)

    inorder = list(bst.in_order())
    preorder = list(bst.pre_order())
    postorder = list(bst.post_order())

    assert sorted(inorder) == sorted(preorder)
    assert sorted(inorder) == sorted(postorder)


def test_all_traversals_have_same_length():
    bst = BSTSet()

    values = [10, 5, 15, 3, 7, 12, 20]

    for value in values:
        bst.put(value)

    assert len(list(bst.in_order())) == 7
    assert len(list(bst.pre_order())) == 7
    assert len(list(bst.post_order())) == 7


def test_traversals_after_duplicate_insertions():
    bst = BSTSet()

    for value in [10, 5, 15, 5, 10, 15, 3, 3]:
        bst.put(value)

    assert list(bst.in_order()) == [3, 5, 10, 15]
    assert list(bst.pre_order()) == [10, 5, 3, 15]
    assert list(bst.post_order()) == [3, 5, 15, 10]


# ============================================================
# BSTSet: Stress and Edge Cases
# ============================================================

def test_large_number_of_insertions():
    bst = BSTSet()

    values = list(range(100))

    for value in values:
        bst.put(value)

    assert list(bst.in_order()) == values


def test_large_number_of_reverse_insertions():
    bst = BSTSet()

    values = list(range(100, 0, -1))

    for value in values:
        bst.put(value)

    assert list(bst.in_order()) == sorted(values)


def test_random_insertion_order():
    import random

    bst = BSTSet()

    values = random.sample(range(1000), 200)

    for value in values:
        bst.put(value)

    assert list(bst.in_order()) == sorted(values)


def test_all_same_values():
    bst = BSTSet()

    for _ in range(100):
        bst.put(10)

    assert list(bst.in_order()) == [10]


def test_mixed_integer_and_float_equivalent_values():
    bst = BSTSet()

    for value in [10, 10.0, 5, 5.0, 15, 15.0]:
        bst.put(value)

    assert list(bst.in_order()) == [5, 10, 15]


def test_boolean_keys():
    bst = BSTSet()

    bst.put(False)
    bst.put(True)

    # Python considers False == 0 and True == 1.
    assert list(bst.in_order()) == [False, True]


def test_zero_and_negative_zero():
    bst = BSTSet()

    bst.put(0)
    bst.put(-0.0)

    assert len(list(bst.in_order())) == 1


# ============================================================
# Potential Bug Tests: Mutation and Structural Integrity
# ============================================================

def test_original_tree_structure_preserved_after_duplicate_insert():
    bst = BSTSet()

    for value in [10, 5, 15]:
        bst.put(value)

    original_left = bst._head.left
    original_right = bst._head.right

    bst.put(10)

    assert bst._head.left is original_left
    assert bst._head.right is original_right


def test_insert_does_not_overwrite_existing_subtrees():
    bst = BSTSet()

    for value in [10, 5, 15, 3, 7]:
        bst.put(value)

    bst.put(6)

    assert list(bst.in_order()) == [3, 5, 6, 7, 10, 15]


def test_insert_maintains_bst_ordering():
    bst = BSTSet()

    values = [50, 25, 75, 10, 30, 60, 90, 5, 15]

    for value in values:
        bst.put(value)

    assert list(bst.in_order()) == sorted(values)


def test_generator_created_before_additional_insertions():
    bst = BSTSet()

    bst.put(10)
    bst.put(5)

    traversal = bst.in_order()

    bst.put(15)

    # Generator execution begins when next() is called, not when created.
    assert list(traversal) == [5, 10, 15]


def test_classical_iterator_created_before_additional_insertions():
    bst = BSTSet()

    bst.put(10)
    bst.put(5)

    iterator = iter(bst)

    bst.put(15)

    # Classical iterator queues the tree during construction.
    assert list(iterator) == [5, 10]


# ============================================================
# Potential Bug Tests: Deep Recursion
# ============================================================

def test_deeply_skewed_tree():
    bst = BSTSet()

    for value in range(500):
        bst.put(value)

    assert list(bst.in_order()) == list(range(500))


def test_deeply_skewed_tree_pre_order():
    bst = BSTSet()

    for value in range(500):
        bst.put(value)

    assert list(bst.pre_order()) == list(range(500))


def test_deeply_skewed_tree_post_order():
    bst = BSTSet()

    for value in range(500):
        bst.put(value)

    assert list(bst.post_order()) == list(range(499, -1, -1))


# ============================================================
# Potential Bug Tests: Invalid Tree Structures
# ============================================================

def test_node_with_invalid_left_child_type():
    root = BSTNode(10, left=5)

    with pytest.raises(AttributeError):
        list(root.in_order())


def test_node_with_invalid_right_child_type():
    root = BSTNode(10, right=15)

    with pytest.raises(AttributeError):
        list(root.in_order())


def test_node_with_none_key():
    node = BSTNode(None)

    assert node.key is None


def test_node_with_unordered_key_types():
    root = BSTNode(10)

    with pytest.raises(TypeError):
        root.put("ten")


def test_iterator_with_invalid_node():
    with pytest.raises(AttributeError):
        BSTNode_Iterator(None)


# ============================================================
# Potential Bug Tests: Iterator Protocol
# ============================================================

def test_iterator_object_is_not_itself_an_iterator():
    root = BSTNode(10)

    iterator = iter(root)

    # Potential bug: BSTNode_Iterator does not define __iter__.
    with pytest.raises(TypeError):
        iter(iterator)


def test_iterator_exhaustion_repeatedly():
    root = BSTNode(10)

    iterator = iter(root)

    assert next(iterator) == 10

    with pytest.raises(StopIteration):
        next(iterator)

    with pytest.raises(StopIteration):
        next(iterator)


def test_iterator_counter_after_exhaustion():
    root = BSTNode(10)

    iterator = iter(root)

    next(iterator)

    with pytest.raises(StopIteration):
        next(iterator)

    assert iterator.counter == 1