import cv2
from open_cv_wrapper import OpenCvWrapper


class ImageCompressionService:

    def __init__(self, open_cv: OpenCvWrapper):
        self.open_cv = open_cv

    def compress_image(
        self, frame: cv2.typing.MatLike, image_compression: int
    ) -> cv2.typing.MatLike:
        compressed_image = self.open_cv.resize(
            frame, (0, 0), fx=1 / image_compression, fy=1 / image_compression
        )
        return compressed_image

    def decompress_image(
        self, frame: cv2.typing.MatLike, image_compression: int
    ) -> cv2.typing.MatLike:
        decompressed_image = self.open_cv.resize(
            frame, (0, 0), fx=image_compression, fy=image_compression
        )
        return decompressed_image
