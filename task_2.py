"""As second task: you have the list of symbols (example: a, b, c, c, a (it’s very primitive)).
You should write function that returns the first repeating element from this list (in our example it’s “c”)."""

def dup(x):
    duplicate = []
    unique = []
    try:
        for i in x:
            if i in unique:
                duplicate.append(i)
            else:
                unique.append(i)
        print(f"First duplicate values: {duplicate[0]}")
    except:
        print("Something wrong in your list or there is no duplicate in it")

list1 = [1, 2, 1, 3, 2, 5]
dup(list1)

list2 = ["aaa", "bbb", "ccc", "ddd", "yy", "aa", "bb", "yy"]
dup(list2)

list3 = [123, "aaa", 2, 123, "aab"]
dup(list3)

list4 = [1, 2, 3, 4, 5]
dup(list4)