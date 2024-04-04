"This Module is used to track a face in the frame and follow it with the drone."

import time
from face_tracking.image_drawing_service import ImageDrawingService
from face_tracking.image_compression_service import ImageCompressionService
from face_tracking.recognition_face_identifier import RecognitionFaceIdentifier
from face_tracking.open_cv_wrapper import OpenCvWrapper
from djitellopy import Tello
import logging
import argparse
from face_tracking.utils.positioning_utils import (
    get_box_center_xyz,
    get_distance_xyz,
    get_frame_center_xy,
    get_vector_xyz,
)
from services.tello_command_dispatcher import TelloCommandDispatcher
from services.tello_connector import TelloConnector
from follow_face_controller import FaceFollowingController


args = argparse.ArgumentParser()

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)

# Variables
ZERO_DEPTH_BOX_SIZE = 400
DEPTH_TARGET = 650

open_cv = OpenCvWrapper()

image_compressor = ImageCompressionService(open_cv)

face_identifier = RecognitionFaceIdentifier(open_cv, image_compressor)

image_drawer = ImageDrawingService(open_cv)


tello = Tello()
tello_service = TelloConnector(tello)
tello_service.connect()

tello_service.streamon()

dispatcher = TelloCommandDispatcher(tello_service)

controller = FaceFollowingController()


print("Starting flying in ...")
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

# tello.takeoff()

while True:
    time.sleep(0.200)

    cam_output = tello.get_frame_read()

    frame = cam_output.frame

    if (
        frame is None
        or getattr(frame, "shape") is None
        or frame.shape[0] == 0
        or frame.shape[1] == 0
    ):
        LOGGER.debug("No frame")
        continue

    faces_trbl = face_identifier.identify_faces(frame)
    if not faces_trbl:
        LOGGER.debug("No faces")
        continue

    frame_center_xyz = (*get_frame_center_xy(frame), DEPTH_TARGET)

    closest = None
    for face_trbl in faces_trbl:
        box_center = get_box_center_xyz(face_trbl, DEPTH_TARGET)
        distance = get_distance_xyz(frame_center_xyz, box_center)
        if closest is None or distance < closest[1]:
            closest = (face_trbl, distance, box_center)
        frame = image_drawer.draw_box(
            frame,
            face_trbl,
            "green",
            f"{box_center}",
        )
        frame = image_drawer.draw_cross_hair_in_box(frame, face_trbl, 4, "green")

    assert closest is not None
    closest_box = closest[0]
    closest_distance = closest[1]
    closest_center = closest[2]

    vector_to_center = get_vector_xyz(frame_center_xyz, closest_center)

    frame = image_drawer.draw_box(frame, closest_box, "red")
    frame = image_drawer.draw_frame_center_cross_hair(frame, 2, 20, "red")

    LOGGER.debug(
        f"Closest face at {frame_center_xyz, closest_center} with distance {closest_distance}"
    )

    LOGGER.debug(f"Drone movement {vector_to_center} to center the face in the frame.")

    open_cv.show_image("frame", frame)

    control_state = controller.get_state(vector_to_center)
    dispatcher.send_commands(control_state)

    if open_cv.listen_for_key(1) & 0xFF == ord("q"):
        break

tello_service.streamoff()

print("Landing")
# Land
tello.land()

# End the connection
tello.end()
