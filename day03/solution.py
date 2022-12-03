def char_to_prio(dup: str):
    charcode = ord(dup)
    if charcode > 96:
        prio = charcode - 96 # so that 97 (a) => 1
    else:
        # should be between 65 (A) and 90 (Z)
        prio = charcode - 38 # so that A == 65 => 65 - 38 == 27
    return prio

sum_prios = 0
distinct_rucksacks = []

with open("input.txt") as input_file:

    for line in input_file:
        line = line.strip("\n")
        num_items = len(line)
        assert num_items % 2 == 0
        split_point = len(line) // 2
        first = line[:split_point]
        second = line[split_point:]

        # prepare input for part 2
        distinct_rucksacks.append(set(line))
        # use set logic to find duplicates
        distinct_first = set(first)
        distinct_second = set(second)
        duplicates = distinct_first.intersection(distinct_second)
        for dup in duplicates:
            prio = char_to_prio(dup)
            sum_prios += prio

num_elves = len(distinct_rucksacks)
GROUP_SIZE = 3
assert num_elves % GROUP_SIZE == 0

badge_prio_sum = 0

for i in range(0, num_elves, GROUP_SIZE):
    first: set = distinct_rucksacks[i]
    second: set = distinct_rucksacks[i+1]
    third: set = distinct_rucksacks[i+2]

    intersection = first.intersection(second).intersection(third)
    assert len(intersection) == 1
    badge = list(intersection)[0]
    badge_prio = char_to_prio(badge)
    badge_prio_sum += badge_prio

print("Sum of prios of the duplicates", sum_prios)
print("Sum of badge prios", badge_prio_sum)