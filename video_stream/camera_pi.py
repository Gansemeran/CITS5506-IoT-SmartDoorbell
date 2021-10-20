import time
import picamera
import cv2
from base_camera import BaseCamera

face_cascade = cv2.CascadeClassifier("./webapp/haarcascade_frontalface_alt2.xml")
ds_factor = 0.6


class Camera(BaseCamera):
    @staticmethod
    def frames():
        """Yields camera frames and if faces are detected, will detect any faces and outline them on the camera feed

        Yields:
            Tuple: Camera frame as a jpeg to bytes, and if faces have been detected.
        """
        with picamera.PiCamera() as camera:
            camera.resolution = (1280, 720)
            camera.framerate = 30
            rawCapture = picamera.array.PiRGBArray(camera, size=(1280, 720))
            # let camera warm up
            time.sleep(0.5)
            for frame in camera.capture_continuous(
                rawCapture, "bgr", use_video_port=True
            ):
                # return current frame
                image = frame.array
                image = cv2.resize(
                    image,
                    None,
                    fx=ds_factor,
                    fy=ds_factor,
                    interpolation=cv2.INTER_AREA,
                )
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
                if face_rects != ():
                    send_email = True
                else:
                    send_email = False
                for (x, y, w, h) in face_rects:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # break
                ret, jpeg = cv2.imencode(".jpg", image)
                yield jpeg.tobytes(), send_email
                rawCapture.truncate(0)
