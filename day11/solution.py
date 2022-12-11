from functools import reduce

global MONKEYS

def operate(old, num, operator):
    if operator == "*":
        return old * num
    elif operator == "+":
        return old + num
    elif operator == "**":
        return old ** num


global last_id
last_id = 0

prod_of_mods = 0

def gen_id():
    global last_id
    last_id += 1
    return last_id


class Monkey:

    def __init__(self, items: list[tuple[int, int]], test_mod: int, decisions: tuple[int, int], operator, num):
        self.items = items
        self.test_mod = test_mod
        self.decisions = decisions
        self.operator = operator
        self.num = num
        self.inspections = 0

    @staticmethod
    def from_string(lines: list[str]) -> "Monkey":
        monkey_num = lines[0].split("Monkey ")[1].strip("\n").strip(":")
        worry_levels = [int(x) for x in lines[1].split("  Starting items: ")[1].strip("\n").split(", ")]
        items = [(gen_id(), worry_level) for worry_level in worry_levels]
        operation_strs = lines[2].split("  Operation: new = old ")[1].strip("\n").split(" ")
        operator = operation_strs[0]
        if operation_strs[1] == "old":
            operator = "**"
            num = 2
        else:
            num = int(operation_strs[1])
        test_mod = int(lines[3].split("  Test: divisible by ")[1].strip("\n"))
        decision_true = int(lines[4].split("    If true: throw to monkey ")[1].strip("\n"))
        decision_false = int(lines[5].split("    If false: throw to monkey ")[1].strip("\n"))
        decisions = (decision_false, decision_true)

        return Monkey(items, test_mod, decisions, operator, num)

    def __repr__(self):
        return f"M{self.items}, I: {self.inspections}"

    def test(self, worry_level: int):
        return worry_level % self.test_mod == 0

    def throw_to_monkey(self, monkey_idx, item):
        MONKEYS[monkey_idx].items.append(item)
        del self.items[0]

    def turn_item(self):
        item = self.inspect()
        decision = 1 if self.test(item[1]) else 0
        self.throw_to_monkey(self.decisions[decision], item)

    def turn(self):
        for i in range(len(self.items)):
            self.turn_item()


    def inspect(self):
        item = self.items[0]
        item_id = item[0]
        worry_level = item[1]
        worry_level = operate(worry_level, self.num, self.operator)
        worry_level = worry_level % prod_of_mods # comment for part 1
        # worry_level = worry_level // 3 uncomment for part 1
        self.inspections += 1
        return (item_id, worry_level)

def parse_input():
    global MONKEYS
    with open("input.txt") as input_reader:
        lines = input_reader.readlines()
        monkeys = "".join(lines).split("\n\n") # double \n only comes where there is an empty line
        monkeys = [Monkey.from_string(monkey.split("\n")) for monkey in monkeys]
        MONKEYS = monkeys

parse_input()

mods = [monkey.test_mod for monkey in MONKEYS]
prod_of_mods = reduce((lambda x, y: x * y), mods)
print(mods, prod_of_mods)

for _ in range(10000):
    for monkey in MONKEYS:
        monkey.turn()

inspections = [monkey.inspections for monkey in MONKEYS]
sorted_insp = sorted(inspections)
print(inspections)
print("Monkey business:", sorted_insp[-1] * sorted_insp[-2] )