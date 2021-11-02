import re
from glob import glob
from os import path

import tensorflow as tf


class SegmentationDataset:

    def __init__(self, images_path: str, segmentations_path: str, file_id_regex: str, batch_size: int = 8,
                 image_size: tuple = (64, 64), resize_interpolation='bicubic', resize_fill_mode='reflect'):
        """
        Creates a binary segmentation dataset from images and their matching segmentations

        :param images_path: string path of the image directory
        :param segmentations_path: string path of the segmentation directory
        :param file_id_regex: regex string used to extract the id in the file name
        :param batch_size: size of the batches to generate
        :param image_size: size to resize the images to
        """
        self.images_path = path.dirname(images_path)
        self.segmentations_path = path.dirname(segmentations_path)
        self.batch_size = batch_size
        self.image_size = image_size
        self.file_id_regex = re.compile(file_id_regex)
        self.resize_interpolation = resize_interpolation

        self.image_segmentation_filepath_pairs = self._group_images_to_segmentations()
        self.dataset = self._create_dataset()

    def _group_images_to_segmentations(self) -> list[tuple[str, str]]:
        """
        Creates a list of tuple from the image and segmentation filenames using the id extracted from their filenames
        using the file_id_regex to create pairs
        :return: [(image_path, segmentation_path)]
        """
        images_filenames, segmentation_filenames = self._list_file_names()

        image_indexed_file_ids: list[tuple[str, int]] = self._extract_indexed_file_id(images_filenames)
        segmentation_indexed_file_ids = self._extract_indexed_file_id(segmentation_filenames)

        image_segmentation_pairs: list[tuple[str, str]] = []

        for image_file_id, image_index in image_indexed_file_ids:
            segmentation_indexed_file_id = segmentation_indexed_file_ids[image_index]

            assert segmentation_indexed_file_id[0] == image_file_id, \
                "Mismatch between image id and segmentation, \
                make sure that all images have a corresponding segmentation"

            segmentation_filepath = segmentation_filenames[segmentation_indexed_file_id[1]]
            image_filepath = images_filenames[image_index]
            image_segmentation_pairs.append((image_filepath, segmentation_filepath))

        return image_segmentation_pairs

    def _list_file_names(self) -> tuple[list[str], list[str]]:
        """
        List all filenames of the images and segmentations folders

        :return (image_filenames, segmentation_filenames)
        """
        image_filenames = glob(self.images_path + '/*')
        segmentation_filenames = glob(self.segmentations_path + '/*')
        return image_filenames, segmentation_filenames

    def _extract_indexed_file_id(self, filenames: list[str]) -> list[tuple[str, int]]:
        """
        Extract the file ids from the file paths and add the current index of the element to the tuple
        :param filenames: list of file paths
        :return: list of (file_id, index)
        """
        indexed_file_ids = []

        for index, filename in enumerate(filenames):
            file_id = self.file_id_regex.findall(filename)

            if file_id:
                indexed_file_ids.append((file_id[0], index))

        return indexed_file_ids

    def _create_dataset(self):
        """
        Create a tf.data dataset with the list of files
        """
        file_pairs_tensor = tf.convert_to_tensor(self.image_segmentation_filepath_pairs)
        dataset = tf.data.Dataset.from_tensor_slices(file_pairs_tensor)
        dataset = dataset.map(self._load_images)
        dataset = dataset.batch(self.batch_size)  # Auto tune ?
        return dataset

    def _load_images(self, file_pairs: tuple[str, str]):
        """

        :param file_pairs:
        :return:
        """
        image_file = tf.io.read_file(file_pairs[0])
        segmentation_file = tf.io.read_file(file_pairs[1])

        image = tf.image.decode_jpeg(image_file, channels=3)
        segmentation = tf.image.decode_jpeg(segmentation_file, channels=3)

        image = tf.cast(image, tf.float32) * (1.0 / 255.0)
        segmentation = tf.cast(segmentation, tf.float32) * (1.0 / 255.0)

        image = tf.image.resize(image, size=self.image_size, method=self.resize_interpolation, antialias=False)
        segmentation = tf.image.resize(segmentation, size=self.image_size, method=self.resize_interpolation,
                                       antialias=False)

        return image, segmentation

    def get_dataset(self):
        return self.dataset
