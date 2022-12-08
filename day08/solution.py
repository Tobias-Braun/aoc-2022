import numpy as np

def parse_map():
    map = []
    with open("input.txt") as input_file:
        for line in input_file:
            parsed = [int(char) for char in line.strip("\n")]
            map.append(parsed)
    return map

# part one, compute visibilities

def is_visible(scan_max, val):
    if scan_max < val:
        visible = True
        scan_max = val
    else:
        visible = False
    return scan_max, visible

def create_visibility_array_for_line(scan_line):
    scan_max = -1 # 0 is the smallest height, so we the init val smaller than that.
    visible = []
    for val in scan_line:
        scan_max, cur_visible = is_visible(scan_max, val)
        visible.append(cur_visible)
    return visible

def horizon_visibility(tree_map: np.ndarray) -> np.ndarray:
    vis_left = []
    vis_right = []
    for h_line in tree_map:
        vis_left_line = create_visibility_array_for_line(h_line)
        vis_right_line = create_visibility_array_for_line(h_line[::-1])
        vis_left.append(vis_left_line)
        vis_right.append(vis_right_line[::-1]) # we need to reverse this again to match the normal iteration order
    return np.logical_or(np.array(vis_left), np.array(vis_right))


def vert_visibility(tree_map: np.ndarray) -> np.ndarray:
    vis_top = []
    vis_bottom = []
    for v_line in tree_map.transpose():
        vis_top_line = create_visibility_array_for_line(v_line)
        vis_bot_line = create_visibility_array_for_line(v_line[::-1])
        vis_top.append(vis_top_line)
        vis_bottom.append(vis_bot_line[::-1]) # we need to reverse this again to match the normal iteration order
    return np.logical_or(np.array(vis_top), np.array(vis_bottom)).transpose() # transpose back


def compute_vis_array(tree_map):
    h_vis = horizon_visibility(tree_map)
    v_vis = vert_visibility(tree_map)
    vis = np.logical_or(h_vis, v_vis)
    return vis

tree_map = np.array(parse_map())
vis = compute_vis_array(tree_map)
print("visible trees:", np.sum(vis))

# part two, compute scenic score

# Obvious way would be to iterate through the map and compute the scenic score for each tree
# However, that algorithm is O(n^4) 🤮
# Instead we scan like in part 1, holding a count for each possible tree height, which is O(n^2)

def view_dists_in_line(scan_line: np.ndarray):
    view_dist_by_height = np.zeros(10) # a view dist for each height (id by index). Gets reset to zero when the view is blocked.
    view_dists = []
    for val in scan_line:
        # add score, which is the count for the respective height
        view_dists.append(view_dist_by_height[val])
        # reset count for all trees with same height or smaller
        view_dist_by_height[:val + 1] = 0
        # increase counter for all heights
        view_dist_by_height = view_dist_by_height + 1
    return view_dists

def compute_scenic_scores(tree_map):
    view_dists_left = []
    view_dists_right = []
    view_dists_top = []
    view_dists_bot = []
    for h_line in tree_map:
        vd_left_line = view_dists_in_line(h_line)
        vd_right_line = view_dists_in_line(h_line[::-1])[::-1]
        view_dists_left.append(vd_left_line)
        view_dists_right.append(vd_right_line)
    for v_line in tree_map.transpose():
        vd_top_line = view_dists_in_line(v_line)
        vd_bot_line = view_dists_in_line(v_line[::-1])[::-1]
        view_dists_top.append(vd_top_line)
        view_dists_bot.append(vd_bot_line)
    left, right, top, bot = np.array(view_dists_left), np.array(view_dists_right), np.array(view_dists_top).transpose(), np.array(view_dists_bot).transpose()
    # we transpose top and bot again to revert the transpose we did for these elements previously, so that they match with the other array.
    scenic_scores = left * right * top * bot
    return scenic_scores

scenic_scores = compute_scenic_scores(tree_map)
print(scenic_scores)

print("Max scenic score:", int(np.amax(scenic_scores)))