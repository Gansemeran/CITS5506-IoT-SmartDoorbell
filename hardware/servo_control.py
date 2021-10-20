""" https://www.explainingcomputers.com/sample_code/Servo_Test_DD_Two_Servos.py
https://www.explainingcomputers.com/sample_code/Servo_Test_CC_Go_to_Angle.py"""
from pygame import mixer
import RPi.GPIO as GPIO
from time import sleep

# load the sound files for voice msg
mixer.init()
door_open = mixer.Sound("sound/door_open_msg.wav")
door_lock = mixer.Sound("sound/door_lock_msg.wav")
box_open = mixer.Sound("sound/box_open_msg.wav")
box_lock = mixer.Sound("sound/box_lock_msg.wav")


def door_servo():
    """Unlocks and relocks servo connected to pin 11, the door"""
    # Set pins 11 as outputs, and define as PWM servo1 for door controlling
    servo1 = GPIO.PWM(11, 50)  # pin 11 for servo1

    # Start PWM running, value of 0 (pulse off)
    servo1.start(0)
    # Start servo at 0 degree
    servo1.ChangeDutyCycle(2)

    servo1.ChangeDutyCycle(
        2 + (90 / 18)
    )  # Turn the servo arm to 90 degrees, angle to be adjusted according to needs
    sleep(0.5)
    servo1.ChangeDutyCycle(0)
    door_open.play()
    sleep(10)  # Time gap waiting for visitor to open the door, can be changed
    servo1.ChangeDutyCycle(2)  # Switch the angle back to 0
    sleep(0.5)
    servo1.ChangeDutyCycle(0)
    door_lock.play()


def box_servo():
    """Unlocks and relocks servo connected to pin 12, the box"""
    # Set pins 12 as outputs, and define as PWM servo2 for box controlling
    servo2 = GPIO.PWM(12, 50)  # pin 12 for servo2
    # Start PWM running, value of 0 (pulse off)
    servo2.start(0)
    # Start servo at 0 degree
    servo2.ChangeDutyCycle(2)
    servo2.ChangeDutyCycle(
        2 + (90 / 18)
    )  # Turn the servo arm to 90 degrees, angle to be adjusted according to needs
    sleep(0.5)
    servo2.ChangeDutyCycle(0)
    box_open.play()
    sleep(10)  # Time gap waiting for visitor to open the door, can be changed
    servo2.ChangeDutyCycle(2)  # Switch the angle back to 0
    sleep(0.5)
    servo2.ChangeDutyCycle(0)
    box_lock.play()


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    box_servo()
