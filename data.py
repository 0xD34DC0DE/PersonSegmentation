import re
from glob import glob
from os import path


class SegmentationDataset:

    def __init__(self, images_path: str, segmentations_path: str, file_id_regex: str, batch_size: int = 8,
                 image_size: tuple = (64, 64)):
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
        self.image_segmentation_filepath_pairs = self._group_images_to_segmentations()
        print("yay")

    def _group_images_to_segmentations(self) -> list[tuple[str, str]]:
        """
        Creates a list of tuple from the image and segmentation filenames using the id extracted from their filenames
        using the file_id_regex to create pairs
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

        :param filenames: list of file paths
        :return: list of (file_id, index)
        """
        indexed_file_ids = []

        for index, filename in enumerate(filenames):
            file_id = self.file_id_regex.findall(filename)

            if file_id:
                indexed_file_ids.append((file_id[0], index))

        return indexed_file_ids
