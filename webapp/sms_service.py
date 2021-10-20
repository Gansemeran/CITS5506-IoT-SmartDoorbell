from urllib import request, parse
from twilio.rest import Client

send_message = False
text_body = "Someone has been detected at your door. Please see your email for more details.\n\nControl your door at http://127.0.0.1:5000"

# Good quality SMS message but we only have about 35 free sms codes, so don't use unless neccesary
password = "PLACEHOLDER"


def send_sms_good(text_body=text_body, phone_number=None):
    """Sends text message with the given text body to the given phone number using gtnotify.

    Args:
        text_body (str, optional): SMS body to send. Defaults to text_body.
        phone_number (str, optional): Phone number to send to.
    """
    if send_message:
        s = (
            "https://sms.gtnotify.com/api/sendsms.php/?username=PLACEHOLDER&pass="
            + password
            + "&sender=SmartDoor"
            + "&smstext="
            + parse.quote_plus(text_body)
            + "&gsm="
            + phone_number
        )
        print(request.urlopen(s).read())


# SMS messages that don't have good formatting, but we have 300 text messages.
account_sid = "NONE"
auth_token = "NONE"


def send_sms_bad(text_body=text_body, phone_number=None):
    """Sends text message with the given text body to the given phone number using twilio.

    Args:
        text_body (str, optional): SMS body to send. Defaults to text_body.
        phone_number (str, optional): Phone number to send to.
    """
    if send_message:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            messaging_service_sid="PLACEHOLDER",
            body=text_body,
            to=phone_number,
        )
