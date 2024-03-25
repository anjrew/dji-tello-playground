from typing import cast
import cv2
import numpy as np
from numpy.typing import NDArray


class CircleDetector:
    """
    A class that detects circles in an image using the Hough transform.
    """

    def detect_circles(self, img: cv2.typing.MatLike):
        """
        Detects circles in the given image and displays the result.

        Args:
            img: The input image in BGR format.

        Returns:
            None
        """
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Blur using 3 * 3 kernel
        gray_blurred = cv2.blur(gray, (3, 3))

        # Apply Hough transform on the blurred image
        detected_circles = cv2.HoughCircles(
            gray_blurred,
            cv2.HOUGH_GRADIENT,
            1,
            20,
            param1=50,
            param2=30,
            minRadius=1,
            maxRadius=40,
        )

        # Draw circles that are detected
        if detected_circles is not None:
            # Convert the circle parameters a, b, and r to integers
            detected_circles = cast(NDArray[np.float32], detected_circles)
            detected_circles = cast(
                NDArray[np.uint16], np.uint16(np.around(detected_circles))
            )

            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]

                # Draw the circumference of the circle
                cv2.circle(img, (a, b), r, (0, 255, 0), 2)

                # Draw a small circle (of radius 1) to show the center
                cv2.circle(img, (a, b), 1, (0, 0, 255), 3)

            cv2.imshow("Detected Circle", img)
            cv2.waitKey(0)


# Usage example
if __name__ == "__main__":
    import os

    # Get the absolute path of the script
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    # Specify the relative path of the image file
    image_path = "circles.jpg"

    # Construct the absolute path of the image file
    absolute_path = os.path.join(script_dir, image_path)

    detector = CircleDetector()

    # Read image using the absolute path
    img = cv2.imread(absolute_path, cv2.IMREAD_COLOR)

    detector.detect_circles(img)
