from abc import ABC, abstractmethod
from typing import Sequence
import cv2


class AbstractFaceIdentifier(ABC):
    """
    Abstract base class for face identifier implementations.

    This class defines the interface for identifying faces in an image.
    """

    @abstractmethod
    def identify_faces(self, image: cv2.Mat) -> Sequence[cv2.typing.Rect]:
        """
        Detect faces in the given frame.

        Args:
            image: A frame containing the faces to be detected.

        Returns:
            List[Tuple[int, int, int, int]]:
                A list of tuples containing the face bounding box coordinates
                (top, right, bottom, left) for each detected face.
        """
