import tensorflow as tf

from data import SegmentationDataset

if __name__ == '__main__':
    # msg = tf.constant('TensorFlow 2.0 Hello World')
    # tf.print(msg)

    images_directory = "C:/Users/0xD34DC0DE/Pictures/ASMLGen/output_test/images/person/"
    segmentations_directory = "C:/Users/0xD34DC0DE/Pictures/ASMLGen/output_test/annotations/person/"

    dataset = SegmentationDataset(images_directory, segmentations_directory, file_id_regex="(\\d*)\\w*\\.")

#8:20 - 11:48