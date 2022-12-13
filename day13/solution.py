input_str = open("input.txt").read().strip()
pairs = input_str.split("\n\n")

from functools import cmp_to_key

def is_in_order(a, b):
    res = None # None == result could not be determined at current position
    for i in range(len(a)):
        if i == len(b): # if right list is smaller
            return False # not in order
        left, right = a[i], b[i]
        # in the following, res is set in exactly one branch to either True, False, or None
        if type(left) == int and type(right) == int:
            if left < right:
                res = True # in order
            elif left > right:
                res = False # not in order
            # if left == right continue checking (None)
        elif type(left) == int and type(right) == list:
            res = is_in_order(left, right)
        elif type(left) == int:
            res = is_in_order([left], right)
        elif type(right) == int:
            res = is_in_order(left, [right])
        # res updated, check if it determined (res != None)
        if res != None:
            return res
        # not determined, continue checking with values from a
    # a is exhausted, check if b is longer
    if len(a) < len(b):
        return True
    return None # if result can't be determined return with None

def c_in_order(a, b):
    for i in range(len(a)):
        if i == len(b):
            return False
        if type(a[i]) == int and type(b[i]) == int:
            if a[i] > b[i]:
                return False
            elif a[i] < b[i]:
                return True
        elif type(a[i]) == list and type(b[i]) == list:
            sub_result = c_in_order(a[i], b[i])
            if sub_result != None:
                return sub_result
        elif type(a[i]) == int and type(b[i]) == list:
            sub_result = c_in_order([a[i]], b[i])
            if sub_result != None:
                return sub_result
        else:
            sub_result = c_in_order(a[i], [b[i]])
            if sub_result != None:
                return sub_result
    if len(b) > len(a):
        return True
    return None

def sort_cmp(a, b):
    cmp = c_in_order(a, b)
    if cmp == None:
        return 0
    elif cmp == False:
        return 1
    else:
        return -1

in_order = 0
indices_sum = 0
all_list = []
for index, pair in enumerate(pairs):
    vals = pair.split("\n")
    first = eval(vals[0])
    second = eval(vals[1])
    all_list.append(first)
    all_list.append(second)
    res = c_in_order(first, second)
    print(res)
    if res:
        indices_sum += index + 1 # + 1 because they start counting at 1
        in_order += 1

print("Part 1:", indices_sum)
div1 = [[2]]
div2 = [[6]]

all_list.append(div1)
all_list.append(div2)

all_list.sort(key=cmp_to_key(sort_cmp))
print(*all_list, sep="\n")
print("Part 2:", (all_list.index(div1) + 1) * (all_list.index(div2) + 1))

