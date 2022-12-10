import os
from utils import prettify_num

for i in range(3,25):
    path = "day" + prettify_num(str(i))
    os.mkdir(path)
    input_file = open(os.path.join(path, "input.txt"), "x")
    solution_file = open(os.path.join(path, "solution.py"), "x")