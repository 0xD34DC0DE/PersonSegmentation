import tensorflow as tf
import time
from data import SegmentationDataset
import matplotlib.pyplot as plt


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
    # msg = tf.constant('TensorFlow 2.0 Hello World')
    # tf.print(msg)

    images_directory = "C:/Users/0xD34DC0DE/Pictures/ASMLGen/output_test/images/person/"
    segmentations_directory = "C:/Users/0xD34DC0DE/Pictures/ASMLGen/output_test/annotations/person/"

    dataset = SegmentationDataset(images_directory, segmentations_directory,
                                  file_id_regex="(\\d*)\\w*\\.").get_dataset()
    print("benchmarking")
    benchmark(dataset)

    i, s = next(iter(dataset))
    plt.imshow(i[0])
    plt.show()
# 8:20 - 11:48
