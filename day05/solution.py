import re
import copy

parse_stack_line_regex = re.compile(r"(?:\[([A-Z])\]|(?:\s(\s)\s))(\s|\n)")
move_line_regex = re.compile(r"move (\d+) from (\d+) to (\d+)")

def parse_stack_line(stack_arr, line):
    # the input matches this schema: 3 chars either [d] or 3 spaces, then a separating space.
    # we can use this re to replace the string
    line_sub = re.sub(parse_stack_line_regex, r"\1\2", line)
    return line_sub

def convert_cargo_arr_into_stacks(cargo_arr):
    num_stacks = len(cargo_arr[0])
    stacks = [[] for i in range(num_stacks)] # init one empty stack for each stack in the input
    for line in cargo_arr[::-1]: # go through the array reversed, so from bottom to top of the stack declaration (so we can push elements on the stacks in order)
        for index, char in enumerate(line):
            if char != " ": # we don't append empty slots " " to the stack.
                stacks[index].append(char)
    return stacks

def parse_move(line):
    line_sub = re.sub(move_line_regex, r"\1,\2,\3", line)
    move = tuple([int(x) for x in line_sub.split(",")]) # convert into ints
    return move


def parse_input():
    with open("input.txt") as input_file:
        stacks = None
        cargo_arr = []
        move_list = []
        parsing_stack = True
        for line in input_file:
            if line.startswith(" 1") or line == "\n": # border between stack declaration and moves
                parsing_stack = False
                continue # these two lines are trash, omit them
            if parsing_stack:
                parsed_line = parse_stack_line(cargo_arr, line)
                cargo_arr.append(parsed_line)
                stacks = convert_cargo_arr_into_stacks(cargo_arr)
            else: # parsing moves
                move = parse_move(line)
                move_list.append(move)
    return stacks, move_list

def make_move(stacks, move: tuple[int, int, int], is_part_two: bool):
    count, from_stack, to_stack = move
    from_stack -= 1
    to_stack -= 1 # -= 1 both, because the indices of my list start with zero but the text references of the stacks start at 1
    if not is_part_two:
        # part 1, move one by one
        for _ in range(count):
            element = stacks[from_stack].pop()
            stacks[to_stack].append(element)
    else:
        # part 2, move in order
        moving_sub_stack = stacks[from_stack][-count:]
        stacks[from_stack] = stacks[from_stack][:-count] # remove substack from from_stack
        stacks[to_stack] = stacks[to_stack] + moving_sub_stack # append to to_stack in order (at the end of array == top of stack)

def make_moves(stacks, move_list, is_part_two: bool = False):
    for move in move_list:
        make_move(stacks, move, is_part_two)

def stacks_to_solution_str(stacks):
    top_of_each_stack = [stack[-1] for stack in stacks]
    solution = "".join(top_of_each_stack)
    return solution

if __name__ == "__main__":
    stacks, move_list = parse_input()
    part1_stacks = stacks
    part2_stacks = copy.deepcopy(stacks) # use the copy module here, as list.copy() creates a shallow copy only.

    make_moves(part1_stacks, move_list)
    make_moves(part2_stacks, move_list, is_part_two=True)
    # after this method, we have modified the stacks list in place.
    # we can now print the top of each stack (the last element of the list)

    print("Part 1:", stacks_to_solution_str(part1_stacks))
    print("Part 2:", stacks_to_solution_str(part2_stacks))
