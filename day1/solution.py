elves = []

with open("input.txt") as input_file:
    next_elf = []
    for line in input_file:
        if line == "\n":
            elves.append(next_elf)
            next_elf = []
        else:
            next_elf.append(int(line))

def sum_calories(elf):
    return sum(elf)

sums = list(map(sum_calories, elves))

def insert_into_top_list(val, top_list):
    for i in range(len(top_list)):
        if val > top_list[i]:
            # insert here and move all others down
            top_list.insert(i, val)
            del top_list[-1] # remove last element so that number of elements stays the same
            break

top_list = [0,0,0]
for val in sums:
    if val > top_list[-1]:
        insert_into_top_list(val, top_list)

print(sum(top_list))