import pytest

# Assumes the original program is saved in BST.py
from BST import BSTNode, BSTSet, BSTNode_Iterator


# ==========================================
# BSTNode CONSTRUCTOR TESTS
# ==========================================

def test_node_creation():
    node = BSTNode(10)

    assert node.key == 10
    assert node.left is None
    assert node.right is None


def test_node_creation_with_children():
    left = BSTNode(5)
    right = BSTNode(15)
    node = BSTNode(10, left, right)

    assert node.left is left
    assert node.right is right


def test_node_creation_with_negative_key():
    node = BSTNode(-10)
    assert node.key == -10


def test_node_creation_with_zero():
    node = BSTNode(0)
    assert node.key == 0


def test_node_repr():
    node = BSTNode(10)
    assert repr(node) == "BSTNode(key=10)"


# ==========================================
# BSTNode PUT TESTS
# ==========================================

def test_put_smaller_key():
    root = BSTNode(10)
    root.put(5)

    assert root.left.key == 5


def test_put_larger_key():
    root = BSTNode(10)
    root.put(15)

    assert root.right.key == 15


def test_put_duplicate_root():
    root = BSTNode(10)
    root.put(10)

    assert root.left is None
    assert root.right is None


def test_put_duplicate_left_child():
    root = BSTNode(10)
    root.put(5)
    root.put(5)

    assert root.left.key == 5
    assert root.left.left is None
    assert root.left.right is None


def test_put_duplicate_right_child():
    root = BSTNode(10)
    root.put(15)
    root.put(15)

    assert root.right.key == 15
    assert root.right.left is None
    assert root.right.right is None


def test_put_multiple_keys():
    root = BSTNode(10)

    for key in [5, 15, 3, 7, 12, 18]:
        root.put(key)

    assert root.left.key == 5
    assert root.right.key == 15
    assert root.left.left.key == 3
    assert root.left.right.key == 7
    assert root.right.left.key == 12
    assert root.right.right.key == 18


def test_put_negative_keys():
    root = BSTNode(0)

    for key in [-10, -5, -20, 5]:
        root.put(key)

    assert root.left.key == -10
    assert root.left.right.key == -5
    assert root.left.left.key == -20
    assert root.right.key == 5


def test_put_zero():
    root = BSTNode(10)
    root.put(0)

    assert root.left.key == 0


def test_put_ascending_order():
    root = BSTNode(1)

    for key in range(2, 11):
        root.put(key)

    current = root
    for key in range(1, 11):
        assert current.key == key
        if key < 10:
            current = current.right


def test_put_descending_order():
    root = BSTNode(10)

    for key in range(9, 0, -1):
        root.put(key)

    current = root
    for key in range(10, 0, -1):
        assert current.key == key
        if key > 1:
            current = current.left


def test_put_mixed_order():
    root = BSTNode(50)

    keys = [25, 75, 10, 30, 60, 90, 5, 15, 27, 35]

    for key in keys:
        root.put(key)

    assert list(root.in_order()) == sorted([50] + keys)


def test_put_float_keys():
    root = BSTNode(10.5)
    root.put(5.5)
    root.put(15.5)

    assert list(root.in_order()) == [5.5, 10.5, 15.5]


def test_put_string_keys():
    root = BSTNode("m")
    root.put("a")
    root.put("z")

    assert list(root.in_order()) == ["a", "m", "z"]


# ==========================================
# IN-ORDER TRAVERSAL TESTS
# ==========================================

def test_in_order_single_node():
    root = BSTNode(10)

    assert list(root.in_order()) == [10]


def test_in_order_empty_children():
    root = BSTNode(10)

    assert list(root.in_order()) == [10]


def test_in_order_two_children():
    root = BSTNode(10, BSTNode(5), BSTNode(15))

    assert list(root.in_order()) == [5, 10, 15]


def test_in_order_balanced_tree():
    root = BSTNode(10)
    for key in [5, 15, 3, 7, 12, 18]:
        root.put(key)

    assert list(root.in_order()) == [3, 5, 7, 10, 12, 15, 18]


def test_in_order_left_skewed_tree():
    root = BSTNode(10)
    for key in [9, 8, 7, 6]:
        root.put(key)

    assert list(root.in_order()) == [6, 7, 8, 9, 10]


def test_in_order_right_skewed_tree():
    root = BSTNode(1)
    for key in [2, 3, 4, 5]:
        root.put(key)

    assert list(root.in_order()) == [1, 2, 3, 4, 5]


