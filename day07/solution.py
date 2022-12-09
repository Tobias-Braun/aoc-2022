# We build a tree using anytree (https://stackoverflow.com/questions/2358045/how-can-i-implement-a-tree-in-python)
from anytree import Node
import re
from numerize.numerize import numerize


CD_COMMAND = "cd"
LS_COMMAND = "ls"
FILE = "file"
DIR = "dir"

def node_path_str(curr_node):
    return "/".join([str(node.name) for node in curr_node.path])

NODE_SIZES = {"": None} # hash table that holds the sizes based on node name

NODE_TYPES = {"": DIR} # hash table that holds the types based on node name

# Name parsing
file_parse_regex = r"(?:\d+)\s([\w\.]+)"
dir_parse_regex = r"dir\s([\w\.]+)"
cd_command_parse_regex = r"\$ cd ([\w\.\/]+)"
ls_command_parse_regex = r"\$ (ls)"



ALL_TYPES = [CD_COMMAND, LS_COMMAND, FILE, DIR]

TYPE_TO_REGEX = {
    CD_COMMAND: cd_command_parse_regex,
    LS_COMMAND: ls_command_parse_regex,
    FILE: file_parse_regex,
    DIR: dir_parse_regex,
}

# Size parsing for file
file_size_parsing = re.compile(r"(\d+)\s(?:[\w\.]+)")


# Part 2 declarations
FILE_SYSTEM_SIZE = 70_000_000
TARGET_UNUSED_SPACE = 30_000_000

def change_dir(curr_node, rel_path, size = None):
    if rel_path == "..":
        # print("moving up to " + curr_node.parent.name)
        new_node = curr_node.parent
    else:
        # print("going to child " + rel_path)
        children = curr_node.children
        children_with_matching_path = [child for child in children if child.name == rel_path]
        assert len(children_with_matching_path) == 1
        new_node = children_with_matching_path[0]
    return new_node

def noop(curr_node, rel_path, size = None):
    return curr_node

def add_node(curr_node, rel_path, size = None, node_type = str):
    new_node = Node(rel_path, parent=curr_node)
    # print("Listed " + node_type + " " + rel_path + ", child of " + curr_node.name)
    # print("path_str:", node_path_str(new_node))
    path_str = node_path_str(new_node)
    NODE_SIZES[path_str] = size
    NODE_TYPES[path_str] = node_type
    return curr_node

def add_file(curr_node, rel_path, size = None):
    return add_node(curr_node, rel_path, size, node_type=FILE)

def add_dir(curr_node, rel_path, size = None):
    return add_node(curr_node, rel_path, size = None, node_type=DIR)

TYPE_TO_ACTION = {
    CD_COMMAND: change_dir,
    LS_COMMAND: noop,
    FILE: add_file,
    DIR: add_dir,
}


def terminal_line_to_path(regex, string):
    return re.sub(regex, r"\1", string)

def regex_matches(regex, line):
    return re.match(regex, line) != None

def get_line_type(line):
    for line_type in ALL_TYPES:
        regex = TYPE_TO_REGEX[line_type]
        if regex_matches(regex, line):
            return line_type
    raise Exception("Parsing Error, should match known type:", line)

def parse_file_size(string):
    return int(re.sub(file_size_parsing, r"\1", string))


def parse_input():
    with open("input.txt") as input_file:

        first_line = input_file.readline() # read first line to get root of tree
        assert re.match(cd_command_parse_regex, first_line) != None
        root = Node("")
        current_node = root
        print(node_path_str(current_node))
        for line in input_file: # all other input lines
            line = line.strip("\n")
            line_type = get_line_type(line)
            path = terminal_line_to_path(TYPE_TO_REGEX[line_type], line)
            size = None
            if line_type == FILE:
                size = parse_file_size(line)
            action = TYPE_TO_ACTION[line_type] # action is a callable with the params (curr_node, rel_path, size)
            current_node = action(current_node, path, size)
    return root

def get_size(node):
    path_str = node_path_str(node)
    if NODE_SIZES[path_str] != None:
        return NODE_SIZES[path_str]
    else:
        assert NODE_TYPES[path_str] == DIR
        size_sum = 0
        for child in node.children:
            child_size = get_size(child)
            size_sum += child_size
        NODE_SIZES[path_str] = size_sum
        return size_sum

def get_under_threshold_count(node, threshold):
    path_str = node_path_str(node)
    if NODE_TYPES[path_str] == DIR:
        count_sum = 0
        size_sum = 0
        for child in node.children:
            child_count, child_size_sum = get_under_threshold_count(child, threshold)
            count_sum += child_count
            size_sum += child_size_sum
        own_size = get_size(node)
        if own_size <= threshold:
            count_sum += 1
            size_sum += own_size
        return count_sum, size_sum 
    else:
        return 0, 0

def get_smallest_over_threshold(node, threshold):
    path_str = node_path_str(node)
    smallest_size = FILE_SYSTEM_SIZE
    for child in node.children:
        smallest_in_child = get_smallest_over_threshold(child, threshold)
        if smallest_in_child >= threshold and smallest_in_child < smallest_size:
            smallest_size = smallest_in_child
    own_size = get_size(node)
    if own_size >= threshold and own_size < smallest_size:
        smallest_size = own_size
    return smallest_size

if __name__ == "__main__":
    # Part 1
    root = parse_input()
    complete_size = get_size(root)
    count, size_sum = get_under_threshold_count(root, 100000)
    print("Part 1:", size_sum)

    unused_space = FILE_SYSTEM_SIZE - complete_size
    space_to_free = TARGET_UNUSED_SPACE - unused_space
    smallest_size = get_smallest_over_threshold(root, space_to_free)
    print("Disk", numerize(FILE_SYSTEM_SIZE), "Used", numerize(complete_size), "Target", numerize(TARGET_UNUSED_SPACE), "to_free", numerize(space_to_free), "smallest", numerize(smallest_size))
    print("Part 2:", smallest_size)


