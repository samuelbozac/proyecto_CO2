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

class H_Bridge():
    def __init__(self, pin1, pin2):
        self.opener = gpiozero.OutputDevice(pin1, active_high=True, initial_value=False)
        self.closer = gpiozero.OutputDevice(pin2, active_high=True, initial_value=False)

    def opens(self, timeout = 0.1):
        """Function to open the door"""
        self.opener.on()
        time.sleep(timeout)
        self.opener.off()
        return True

    def close(self, timeout = 0.1):
        """Function to close the doors"""
        self.closer.on()
        time.sleep(timeout)
        self.closer.off()
        return True
