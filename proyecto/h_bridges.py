# import RPi.GPIO as GPIO
import time
import gpiozero

# class Transistor():
#     GPIO.setmode(GPIO.BOARD)
    
#     def __init__(self, pin):
#         self.pin = pin

#     def activate(self, output):
#         assert self.pin is not None
#         assert output is not None
#         GPIO.setup(self.pin, GPIO.OUT)

#         if(output == "HIGH"):
#             GPIO.output(self.pin, GPIO.HIGH)

#         elif(output == "LOW"):
#             GPIO.output(self.pin, GPIO.LOW)

class H_Bridges():
    def __init__(self, pin1, pin2):
        self.opener = gpiozero.OutputDevice(pin1, active_high=True, initial_value=False)
        self.opener = gpiozero.OutputDevice(pin1, active_high=True, initial_value=False)
        self.high_opener = self.opener.on()
        self.low_opener = self.opener.off()
        self.high_closer = self.closer.on()
        self.low_closer = self.closer.off()

    def opens(self, timeout = 3):
        """Function to open the door"""
        self.high_opener
        time.sleep(timeout)
        self.low_opener
        return True

    def close(self, timeout):
        """Function to close the doors"""
        self.high_closer
        time.sleep(timeout)
        self.low_closer
        return True