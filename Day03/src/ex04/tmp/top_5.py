import pstats

with open("pstats-cumulative.txt", "w") as f:
    p = pstats.Stats("profiling-output", stream=f)
    p.sort_stats("cumulative")
    p.print_stats(5)
