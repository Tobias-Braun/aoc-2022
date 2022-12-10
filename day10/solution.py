
ADDX = "addx"
NOOP = "noop"

INSTRUCTIONS = [ADDX, NOOP]

CYCLES = {
    ADDX: 2,
    NOOP: 1
}

X = 1
Sprite = [0, 1, 2]
cycles = 0
next_target = 20
signal_sum = 0

CRT = ""

with open("input.txt") as input_file:
    for line in input_file:
        instruction = None
        val = None
        line = line.strip()
        if line.startswith("add"):
            # add instruction
            instruction = ADDX
            val = int(line.split(" ")[1])
        else:
            # noop
            instruction = NOOP
        # add cycles
        print(instruction, val, cycles, "S:", Sprite)
        for _ in range(CYCLES[instruction]):
            if cycles % 40 in Sprite:
                CRT += "#"
            else:
                CRT += "."
            cycles += 1
            if cycles >= next_target:
                print("signal strength", X, next_target)
                signal_val = X * next_target
                signal_sum += signal_val
                next_target = next_target + 40
        if instruction == ADDX:
            # update X
            X += val
            Sprite = [X - 1, X, X + 1]

print("Part 1:", signal_sum)


print("Part 2:")
print(CRT[0:40])
print(CRT[40:80])
print(CRT[80:120])
print(CRT[120:160])
print(CRT[160:200])
print(CRT[200:240])