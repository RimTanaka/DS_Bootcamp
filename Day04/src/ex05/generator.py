#!/usr/bin/python3

import sys
import time
import resource


def read_lines_generator(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def main():
    if len(sys.argv) != 2:
        print("Usage: ./generator.py <file_path>")
        sys.exit(1)

    try:
        filepath = sys.argv[1]

        start_time = time.process_time()
        tmp = read_lines_generator(filepath)
        for _ in tmp:
            pass
        end_time = time.process_time()

        peak_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3)
        print(f"Peak Memory Usage = {peak_memory: .3f} GB")
        print(f"User Mode Time + System Mode Time = {end_time - start_time: .2f}s")
    except FileNotFoundError as ex:
        print(f"Error: {ex}")


if __name__ == "__main__":
    main()
