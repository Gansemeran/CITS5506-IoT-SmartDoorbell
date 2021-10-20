from datetime import datetime, timedelta
from flask_mail import Message
from . import sms_service

time_of_last_email = datetime.min
email_delay = timedelta(minutes=3)
doorbell = False


def send_mail(app, Mail, image, force):
    """Sends email, with attached email, using given app context and mail object, will not send more than 1 email more than every 3 minutes
    Will also send sms notification.

    Args:
        app (Flask): the Flask application that the mail object is tied to
        Mail (Flask-Mail): Flask-Mail instance that the mail should be sent with
        image (image/jpeg): the image to attach to the email
    """
    with app.app_context():
        global time_of_last_email
        if (datetime.now() - time_of_last_email) > email_delay or force:
            global doorbell
            doorbell = False
            time_of_last_email = datetime.now()
            # send sms
            sms_service.send_sms_bad()
            # send email
            msg = Message(
                "Doorbell has Detected a Person",
                sender="PLACEHOLDER@example.com",
                recipients=["PLACEHOLDER@example.com"],
            )
            msg.html = """<p>Hello User,
            A person has been detected by the doorbell, please review attachment for information.
            Go to <a href="http://127.0.0.1:5000/">Doorbell Viewer</a> for additional actions.</br></p><img src='cid:Image'>"""
            msg.attach(
                "image.jpeg",
                "image/jpeg",
                image,
                "inline",
                headers=[["Content-ID", "<Image>"]],
            )

            Mail.send(msg)


def check_doorbell():
    global doorbell
    return doorbell


def doorbell_rung():
    global doorbell
    doorbell = True
