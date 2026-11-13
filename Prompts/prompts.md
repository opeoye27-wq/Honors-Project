# Prompt 1: Sending the code directly

I will provide you with a program. Analyze the code and generate a comprehensive set of unit tests that covers all possible edge cases and identify potential bugs

Return an executable unit test code using the appropriate framework for the given programming language. Include tests for normal inputs, coundary conditions, unusual inputs, and invalid inputs where applicable

Do not modify the original program. Do not include the implementation of the function in your response. Return only the unit tests.

# Prompt 2: Detailed Description Only

I will provide you with a detailed description of a program. Based on this description alone, generate a comprehensive set of unit tests that aims to cover all possible edge cases and identify potential bugs.

Return an executable unit test code using the appropriate framework for the given programming language. Include tests for normal inputs, coundary conditions, unusual inputs, and invalid inputs where applicable

Base your tests only on the behavior and requirements stated in the description. Don't assume accesses to the original implementation. If any behavior is ambiguous, don't silently assume an answer; make the assumption explicit.

Do not include the implementation of the function in your response. Return only the unit tests.

## Basic Counting Program
I am working with a Python program that contains two lists of integers and two functions designed to determine how many values the lists have in common.

The program is intended to count the distinct values that appear in both lists. The lists are generated randomly and contain integers drawn from a range based on the requested list size. The program also compares two approaches to finding common elements: one that uses nested loops and another that uses Python sets.

Generate a comprehensive set of Python unit tests for the functions that calculate the number of common elements. Focus on verifying correctness across normal inputs, empty lists, lists with no common elements, lists with all elements in common, partially overlapping lists, negative integers, zero, and boundary cases. Also consider how duplicate values should be handled according to the intended behavior of counting distinct common values.

The expected result for each test should be determined by the stated behavior, not by assuming the implementation is correct.

Use pytest. Do not modify or implement the functions being tested. Return only executable unit test code.

## Binary Search Tree
I am working with a Python implementation of a binary search tree set. The program has two classes: BSTNode, which represents individual nodes and handles tree operations, and BSTSet, which provides the public interface for interacting with the tree.

The tree stores unique keys. For each node, keys smaller than its key belong in the left subtree, and keys larger than its key belong in the right subtree. Inserting a key that already exists should not create a duplicate.

The program supports inserting keys and traversing the tree in three orders:
- In-order: visit the left subtree, the current node, and then the right subtree.
- Pre-order: visit the current node, the left subtree, and then the right subtree.
- Post-order: visit the left subtree, the right subtree, and then the current node.

In-order traversal should produce keys in ascending order. The tree should support negative integers, zero, and positive integers.

Generate a comprehensive set of Python unit tests using pytest. Test normal operations and edge cases, including an empty tree, a tree with one node, inserting duplicate keys, inserting keys in ascending or descending order, inserting values smaller or larger than the root, and traversing trees with missing left or right children.

Check that all three traversal methods produce the correct order and that inserting keys preserves the set's uniqueness and binary search tree properties. Also test iteration where applicable.

Do not modify or implement the program. Base expected results on the behavior described above. Return only executable unit test code.

## Records Map
I am working with a Python program that implements a hash table for storing temperature records associated with geographic positions.

Each position is a pair of numeric coordinates, and each record stores the minimum and maximum temperatures reported at that position. When a new temperature is reported for a position that already exists, the record should update its minimum and maximum temperatures accordingly. When a position has no existing record, a new record should be created with the reported temperature as both its minimum and maximum.

The hash table uses hashing to assign positions to buckets and must handle hash collisions correctly. It should track the number of unique positions stored and automatically increase its capacity when its load factor exceeds 0.7. Resizing and rehashing should preserve all existing records and their temperature values.

The program supports looking up the minimum and maximum temperatures for a position, checking whether a position exists in the table, and retrieving the number of unique positions stored. Looking up a position that does not exist should raise a KeyError.

Coordinates should be matched according to a consistent rounding rule: coordinates are rounded to the nearest whole number before positions are compared. Positions that resolve to the same rounded coordinate pair should refer to the same record.

Generate a comprehensive set of Python unit tests using pytest. Include normal cases and edge cases involving empty tables, negative and zero temperatures, repeated reports at the same position, updates to minimum and maximum temperatures, coordinates that round to the same position, missing positions, hash collisions, and resizing with multiple existing records.

Verify that the number of unique records remains correct and that all minimum and maximum temperatures are preserved after updates and resizing. Do not modify or implement the program. Base expected results on the behavior described above. Return only executable unit test code.


# Prompt 3: Minimal Description Only

I will provide you with a brief description of a program. Based on this description alone, generate a comprehensive set of unit tests that aims to cover all possible edge cases and identify potential bugs.

Return an executable unit test code using the appropriate framework for the given programming language. Include tests for normal inputs, coundary conditions, unusual inputs, and invalid inputs where applicable

Base your tests only on the behavior and requirements stated in the description. Don't assume accesses to the original implementation. If any behavior is ambiguous, don't silently assume an answer; make the assumption explicit.

Do not include the implementation of the function in your response. Return only the unit tests.

## Basic Counting Program
I have a Python program with functions that count the number of common elements between two lists of integers.

Generate Python unit tests using pytest to test these functions. Include normal cases, edge cases, and unusual inputs.

Do not modify or implement the functions being tested. Return only executable unit test code.

## Binary Search Tree
I have a Python program that implements a binary search tree set. It supports inserting keys and traversing the tree in different orders.

Generate Python unit tests using pytest to test the program's functionality. Include normal cases, edge cases, and unusual inputs.

Do not modify or implement the program. Return only executable unit test code.

## Records Map
I have a Python program that implements a hash table for storing minimum and maximum temperature records at geographic positions.

Generate Python unit tests using pytest to test the program's functionality. Include normal cases, edge cases, and unusual inputs.

Do not modify or implement the program. Return only executable unit test code.