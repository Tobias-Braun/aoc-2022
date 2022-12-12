import numpy as np

# a charcode 97

def height(char: str):
    return ord(char) - 96


height_map = [list(map(height, line)) for line in open("input.txt").read().strip().split("\n")]
height_map = np.array(height_map)
positions = np.where(height_map < 0) # starting and signal pos
pos = (positions[0][0], positions[1][0])
sig = (positions[0][1], positions[1][1])
height_map[pos] = 1
height_map[sig] = 26
print(pos, sig)
visited = np.zeros(height_map.shape)
dists = np.full(height_map.shape, 100000)


def in_bounds(neighbor, height_map):
    return height_map.shape[0] > neighbor[0] >= 0 and height_map.shape[1] > neighbor[1] >= 0

def max_one_higher(previous, neighbor):
    max_one_higher = height_map[previous] <= height_map[neighbor] + 1
    return max_one_higher

queued = [sig]
dists[sig] = 0

run = 0
while len(queued) > 0:
    run += 1
    current = queued[0]
    if visited[current]:
        del queued[0]
        continue
    neighbours = [(current[0], current[1] + 1), (current[0], current[1] - 1), (current[0] + 1, current[1]), (current[0] - 1, current[1])]
    neighbours = [n for n in neighbours if in_bounds(n, height_map)]
    neighbours = [n for n in neighbours if visited[n] == 0]
    neighbours = [n for n in neighbours if max_one_higher(current, n)]
    for n in neighbours:
        dists[n] = min(dists[current] + 1,  dists[n])
    del queued[0]
    queued += neighbours
    visited[current] = 1


print("Part 1:", dists[pos])

a_dists = dists[height_map == 1]

print("Part 2:", min(a_dists))