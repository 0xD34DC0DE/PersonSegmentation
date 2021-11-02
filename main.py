import time
from dataset.data import SegmentationDataset
import matplotlib.pyplot as plt
import statistic_util
import tensorflow as tf
from statistic_util.BinaryRatio import BinaryRatio
from statistic_util.DirectoryIterator import DirectoryIterator
from statistic_util.LoadImage import LoadImage


def benchmark(dataset, num_epochs=1):
    start_time = time.perf_counter()
    for epoch_num in range(num_epochs):
        i = 0
        for sample in dataset:
            i += 1
            if i % 20 == 0:
                print("sample #" + str(i))
            # Performing a training step
            time.sleep(0.01)
            if i == 300:
                break
    print("Execution time:", time.perf_counter() - start_time)


if __name__ == '__main__':
    tf.print(tf.__version__)

    images_directory = "C:/Users/0xD34DC0DE/Pictures/ASMLGen/output_test/images/person/"
    segmentations_directory = "C:/Users/0xD34DC0DE/Pictures/ASMLGen/output_test/annotations/person/"

    dir_iter = DirectoryIterator(images_directory).map(LoadImage()).map(BinaryRatio())
    print(dir_iter.__dir__())
    start_time = time.perf_counter()
    result = dir_iter.get_result()
    print("Execution time:", time.perf_counter() - start_time)
    print(len(result))

    # i = 0
    # start_time = time.perf_counter()
    # for img in dir_iter:
    #     i += 1
    #     if i % 1000 == 0:
    #         print(i)
    # print("Execution time:", time.perf_counter() - start_time)
    # dataset = SegmentationDataset(images_directory, segmentations_directory,
    #                               file_id_regex="(\\d*)\\w*\\.").get_dataset()
    # print("benchmarking")
    # benchmark(dataset)
    #
    # i, s = next(iter(dataset))
    # plt.imshow(i[0])
    # plt.show()
# 8:20 - 11:48
