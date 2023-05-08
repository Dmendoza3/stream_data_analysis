from itertools import permutations, combinations

e_list = ["a", "b", "c", "b"]
round_robin = combinations(e_list, 2)

for l in range(2,len(e_list) + 1):
    print(list(combinations(e_list, l)))
