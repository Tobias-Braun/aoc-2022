import numpy as np

def parse_map():
    map = []
    with open("input.txt") as input_file:
        for line in input_file:
            parsed = [int(char) for char in line.strip("\n")]
            map.append(parsed)
    return map

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

def compute_scenic_scores(tree_map):
    

tree_map = np.array(parse_map())
vis = compute_vis_array(tree_map)

print("visible trees:", np.sum(vis))

