"""
Файл конфигурации, можно задать количество предугадываемых шагов{NUM_OF_STEPS}\
 и конечный текст report{REPORT_TEMPLATE}
"""

NUM_OF_STEPS = 3
REPORT_TEMPLATE = """
Report
We have made {count_observations} \
observations from tossing a coin: {tails_count} \
of them were tails and {heads_count} of them were heads.
The probabilities are {tail_fraction:.2f}% and {head_fraction:.2f}%\
, respectively.
Our forecast is that in the next {pred_steps} \
observations we will have: {pred_tails} tail and {pred_heads} heads.
"""
