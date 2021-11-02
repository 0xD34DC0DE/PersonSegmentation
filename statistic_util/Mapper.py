from statistic_util import Producer


class Mapper:
    def __init__(self):
        pass

    def map(self, mapper_id, mapping_depth, producer: Producer):
        transfer_attr = self._get_transfer(mapper_id)
        item = producer.next_item() if mapping_depth == 0 else getattr(producer, transfer_attr)
        item = self._process(item)

        next_mapper = producer.get_next_mapper(mapping_depth)
        if next_mapper is None:
            producer.collect(item)
        else:
            setattr(producer, transfer_attr, item)
            next_mapper(mapper_id, mapping_depth + 1, producer)

    @staticmethod
    def _get_transfer(mapper_id) -> str:
        return f'transfer{mapper_id}'

    @staticmethod
    def _process(item):
        raise NotImplementedError
