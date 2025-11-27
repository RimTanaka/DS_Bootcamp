import cProfile
import pstats

cProfile.run("import financial; financial.fetch_financial_data('MSFT', 'Total Revenue')", "profiling-output")

with open("profiling-sleep.txt", "w") as f:
    p = pstats.Stats("profiling-output", stream=f)
    p.sort_stats("tottime").print_stats()