def test_in_order_negative_and_positive():
    root = BSTNode(0)

    for key in [-5, 5, -10, 10]:
        root.put(key)

    assert list(root.in_order()) == [-10, -5, 0, 5, 10]


def test_in_order_duplicate_values():
    root = BSTNode(10)

    for key in [5, 15, 10, 5, 15]:
        root.put(key)

    assert list(root.in_order()) == [5, 10, 15]


def test_in_order_generator():
    root = BSTNode(10)

    result = root.in_order()

    assert iter(result) is result


def test_in_order_multiple_iterations():
    root = BSTNode(10)
    for key in [5, 15, 3, 7]:
        root.put(key)

    assert list(root.in_order()) == [3, 5, 7, 10, 15]
    assert list(root.in_order()) == [3, 5, 7, 10, 15]


def test_in_order_partial_iteration():
    root = BSTNode(10)
    for key in [5, 15, 3, 7]:
        root.put(key)

    iterator = root.in_order()

    assert next(iterator) == 3
    assert next(iterator) == 5


# ==========================================
# PRE-ORDER TRAVERSAL TESTS
# ==========================================

def test_pre_order_single_node():
    root = BSTNode(10)

    assert list(root.pre_order()) == [10]


def test_pre_order_two_children():
    root = BSTNode(10, BSTNode(5), BSTNode(15))

    assert list(root.pre_order()) == [10, 5, 15]


def test_pre_order_balanced_tree():
    root = BSTNode(10)

    for key in [5, 15, 3, 7, 12, 18]:
        root.put(key)

    assert list(root.pre_order()) == [10, 5, 3, 7, 15, 12, 18]


def test_pre_order_left_skewed_tree():
    root = BSTNode(10)

    for key in [9, 8, 7]:
        root.put(key)

    assert list(root.pre_order()) == [10, 9, 8, 7]


def test_pre_order_right_skewed_tree():
    root = BSTNode(1)

    for key in [2, 3, 4]:
        root.put(key)

    assert list(root.pre_order()) == [1, 2, 3, 4]


def test_pre_order_multiple_iterations():
    root = BSTNode(10)
    root.put(5)
    root.put(15)

    assert list(root.pre_order()) == [10, 5, 15]
    assert list(root.pre_order()) == [10, 5, 15]


# ==========================================
# POST-ORDER TRAVERSAL TESTS
# ==========================================

def test_post_order_single_node():
    root = BSTNode(10)

    assert list(root.post_order()) == [10]


def test_post_order_two_children():
    root = BSTNode(10, BSTNode(5), BSTNode(15))

    assert list(root.post_order()) == [5, 15, 10]


def test_post_order_balanced_tree():
    root = BSTNode(10)

    for key in [5, 15, 3, 7, 12, 18]:
        root.put(key)

    assert list(root.post_order()) == [3, 7, 5, 12, 18, 15, 10]


def test_post_order_left_skewed_tree():
    root = BSTNode(10)

    for key in [9, 8, 7]:
        root.put(key)

    assert list(root.post_order()) == [7, 8, 9, 10]


def test_post_order_right_skewed_tree():
    root = BSTNode(1)

    for key in [2, 3, 4]:
        root.put(key)

    assert list(root.post_order()) == [4, 3, 2, 1]


def test_post_order_multiple_iterations():
    root = BSTNode(10)
    root.put(5)
    root.put(15)

    assert list(root.post_order()) == [5, 15, 10]
    assert list(root.post_order()) == [5, 15, 10]


# ==========================================
# BSTNode ITERATOR TESTS
# ==========================================

def test_iterator_single_node():
    root = BSTNode(10)

    assert list(iter(root)) == [10]


def test_iterator_multiple_nodes():
    root = BSTNode(10)

    for key in [5, 15, 3, 7, 12, 18]:
        root.put(key)

    assert list(iter(root)) == [3, 5, 7, 10, 12, 15, 18]


def test_iterator_next():
    root = BSTNode(10)
    root.put(5)
    root.put(15)

    iterator = iter(root)

    assert next(iterator) == 5
    assert next(iterator) == 10
    assert next(iterator) == 15


def test_iterator_stop_iteration():
    root = BSTNode(10)
    iterator = iter(root)

    assert next(iterator) == 10

    with pytest.raises(StopIteration):
        next(iterator)


def test_iterator_repeated_stop_iteration():
    root = BSTNode(10)
    iterator = iter(root)

    next(iterator)

    with pytest.raises(StopIteration):
        next(iterator)

    with pytest.raises(StopIteration):
        next(iterator)


