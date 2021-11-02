from __future__ import annotations

import concurrent
from concurrent import futures

from statistic_util import Mapper
import threading
from multiprocessing import cpu_count
import traceback
import logging

class Producer:

    def __init__(self, producer_impl: Producer, items: list):
        self._mappers: list[Mapper] = []
        self._results = []
        self._items = items
        self._producer_impl: Producer = producer_impl
        self._iter_lock: threading.Lock = threading.Lock()
        self._result_lock: threading.Lock = threading.Lock()
        # Most modern system use virtual cores (aka hyperthreading) but compute heavy tasks wont benefit from this,
        # so divide the available number of cores by two to get the physical core count
        self._thread_count = cpu_count() // 2

    def get_next_mapper(self, mapping_depth) -> Mapper:
        if mapping_depth == len(self._mappers) - 1:
            return None
        else:
            return self._mappers[mapping_depth + 1]

    @staticmethod
    def _call_first_mapper(self, item):
        return self._mappers[0].map(item, 0, self)

    def collect(self, result):
        with self._result_lock:
            self._results.append(result)

    def _next_item(self):
        for item in self._items:
            yield item

    def map(self, mapper: Mapper) -> Producer:
        self._mappers.append(mapper)
        return self

    def get_result(self):
        if not self._results:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_list = []
                for item in self._next_item():
                    future_list.append(
                        executor.submit(self._mappers[0].map, mapping_depth=0, producer=self, item=item)
                    )

                for future in future_list:
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(traceback.format_exc())

                # executor.map(self._call_first_mapper, self)
        return self._results

    @staticmethod
    def _produce_item(self, item):
        raise NotImplementedError("_produce_item needs to be implemented")
