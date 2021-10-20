# required flask web server imports
from flask import Flask, render_template, Response

# check to see if this code is running on raspberry pi
import platform

if platform.machine() == "armv7l":
    print("This is running on a raspberry pi")
    raspberry_pi = True
    from hardware import *
    from sound_effect import doorbell_ring

    doorbell_ring.setup()
else:
    raspberry_pi = False

# mail service for flask
from flask_mail import Mail


# will attempt to import and init pi camera, if it fails (pi camera no available/attached etc.)
# will instead load opencv camera which will auto initialise first camera connected
try:
    from video_stream.camera_pi import Camera
except:
    from video_stream.camera_ocv import Camera

# email send functions
from . import email_service
import threading
import time

# wrapper function on creating the app to make testing simpler, when executing flask run will automatically call this function
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # configure the mail service defaults
    app.config["MAIL_SERVER"] = "smtp.example.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = "PLACEHOLDER@example.com"
    app.config["MAIL_PASSWORD"] = "!PLACEHOLDER!"
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    mail = Mail(app)

    def gen(camera):
        """Given an instance of a Camera class, will continually call the get_frame method, and send an email if the frame returns a detected face.
        yields a formatted byte string of the frame for sending over a HTTP response.

        Args:
            camera (Camera): instance of the Camera class

        Yields:
            byte string: formatted string to send as a HTTP response for an image
        """
        while True:
            frame, send_email = camera.get_frame()
            if send_email or email_service.check_doorbell():
                # pass email to another thread so it doesnt lag the server so much
                thread = threading.Thread(
                    target=email_service.send_mail,
                    args=(app, mail, frame, email_service.check_doorbell()),
                )
                thread.start()
            yield (
                b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )

    def back_gen():
        """Background camera thread, to continuously retrieve frames to check if a face has been detected and to send an email"""
        for _ in gen(Camera()):
            time.sleep(1)

    @app.before_first_request
    def before_first():
        """Before first is to set up any background tasks that are required, such as background camera notifications"""
        print("Set up finished")
        thread = threading.Thread(target=back_gen)
        thread.daemon = True
        thread.start()

    @app.route("/")
    def index():
        """Landing page route index page

        Returns:
            HTML: rendered HTMl template of the index page
        """
        return render_template("index.html")

    @app.route("/video")
    def video():
        """API route for the raw video feed, meant to be embedded in the webpage

        Returns:
            HTTP Response: The generated camera frame as well as mimetype
        """
        # COMMENT OUT THE FIRST LINE WHEN DEVELOPING
        # OPENCV CRASHES SERVER WHEN IT AUTORELOADS

        return Response(
            gen(Camera()),
            # gen(video_stream.VideoCamera()),
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )

    @app.route("/video/download")
    def download_image():
        """API route to download a single frame of the camera

        Returns:
            HTTP Response: image/jpg of the current camera frame
        """
        return Response(Camera().get_frame()[0], mimetype="image/jpg")

    # the 'message' parameter changes based on which button is clicked
    @app.route("/button_press/<message>")
    def button_press(message):
        """API route for button presses on the website

        Args:
            message (string): the button that was pressed

        Returns:
            string: returns empty string
        """
        if raspberry_pi:
            print(message)
            if message == "Open Door":
                servo_control.door_servo()
            elif message == "Open Box":
                threading.Thread(target=servo_control.box_servo()).start()
        return ""

    return app
