from abc import ABC, abstractmethod
from typing import Sequence
import cv2


class AbstractFaceIdentifier(ABC):

    @abstractmethod
    def identify_faces(self, image: cv2.Mat) -> Sequence[cv2.typing.Rect]:
        """
        Detect faces in the given frame using the specified image compression factor.

        Args:
            image: A frame containing the faces to be detected.

        Returns:
            List[Tuple[int, int, int, int]]:
                A list of tuples containing the face bounding box coordinates
                (top, right, bottom, left) for each detected face.
        """
        pass
