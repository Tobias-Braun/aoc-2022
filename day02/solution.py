ROCK = 1
PAPER = 2
SCISSORS = 3

elve_to_score_map = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS
}


def win(elf):
    if elf == 3:
        return 1 # win with rock against scissors
    else:
        return elf + 1

def draw(elf):
    return elf # choose the same


def lose(elf):
    if elf == 1:
        return 3 # lose with scissors against rock
    else:
        return elf - 1


result_to_action_map = {
    "X": lose,
    "Y": draw,
    "Z": win,
}

def outcome(elf, me):
    if me == elf:
        return 3 # draw
    elif me > elf:
        if me == SCISSORS and elf == ROCK:
            return 0 # lost
        else:
            return 6 # won
    elif elf > me:
        if me == ROCK and elf == SCISSORS:
            return 6 # won
        else:
            return 0 # lost
    raise NotImplementedError

def round_score(elf, me):
    return outcome(elf, me) + me
    
rounds = []
round_scores = []

with open("input.txt") as input_file:

    for line in input_file:
        choses = line.strip("\n").split(" ")
        assert len(choses) == 2
        elf_action = elve_to_score_map[choses[0]]
        result = choses[1]
        my_action = result_to_action_map[result](elf_action)
        data = (elf_action, my_action)
        rounds.append(data)
        round_scores.append(round_score(*data))

print("Total score:", sum(round_scores))