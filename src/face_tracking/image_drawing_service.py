from typing import Dict, Tuple, Union
import cv2
import numpy as np

try:
    from open_cv_wrapper import OpenCvWrapper
except ModuleNotFoundError:
    from face_tracking.open_cv_wrapper import OpenCvWrapper


class ImageDrawingService:
    def __init__(self, open_cv_wrapper: OpenCvWrapper):
        self.open_cv = open_cv_wrapper
        self._color_map: Dict[str, Tuple[int, int, int]] = {
            "red": (0, 0, 255),
            "green": (
                0,
                255,
                0,
            ),
            "blue": (255, 0, 0),
            "yellow": (0, 255, 255),
            "magenta": (
                255,
                0,
                255,
            ),
            "cyan": (255, 255, 0),
            "white": (
                255,
                255,
                255,
            ),
            "black": (
                0,
                0,
                0,
            ),
        }

    def draw_box(
        self,
        frame: np.ndarray,
        target: Union[cv2.typing.Rect, Tuple[int, int, int, int]],
        color: str,
        label: str = "",
    ) -> np.ndarray:
        top, right, bottom, left = target
        color_tuple = self._color_map[color]
        self.open_cv.rectangle(frame, (left, top), (right, bottom), color_tuple, 2)
        if label:
            self.open_cv.rectangle(
                frame,
                (left, bottom - 35),
                (right, bottom),
                color_tuple,
                cv2.FILLED,
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            box_width = right - left
            _, frame_width = frame.shape[:2]
            font_scale = (box_width / frame_width) + 1
            font_size = 0.4
            scaled_font = font_size * (font_scale**3)
            self.open_cv.write_text(
                frame,
                label,
                (left + 6, bottom - 6),
                font,
                scaled_font,
                (255, 255, 255),
                1,
            )

        return frame

    def draw_frame_center_cross_hair(
        self,
        frame: np.ndarray,
        cross_hair_thickness: int,
        cross_hair_length: int,
        color: str,
    ) -> np.ndarray:

        # Get the image dimensions
        height, width = frame.shape[:2]
        # Calculate the center of the image
        center_x, center_y = width // 2, height // 2
        color_tuple = self._color_map[color]
        cv2.line(
            frame,
            (center_x - cross_hair_length, center_y),
            (center_x + cross_hair_length, center_y),
            color_tuple,
            cross_hair_thickness,
        )
        # Draw a red vertical line through the center
        cv2.line(
            frame,
            (center_x, center_y - cross_hair_length),
            (center_x, center_y + cross_hair_length),
            color_tuple,
            cross_hair_thickness,
        )
        return frame

    def draw_cross_hair_in_box(
        self,
        frame: np.ndarray,
        box: Union[
            Tuple[int, int, int, int], cv2.typing.Rect
        ],  # (top, left, bottom, right)
        cross_hair_size: int,
        color: str,
    ) -> np.ndarray:
        """
        Draws a crosshair in a specified box within the frame.
        Assumes box is given as (top, left, bottom, right).
        """
        top, left, bottom, right = box
        # Calculate center of the box
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        color_tuple = self._color_map[color]

        # Ensure cross_hair_size is appropriately scaled to fit within the box if necessary
        cross_hair_length = min(cross_hair_size, right - left, bottom - top)

        # Draw horizontal line across the center
        cv2.line(
            frame,
            (center_x - cross_hair_length // 2, center_y),
            (center_x + cross_hair_length // 2, center_y),
            color_tuple,
            thickness=1,  # Adjust thickness as necessary
        )

        # Draw vertical line across the center
        cv2.line(
            frame,
            (center_x, center_y - cross_hair_length // 2),
            (center_x, center_y + cross_hair_length // 2),
            color_tuple,
            thickness=1,  # Adjust thickness as necessary
        )

        return frame
