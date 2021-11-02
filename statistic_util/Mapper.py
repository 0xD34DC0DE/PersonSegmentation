from statistic_util import Producer
from os import getpid


class Mapper:
    def __init__(self):
        pass

    def map(self, item, mapping_depth, producer: Producer) -> None:
        # transfer_attr = self._get_transfer(producer)
        # if mapping_depth != 0:
        #     getattr(producer, transfer_attr)
        item = self._process(item)

        next_mapper = producer.get_next_mapper(mapping_depth)
        if next_mapper is None:
            producer.collect(item)
        else:
            #setattr(producer, transfer_attr, item)
            next_mapper.map(item, mapping_depth + 1, producer)

    @staticmethod
    def _get_transfer(producer: Producer) -> str:
        transfer_str = f'transfer{getpid()}'
        if not hasattr(producer, transfer_str):
            setattr(producer, transfer_str, None)
        return transfer_str

    @staticmethod
    def _process(item):
        raise NotImplementedError
