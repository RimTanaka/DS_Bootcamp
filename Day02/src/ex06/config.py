"""
Файл конфигурации

Можно задать количество предугадываемых шагов{NUM_OF_STEPS}\
        конечный текст report{REPORT_TEMPLATE}/Уровень логирования{level}
"""

import logging

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(
        filename='analytics.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)
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
