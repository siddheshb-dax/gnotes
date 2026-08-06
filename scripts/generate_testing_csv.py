import time
import argparse

TIME = str(int(time.time()))
FILENAME = f"generated_{TIME}.csv"

parser = argparse.ArgumentParser()
parser.add_argument("--lines", type=int, help="The number of lines to add in the file.")
args = parser.parse_args()

n_lines = args.lines

import random
import string

def generate_random_string():
    MIN_SIZE = 0
    MAX_SIZE = 25

    length = random.randint(MIN_SIZE, MAX_SIZE)
    char_pool = string.ascii_letters + string.digits

    return ''.join(random.choices(char_pool, k=length))

with open(f"../{FILENAME}", "w") as file:
    file.write("title,content\n")
    for i in range(n_lines):
        title = generate_random_string()
        content = generate_random_string()

        file.write(f"{title},{content}\n")

