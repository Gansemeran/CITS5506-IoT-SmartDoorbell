"""Part of the code is from Youtube video "How to use Active Buzzer with Arduino& Raspberry Pi" by SunFounder
    Maker Education and also inspired by "Python Programming Tutorial: Getting Started
    with the Raspberry Pi" fron Sparkfun website.
    The wav file is downloaded from "wavsource.com/sfx/sfx2.htm" - Doorbell 2
    The following commented out command lines are needed to install pygame library"""
# sudo apt-get update
# sudo apt-get install python3-pygame

from pygame import mixer
import RPi.GPIO as GPIO
import time
from webapp.email_service import doorbell_rung

# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
button = 3  # pin number for the button
# mixer.init()
sound = mixer.Sound("./sound_effect/doorbell2.wav")
gap = 2  # time gap between 2 rings


def ring(placeholder=None):
    """Plays the doorbell ring 3 times"""
    doorbell_rung()
    sound.play()
    time.sleep(gap)
    sound.play()
    time.sleep(gap)
    sound.play()


def loop():
    """Continuous polling method of detecting falling edge"""
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        if GPIO.input(button) == GPIO.LOW:
            ring()


def setup():
    """Attach ring interrupt to button pin on falling edge"""
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # change GPIO.FALLING to GPIO.RISING depending on how we have it wired up
    GPIO.add_event_detect(button, GPIO.FALLING, bouncetime=5000, callback=ring)


if __name__ == "__main__":
    """For testing purposes, will not execute when imported"""
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