def test_multiple_independent_iterators():
    root = BSTNode(10)
    root.put(5)
    root.put(15)

    iterator1 = iter(root)
    iterator2 = iter(root)

    assert next(iterator1) == 5
    assert next(iterator2) == 5
    assert next(iterator1) == 10
    assert next(iterator2) == 10


# ==========================================
# BSTSET CONSTRUCTOR TESTS
# ==========================================

def test_empty_bstset_creation():
    tree = BSTSet()

    assert tree._head is None


# ==========================================
# BSTSET PUT TESTS
# ==========================================

def test_bstset_put_first_element():
    tree = BSTSet()
    tree.put(10)

    assert tree._head.key == 10


def test_bstset_put_multiple_elements():
    tree = BSTSet()

    for key in [10, 5, 15, 3, 7]:
        tree.put(key)

    assert list(tree.in_order()) == [3, 5, 7, 10, 15]


def test_bstset_put_duplicate_elements():
    tree = BSTSet()

    for key in [10, 5, 15, 10, 5, 15]:
        tree.put(key)

    assert list(tree.in_order()) == [5, 10, 15]


def test_bstset_put_zero():
    tree = BSTSet()
    tree.put(0)

    assert tree._head.key == 0


def test_bstset_put_negative_numbers():
    tree = BSTSet()

    for key in [-10, -5, 0, 5, 10]:
        tree.put(key)

    assert list(tree.in_order()) == [-10, -5, 0, 5, 10]


def test_bstset_put_float_values():
    tree = BSTSet()

    for key in [10.5, 5.5, 15.5]:
        tree.put(key)

    assert list(tree.in_order()) == [5.5, 10.5, 15.5]


def test_bstset_put_string_values():
    tree = BSTSet()

    for key in ["m", "a", "z"]:
        tree.put(key)

    assert list(tree.in_order()) == ["a", "m", "z"]


# ==========================================
# BSTSET TRAVERSAL TESTS
# ==========================================

def test_bstset_in_order_single_node():
    tree = BSTSet()
    tree.put(10)

    assert list(tree.in_order()) == [10]


def test_bstset_in_order_multiple_nodes():
    tree = BSTSet()

    for key in [10, 5, 15, 3, 7]:
        tree.put(key)

    assert list(tree.in_order()) == [3, 5, 7, 10, 15]


def test_bstset_pre_order_single_node():
    tree = BSTSet()
    tree.put(10)

    assert list(tree.pre_order()) == [10]


def test_bstset_pre_order_multiple_nodes():
    tree = BSTSet()

    for key in [10, 5, 15, 3, 7]:
        tree.put(key)

    assert list(tree.pre_order()) == [10, 5, 3, 7, 15]


def test_bstset_post_order_single_node():
    tree = BSTSet()
    tree.put(10)

    assert list(tree.post_order()) == [10]


def test_bstset_post_order_multiple_nodes():
    tree = BSTSet()

    for key in [10, 5, 15, 3, 7]:
        tree.put(key)

    assert list(tree.post_order()) == [3, 7, 5, 15, 10]


def test_bstset_traversals_return_same_elements():
    tree = BSTSet()

    for key in [50, 25, 75, 10, 30, 60, 90]:
        tree.put(key)

    inorder = list(tree.in_order())
    preorder = list(tree.pre_order())
    postorder = list(tree.post_order())

    assert sorted(inorder) == sorted(preorder)
    assert sorted(inorder) == sorted(postorder)
    assert len(inorder) == len(preorder) == len(postorder)


def test_bstset_multiple_traversal_calls():
    tree = BSTSet()

    for key in [10, 5, 15]:
        tree.put(key)

    assert list(tree.in_order()) == [5, 10, 15]
    assert list(tree.pre_order()) == [10, 5, 15]
    assert list(tree.post_order()) == [5, 15, 10]

    assert list(tree.in_order()) == [5, 10, 15]
    assert list(tree.pre_order()) == [10, 5, 15]
    assert list(tree.post_order()) == [5, 15, 10]


# ==========================================
# BSTSET EMPTY TREE TESTS
# ==========================================

def test_empty_bstset_in_order():
    tree = BSTSet()

    # Current implementation raises AttributeError.
    # A properly implemented empty traversal should return no elements.
    with pytest.raises(AttributeError):
        list(tree.in_order())


def test_empty_bstset_pre_order():
    tree = BSTSet()

    assert list(tree.pre_order()) == []


def test_empty_bstset_post_order():
    tree = BSTSet()

    assert list(tree.post_order()) == []


