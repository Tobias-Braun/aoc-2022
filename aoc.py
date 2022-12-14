#! python3
from datetime import date
import subprocess

d = date.today()
day = d.strftime("%d")

cmd = f"powershell.exe Get-Content day{day}/input.txt | python " + f"day{day}/solution.py"
print(cmd)

p = subprocess.run(cmd)