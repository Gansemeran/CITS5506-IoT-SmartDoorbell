import os
import cv2
from .base_camera import BaseCamera

# frontal face classifier
face_cascade = cv2.CascadeClassifier("./webapp/haarcascade_frontalface_alt2.xml")
# downscale factor
ds_factor = 0.6


class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        """If the env parameter OPENCV_CAMERA_SOURCE is defined, sets the camera source to that value,
        else initialises with default first camera detected.
        """
        if os.environ.get("OPENCV_CAMERA_SOURCE"):
            Camera.set_video_source(int(os.environ["OPENCV_CAMERA_SOURCE"]))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        """Sets video source to another camera

        Args:
            source (integer): integer of the desired video source
        """
        Camera.video_source = source

    @staticmethod
    def frames():
        """Yields camera frames and if faces are detected, will detect any faces and outline them on the camera feed

        Raises:
            RuntimeError: If camera could not be started

        Yields:
            Tuple: Camera frame as a jpeg to bytes, and if faces have been detected.
        """
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError("Could not start camera.")

        while True:
            # read current frame
            _, image = camera.read()
            # resize image to make further processing faster
            image = cv2.resize(
                image, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA
            )
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
            if face_rects != ():
                send_email = True
            else:
                send_email = False
            for (x, y, w, h) in face_rects:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            ret, jpeg = cv2.imencode(".jpg", image)
            # encode as a jpeg image and return it
            yield jpeg.tobytes(), send_email
