from itertools import chain
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)



paths = [[eval(exp) for exp in line.split(" -> ")] for line in open("input.txt").read().strip().splitlines()]
flatten_paths = list(chain.from_iterable(paths))

xes = [pos[0] for pos in flatten_paths]
yes = [pos[1] for pos in flatten_paths]

min_x = min(xes)
max_x = max(xes)
min_y = min(yes)
max_y = max(yes) + 2

GRID_DIMS = (1000, max_y + 1)
grid = np.zeros(GRID_DIMS)

def print_grid(grid):
    print("TOP " * 12)
    for x_line in range(GRID_DIMS[1]):
        p_line = [ "." if p == 0 else "#" if p == 1 else "o" for p in grid[:,x_line]]
        print("".join(p_line[400:600]))
    print("END " * 12)

for path in paths:
    curr = path[0]
    for val in path[1:]:
        x_first = curr[0]
        x_second = val[0]
        y_first = curr[1]
        y_second = val[1]
        if x_first == x_second:
            # slice y
            if y_first <= y_second:
                grid[x_first,y_first:y_second + 1] = 1
            else:
                grid[x_first,y_second:y_first + 1] = 1
        else:
            # slice x
            if x_first <= x_second:
                grid[x_first:x_second + 1, y_first] = 1
            else:
                grid[x_second:x_first + 1, y_first] = 1
        curr = val

# part 2 add floor:
grid[:,max_y] = 1

FALL_CORD = (500, 0)
print_grid(grid)
print( grid.shape)

curr_coord = FALL_CORD
n_sand = 0
# we go up in y direction

while True: # no sand has fallen out of bounds yet
    # simulate falling sand from curr_coord
    down = (curr_coord[0], curr_coord[1] + 1)
    diagonal_left = (curr_coord[0] - 1, curr_coord[1] + 1)
    diagonal_right = (curr_coord[0] + 1, curr_coord[1] + 1)
    if grid[down] == 0:
        curr_coord = down
        continue
    elif grid[diagonal_left] == 0:
        curr_coord = diagonal_left
        continue
    elif grid[diagonal_right] == 0:
        curr_coord = diagonal_right
        continue
    # rest
    grid[curr_coord] = 2
    n_sand += 1
    if curr_coord == FALL_CORD:
        break
    curr_coord = FALL_CORD


print_grid(grid)
print("Part 1:", n_sand)


# part 2: