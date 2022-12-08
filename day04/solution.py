
# parses the input for one elf as a tuple of (min, max)
def parse_elf_range(input_str: str):
    range_strs = input_str.strip().split("-")
    range_vals = map(int, range_strs) # parse strs to ints
    range_tup = tuple(range_vals)
    return range_tup


def first_contains_second(first, second):
    min_first = first[0]
    min_second = second[0]
    max_first = first[1]
    max_second = second[1]

    return min_first <= min_second and max_first >= max_second

def first_overlaps_with_second(first, second):
    # two pairs a and b overlap, if there is a section d1 ... dt between a1... an and b1... bn that both share.
    # that is, the maximum of a must be bigger than the minimum of b and vice versa.
    min_first = first[0]
    min_second = second[0]
    max_first = first[1]
    max_second = second[1]

    return max_first >= min_second and min_first <= max_second


def one_contains_other(a, b):
    # one contains other if first contains second or vice versa
    return first_contains_second(a,b) or first_contains_second(b, a)


sum_of_full_containments = 0
sum_of_overlaps = 0

with open("input.txt") as input:
    
    for line in input:
        elf_split = line.strip("\n").split(",")
        assert len(elf_split) == 2
        first = parse_elf_range(elf_split[0])
        second = parse_elf_range(elf_split[1])
        if one_contains_other(first, second):
            sum_of_full_containments += 1
        if first_overlaps_with_second(first, second):
            sum_of_overlaps += 1

print("Sum of containments:", sum_of_full_containments)
print("Sum of overlaps:", sum_of_overlaps)