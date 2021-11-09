from time import sleep
import RPi.GPIO as GPIO

class FanCooler():
    GPIO.setmode(GPIO.BOARD)
    
    def __init__(self, pin):
        self.pin = pin

    def activate(self):
        assert self.pin is not None
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)
    
    def desactivate(self):
        assert self.pin is not None
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)