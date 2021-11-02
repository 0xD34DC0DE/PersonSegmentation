from __future__ import annotations

from statistic_util import Mapper
import multiprocessing


class Producer:

    def __init__(self, producer_impl: Producer, items: list):
        self._mappers: list[Mapper] = []
        self._results = []
        self._items = []
        self._producer_impl: Producer = producer_impl
        self._lock: multiprocessing.Lock = multiprocessing.Lock()
        # Most modern system use virtual cores (aka hyperthreading) but compute heavy tasks wont benefit from this,
        # so divide the available number of cores by two to get the physical core count
        self._thread_count = multiprocessing.cpu_count() // 2
        self._add_transfer_attributes(self._thread_count)

    def _add_transfer_attributes(self, attribute_count: int):
        for i in range(attribute_count):
            setattr(self, f'transfer{i}', any)

    def get_next_mapper(self, mapping_depth) -> Mapper:
        if mapping_depth == len(self._mappers) - 1:
            return None
        else:
            return self._mappers[mapping_depth + 1]

    def collect(self, result):
        self._lock.acquire()
        self._results.append(result)
        self._lock.release()

    def next_item(self):
        self._lock.acquire()
        for item in self._items:
            self._lock.release()
            yield self._producer_impl._produce_item(item)

    def map(self, mapper: Mapper) -> Producer:
        self._mappers.append(mapper)
        return self

    @staticmethod
    def _produce_item(self, item):
        raise NotImplementedError("_produce_item needs to be implemented")
