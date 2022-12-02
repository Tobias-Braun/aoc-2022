import os

def prettify_num(num: str, max_len: int):
    len_diff = max_len - len(num)
    if len_diff == 0:
        return num
    else:
        return "0" * len_diff + num

MAX_NUM_LENGTH = 2 # as max day is 24, which has two digits.

for i in range(3,25):
    path = "day" + prettify_num(str(i), MAX_NUM_LENGTH)
    os.mkdir(path)
    input_file = open(os.path.join(path, "input.txt"), "x")
    solution_file = open(os.path.join(path, "solution.py"), "x")