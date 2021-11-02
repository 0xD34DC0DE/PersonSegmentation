from statistic_util.Mapper import Mapper

import numpy as np


class BinaryRatio(Mapper):

    def __init__(self):
        super().__init__()

    def _process(self, item):
        return len(item)