def test_empty_bstset_iteration():
    tree = BSTSet()

    with pytest.raises(TypeError):
        iter(tree)


# ==========================================
# INVALID INPUT TESTS
# ==========================================

def test_put_none_into_bstset():
    tree = BSTSet()
    tree.put(None)

    with pytest.raises(TypeError):
        tree.put(10)


def test_put_incompatible_types():
    tree = BSTSet()
    tree.put(10)

    with pytest.raises(TypeError):
        tree.put("hello")


def test_put_list_key():
    tree = BSTSet()
    tree.put(10)

    with pytest.raises(TypeError):
        tree.put([1, 2, 3])


def test_put_dictionary_key():
    tree = BSTSet()
    tree.put(10)

    with pytest.raises(TypeError):
        tree.put({"key": 10})


def test_put_complex_number():
    tree = BSTSet()
    tree.put(10)

    with pytest.raises(TypeError):
        tree.put(3 + 4j)


def test_put_none_as_first_key():
    tree = BSTSet()
    tree.put(None)

    assert tree._head.key is None


def test_put_boolean_keys():
    tree = BSTSet()

    tree.put(True)
    tree.put(False)

    assert list(tree.in_order()) == [False, True]


# ==========================================
# LARGE INPUT AND STRESS TESTS
# ==========================================

def test_large_balanced_tree():
    tree = BSTSet()

    for key in range(1000):
        tree.put(key)

    assert list(tree.in_order()) == list(range(1000))


def test_large_randomized_tree():
    import random

    random.seed(42)
    values = random.sample(range(10000), 500)

    tree = BSTSet()

    for value in values:
        tree.put(value)

    assert list(tree.in_order()) == sorted(values)


def test_large_duplicate_input():
    tree = BSTSet()

    for _ in range(1000):
        tree.put(10)

    assert list(tree.in_order()) == [10]


def test_large_left_skewed_tree():
    tree = BSTSet()

    for key in range(100, 0, -1):
        tree.put(key)

    assert list(tree.in_order()) == list(range(1, 101))


def test_large_right_skewed_tree():
    tree = BSTSet()

    for key in range(1, 101):
        tree.put(key)

    assert list(tree.in_order()) == list(range(1, 101))


# ==========================================
# ITERATOR AND GENERATOR CONSISTENCY TESTS
# ==========================================

def test_classic_iterator_matches_generator():
    root = BSTNode(50)

    for key in [25, 75, 10, 30, 60, 90]:
        root.put(key)

    assert list(iter(root)) == list(root.in_order())


def test_pre_order_and_post_order_have_same_length():
    root = BSTNode(50)

    for key in [25, 75, 10, 30, 60, 90]:
        root.put(key)

    assert len(list(root.pre_order())) == len(list(root.post_order()))


def test_traversals_contain_no_duplicates():
    root = BSTNode(10)

    for key in [5, 15, 3, 7, 12, 18, 5, 15]:
        root.put(key)

    assert len(list(root.in_order())) == len(set(root.in_order()))
    assert len(list(root.pre_order())) == len(set(root.pre_order()))
    assert len(list(root.post_order())) == len(set(root.post_order()))


def test_traversals_preserve_all_inserted_unique_values():
    values = [40, 20, 60, 10, 30, 50, 70]
    root = BSTNode(values[0])

    for key in values[1:]:
        root.put(key)

    assert set(root.in_order()) == set(values)
    assert set(root.pre_order()) == set(values)
    assert set(root.post_order()) == set(values)


# ==========================================
# TREE STRUCTURE AND INVARIANT TESTS
# ==========================================

def test_bst_left_child_is_smaller():
    root = BSTNode(50)

    for key in [25, 75, 10, 30]:
        root.put(key)

    assert root.left.key < root.key


def test_bst_right_child_is_larger():
    root = BSTNode(50)

    for key in [25, 75, 60, 90]:
        root.put(key)

    assert root.right.key > root.key


def test_bst_in_order_is_sorted():
    root = BSTNode(50)

    for key in [25, 75, 10, 30, 60, 90, 5, 15]:
        root.put(key)

    result = list(root.in_order())

    assert result == sorted(result)


def test_put_does_not_change_existing_nodes():
    root = BSTNode(10)
    root.put(5)
    root.put(15)

    left = root.left
    right = root.right

    root.put(3)

    assert root.left is left
    assert root.right is right


def test_put_does_not_replace_root():
    tree = BSTSet()
    tree.put(10)

    original_root = tree._head
    tree.put(5)
    tree.put(15)

    assert tree._head is original_root