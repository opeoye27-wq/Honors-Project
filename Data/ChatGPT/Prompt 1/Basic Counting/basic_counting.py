import random
import time

def generate_lists(size):
    list1 = random.sample(range(size * 2), size)
    list2 = random.sample(range(size * 2), size)
    return list1, list2
    pass

def find_common(list1, list2): #Costs: n^2 + 2n + 1 --> O(n^2)
    common = 0 #1 
    for i in list1: #n *
        for j in list2: #n
            if i == j: #n
                common += 1 #1
    return common # n
    pass

def find_common_efficient(list1, list2): #Big O is O(n) 
    return len(set(list1) & set(list2)) #use set since the cannot have duplicates
    """4 operations: returns a val, gets lenth of a set, converts list1 and list2 to sets, and looks for common nums """
    pass 

def measure_time():
    sizes = [10, 100, 1000, 10000]
    print(f"{'List Size':<10} {'find_common Time (s)':<25} {'find_common_efficiet Time (s)':<30}")
    for i in sizes:
        list1, list2 = generate_lists(i)
        if i <= 100000:
            start = time.perf_counter()
            find_common(list1, list2)
            end = time.perf_counter()
            t1 = end - start
        else: 
            t1 = float('nan')
        if i <= 1000000:
            start = time.perf_counter()
            find_common_efficient(list1, list2)
            end = time.perf_counter()
            t2 = end - start
        else: 
            t2 = float('nan')

        print(f"{i:<10} {t1:<25f} {t2:<20.6f}" )
    
    pass


if __name__ == "__main__":
    measure_time()
