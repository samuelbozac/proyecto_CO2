import RPi.GPIO as GPIO
import time

class Transistor():
    GPIO.setmode(GPIO.BOARD)
    
    def __init__(self, pin):
        self.pin = pin

    def activate(self, output):
        assert self.pin is not None
        assert output is not None
        GPIO.setup(self.pin, GPIO.OUT)

        if(output == "HIGH"):
            GPIO.output(self.pin, GPIO.HIGH)

        if(output == "LOW"):
            GPIO.output(self.pin, GPIO.LOW)

class Puente_h():
    def __init__(self, pin1, pin2):
        self.opener = Transistor(pin = pin1)
        self.closer = Transistor(pin = pin2)
        self.high_opener = self.opener.activate(output = "HIGH")
        self.low_opener = self.opener.activate(output = "LOW")
        self.high_closer = self.closer.activate(output = "HIGH")
        self.low_closer = self.closer.activate(output = "LOW")

    def opens(self, timeout = 3):
        """Function to open the door"""
        self.high_opener
        time.sleep(timeout)
        self.low_opener
        return True