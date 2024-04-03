import cv2
import numpy as np

# Parameters
CANNY_THRESHOLD_1 = 50
CANNY_THRESHOLD_2 = 150
CANNY_APERTURE_SIZE = 3
HOUGH_RHO = 1
HOUGH_THETA = np.pi / 180
HOUGH_THRESHOLD = 100
LINE_COLOR = (0, 0, 255)
LINE_THICKNESS = 2


class LineDetector:
    """
    A class that detects lines in an image using the Hough transform.
    """

    def detect_lines(self, img: cv2.typing.MatLike):
        """
        Detects lines in the given image and displays the result.

        Args:
            img: The input image in BGR format.

        Returns:
            None
        """
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply Canny edge detection
        edges = cv2.Canny(
            blurred,
            CANNY_THRESHOLD_1,
            CANNY_THRESHOLD_2,
            apertureSize=CANNY_APERTURE_SIZE,
        )

        # Apply Hough Line Transform
        lines = cv2.HoughLines(edges, HOUGH_RHO, HOUGH_THETA, HOUGH_THRESHOLD)

        # Draw lines on the image
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                cv2.line(img, (x1, y1), (x2, y2), LINE_COLOR, LINE_THICKNESS)

        cv2.imshow("Detected Lines", img)
        cv2.waitKey(0)


# Usage example
if __name__ == "__main__":
    import os

    # Get the absolute path of the script
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    # Specify the relative path of the image file
    image_path = "lines.png"

    # Construct the absolute path of the image file
    absolute_path = os.path.join(script_dir, image_path)

    detector = LineDetector()

    # Read image using the absolute path
    img = cv2.imread(absolute_path, cv2.IMREAD_COLOR)
    detector.detect_lines(img)
