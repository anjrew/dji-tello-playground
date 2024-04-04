from typing import Sequence

import cv2

try:
    from open_cv_wrapper import OpenCvWrapper
    from face_identifier import AbstractFaceIdentifier
except ModuleNotFoundError:
    from face_tracking.open_cv_wrapper import OpenCvWrapper
    from face_tracking.face_identifier import AbstractFaceIdentifier


class OpenCvFaceIdentifier(AbstractFaceIdentifier):
    def __init__(self, open_cv: OpenCvWrapper):
        self._face_cascade = open_cv.get_face_classifier()
        self.open_cv = open_cv

    def identify_faces(self, image: cv2.typing.MatLike) -> Sequence[cv2.typing.Rect]:
        gray = self.open_cv.convert_rgb_image_to_gray(image)
        faces = self._face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces
