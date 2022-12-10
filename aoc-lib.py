from typing import Literal
import requests
from utils import prettify_num
import os
import argparse

# Create the ArgumentParser object
parser = argparse.ArgumentParser()
parser.add_argument("day", type=int, help="day of the challenge (1-24)", choices=range(1, 25))
parser.add_argument("--answer", type=int, help="challenge answer")
parser.add_argument("--level", type=int, help="level (1-2)", choices=range(1, 3))

# Parse the command line arguments
args = parser.parse_args()

day = args.day
answer = args.answer
level = args.level

session = open("session.cookie").readline().strip("\n").strip()

headers = {
    "Cookie": f"session={session}",
    "User-Agent": "aoc-lib https://github.com/Tobias-Braun/aoc-2022"
}

def get_input(day: int):
    url = f"https://adventofcode.com/2022/day/{day}/input"
    response = requests.get(url, headers=headers)
    return response.text

def write_input_to_file(day: int, input_str: str):
    file_path = os.path.join("./", "day" + prettify_num(day), "input.txt")
    with open(file_path, "w") as input_writer:
        input_writer.writelines(input_str)

def submit_solution(answer: int, day: int, level: Literal[1, 2]) -> tuple[bool, str]:
    url = f"https://adventofcode.com/2022/day/{day}/answer"
    print(url)
    form_params = {
        "answer": answer,
        "level": level
    }
    response = requests.post(url, headers=headers, params=form_params)
    return response.text

if __name__ == "__main__":
        
    if answer != None:
        assert level != None
        assert day != None
        # submit answer
        print(f"Submitting {answer} for day {day}, level {level}")
        res = submit_solution(answer, day, level)
        print(res)
    else: 
        # get input for day
        print(f"Getting input for day {day}")
        input_data = get_input(day)
        write_input_to_file(day, input_data)
        