from typing import Literal, NewType
import numpy as np

# This puzzle is not the best, because it is unclear if the field should have borders or not, and how big it is.
# I assume that the field must be so big that we never hit the borders.
# I also don't know where my initial state is, so I will copy the example and move it so that I use the smallest board possible while still not hitting borders.

# type aliases for typehints
Direction = Literal['D', 'U', 'L', 'R']
Pos = NewType("Pos", tuple[int, int]) 
Move = NewType("Move", tuple[Direction, int])
BoardSize = NewType("BoardSize", tuple[int, int])

def move_head(pos: Pos, direction: Direction) -> Pos:
    if direction == "R":
        return (pos[0] + 1, pos[1])
    elif direction == "L":
        return (pos[0] - 1, pos[1])
    elif direction == "D":
        return (pos[0], pos[1] + 1)
    elif direction == "U":
        return (pos[0], pos[1] - 1)
    else:
        raise Exception(f"Direction is {direction}, should by in [R, L, D, U].")

def correction(diff):
    # a bit hacky, if diff is zero the result is meaningless, but it is also not used if the diff is zero, so it doesn't matter
    return 1 if diff > 0 else -1

def move_tail(head_pos: Pos, tail_pos: Pos) -> Pos: # returns new tail pos
    head_h, head_v = head_pos
    tail_h, tail_v = tail_pos
    h_differs_by_two = abs(head_h - tail_h) == 2
    h_correction = correction(head_h - tail_h)
    v_differs_by_two = abs(head_v - tail_v) == 2
    v_correction = correction(head_v - tail_v)
    not_in_same_row_and_col = head_h != tail_h and head_v != tail_v
    if (h_differs_by_two or v_differs_by_two) and not_in_same_row_and_col: # diagonal correction
        return (tail_h + h_correction, tail_v + v_correction)
    elif h_differs_by_two: # horizontal correction
        return (tail_h + h_correction, tail_v)
    elif v_differs_by_two: # vertical correction
        return (tail_h, tail_v + v_correction)
    else:
        return tail_pos

def parse_input():
    move_list = []
    with open("input.txt") as input_file:
        for line in input_file:
            move = line.strip("\n").split(" ")
            move = (move[0], int(move[1])) # parse into correct datatypes, make tuple
            move_list.append(move)
    return move_list

def get_rel_dists_by_moves(move_list):
    curr_pos: Pos = (0, 0)
    h_min = 0
    h_max = 0
    v_min = 0
    v_max = 0
    for move in move_list:
        direction, dist = move
        for _ in range(dist):
            curr_pos = move_head(curr_pos, direction) # we don't have to calc the tail movement to get board dimensions, because it will always be interior to the head. (like tires of a car making a curve)
        h_pos, v_pos = curr_pos
        if h_pos > h_max:
            h_max = h_pos
        if h_pos < h_min:
            h_min = h_pos
        if v_pos > v_max:
            v_max = v_pos
        if v_pos < v_min:
            v_min = v_pos
    print("Rel movement dists:", f"[({h_min}, {h_max}), ({v_min},{v_max})]")
    print()
    return ((h_min, h_max), (v_min, v_max))

class Board:

    def __init__(self, board_size: BoardSize, initial_head_pos: Pos, num_knots: int):
        self.board_size = board_size
        self.knot_positions = [initial_head_pos for _ in range(num_knots)]
        self.num_knots = num_knots
        self.board = self.create_board(board_size)

    def __str__(self):
        return f"Board, with head at {self.knot_positions[0]}, tail at {self.knot_positions[-1]} and {self.sum_tail_positions()} tail positions and {self.num_knots} knots."

    def create_board(self, board_size: BoardSize):
        board = np.zeros(board_size) # note that if you print the board, it is transposed(), but that does not change the correctness of our results
        board[self.knot_positions[-1]] = 1 # we denote a tail visit by increasing the board value by 1. > 0 means the tail has visited the board.
        return board

    def update_with_move(self, move: Move):
        direction, dist = move
        for _ in range(dist):
            self.move_on_board(direction)

    def move_on_board(self, direction: Direction):
        self.knot_positions[0] = move_head(self.knot_positions[0], direction)
        for i in range(1, self.num_knots):
            self.knot_positions[i] = move_tail(self.knot_positions[i-1], self.knot_positions[i])
        self.board[self.knot_positions[-1]] = 1 # mark tail visit

    def sum_tail_positions(self):
        return int(np.sum(self.board))

if __name__ == "__main__":

    move_list = parse_input()
    rel_dists = get_rel_dists_by_moves(move_list)
    h_dists, v_dists = rel_dists
    h_min, h_max = h_dists
    v_min, v_max = v_dists
    h_size = h_max - h_min + 1 # + 1 to include the zero
    v_size = v_max - v_min + 1 # + 1 to include the zero

    board_size = (h_size, v_size)
    initial_head_pos = (-h_min, -v_min) # move the initial head pos so that the min movements end up at 0 for both axes.

    # init board part 1
    p1_board: Board = Board(board_size, initial_head_pos, 2)
    print(str(p1_board))
    for move in move_list:
        p1_board.update_with_move(move)
    print("After moves...")
    print(str(p1_board))
    print()
    print("Part 1:", p1_board.sum_tail_positions())

    # part 2
    print()
    p2_board: Board = Board(board_size, initial_head_pos, 10)
    print(str(p2_board))
    for move in move_list:
        p2_board.update_with_move(move)
    print("After moves...")
    print(str(p2_board))
    print()
    print("Part 2:", p2_board.sum_tail_positions())