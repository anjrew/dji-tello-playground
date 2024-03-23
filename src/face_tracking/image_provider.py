import logging
import cv2
from open_cv_wrapper import OpenCvWrapper

LOGGER = logging.getLogger(__name__)


class ImageProvider:

    def __init__(
        self, open_cv: OpenCvWrapper, compression: int = 4, headless: bool = False
    ):
        LOGGER.debug(
            f"Initializing ImageProvider {'in headless mode' if headless else ''} with compression {compression}"
        )
        self.compression = compression
        self.open_cv = open_cv
        self.open_cv.set_show_directly(False if headless else True)

    def connect_to_camera(self, id: int = 0):
        self.cap = self.open_cv.connect_to_camera(id)

    def get_image(self) -> cv2.typing.MatLike:
        if not self.cap.isOpened():
            raise Exception("Camera is not connected")

        compression = self.compression
        _, frame = self.cap.read()
        # Get the image height and width

        compressed_image = self.open_cv.resize(
            frame, (0, 0), fx=1 / compression, fy=1 / compression
        )

        return compressed_image
