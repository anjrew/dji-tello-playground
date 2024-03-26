import cv2
from open_cv_wrapper import OpenCvWrapper


class ImageCompressionService:
    """
    A class that provides image compression and decompression functionality.
    """

    def __init__(self, open_cv: OpenCvWrapper):
        self._open_cv = open_cv

    def compress_image(
        self, frame: cv2.typing.MatLike, image_compression: int
    ) -> cv2.typing.MatLike:
        """
        Compresses the given image frame.

        Args:
            frame (cv2.typing.MatLike): The image frame to be compressed.
            image_compression (int): The compression factor to be applied.

        Returns:
            cv2.typing.MatLike: The compressed image frame.
        """
        compressed_image = self._open_cv.resize(
            frame, (0, 0), fx=1 / image_compression, fy=1 / image_compression
        )
        return compressed_image

    def decompress_image(
        self, frame: cv2.typing.MatLike, image_compression: int
    ) -> cv2.typing.MatLike:
        """
        Decompresses the given image frame.

        Args:
            frame (cv2.typing.MatLike): The image frame to be decompressed.
            image_compression (int): The decompression factor to be applied.

        Returns:
            cv2.typing.MatLike: The decompressed image frame.
        """
        decompressed_image = self._open_cv.resize(
            frame, (0, 0), fx=image_compression, fy=image_compression
        )
        return decompressed_image
