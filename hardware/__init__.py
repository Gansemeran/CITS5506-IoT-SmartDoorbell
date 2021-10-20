# Used to initialise all the hardware

# import everything needed
from picamera import PiCamera
from gpiozero import Button, MotionSensor
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
#from pygame import mixer

# initilise the camera, button and motion sensor
#button = Button("BOARD3") # Number can be set as needed
#pir = MotionSensor("BOARD11")

# det the GPIO numbering mode
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Set pins 11 and 12 as outputs
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)

# We list all the modules we want to import
#__all__ = ['pi_camera', 'pir_motion','servo_control']
__all__ = ['servo_control']