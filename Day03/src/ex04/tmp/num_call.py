import pstats

with open("profiling-ncalls.txt", "w") as f:
    p = pstats.Stats("profiling-output", stream=f)
    p.sort_stats("ncalls").print_stats()

