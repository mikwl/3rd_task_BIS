"""As second task: you have the list of symbols (example: a, b, c, c, a (it’s very primitive)).
You should write function that returns the first repeating element from this list (in our example it’s “c”)."""

def duplicate_in_list(x):
    duplicate = []
    unique = []
    try:
        for i in x:
            if i in unique:
                duplicate.append(i)
            else:
                unique.append(i)
        print(f"First duplicate value: {duplicate[0]}")
    except:
        print("Something wrong in your list or there is no duplicate in it.")

"""Easy tests for this function"""

test1 = [1, 2, 1, 3, 2, 5]
duplicate_in_list(test1)

test2 = ["aaa", "bbb", "ccc", "ddd", "yy", "aa", "bb", "yy"]
duplicate_in_list(test2)

test3 = [123, "aaa", 2, 123, "aab"]
duplicate_in_list(test3)

test4 = [1, 2, 3, 4, 5]
duplicate_in_list(test4)