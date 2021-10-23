import RPi.GPIO as GPIO

class Puente_h():
    GPIO.setmode(GPIO.BOARD)
    
    def __init__(self, pin, output):
        self.pin = pin
        self.output = output

    def activate(self):
        assert self.pin is not None
        assert self.output is not None
        GPIO.setup(self.pin, GPIO.OUT)

        if(self.output == "HIGH"):
            GPIO.output(self.pin, GPIO.HIGH)

        if(self.output == "LOW"):
            GPIO.output(self.pin, GPIO.LOW)
