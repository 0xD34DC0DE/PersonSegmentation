from __future__ import annotations

from statistic_util import Mapper
import multiprocessing


class Producer:

    def __init__(self):
        self.mappers: list[Mapper] = []
        self.result = None
        self.items = []
        self.lock: multiprocessing.Lock = multiprocessing.Lock()
        # Most modern system use virtual cores (aka hyperthreading) but compute heavy tasks wont benefit from this,
        # so divide the available number of cores by two to get the physical core count
        self.thread_count = multiprocessing.cpu_count() // 2
        self.add_transfer_attributes(self.thread_count)

    def add_transfer_attributes(self, attribute_count: int):
        for i in range(attribute_count):
            setattr(self, f'transfer{i}', any)

    def collect(self):
        pass

    def produce(self):
        self.lock.acquire()
        for item in self.items:
            self.lock.release()
            yield item

    def map(self, mapper: Mapper) -> Producer:
        self.mappers.append(mapper)
        return self