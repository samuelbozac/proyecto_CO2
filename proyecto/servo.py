from time import sleep
import RPi.GPIO as GPIO
import helpers.commands as commands
import sys


class ServoMotor:
    """Class representing the Servo Motor device"""
    channel = None
    PWMInstance = None

    def _init_(self, channel, feq=50):
        assert channel is not None
        self.channel = channel
        GPIO.setup(channel, GPIO.OUT)
        self.PWMInstance = GPIO.PWM(channel, feq)
        self.PWMInstance.start(0)  # Init a 0 duty cycle

    # NOTE The sleep is used in the movement functions to stop
    # execution of the program until servo movement is complete
    # since the ChangeDutyCycle does not stop execution
    def moveToMin(self):
        """Move Servo Motor to 0 degree (left)"""
        self.PWMInstance.ChangeDutyCycle(2)
        sleep(1.5)

    def moveToMid(self):
        """Move Servo Motor to 90 degrees (center)"""
        self.PWMInstance.ChangeDutyCycle(7.5)
        sleep(1.5)

    def moveToMax(self):
        """Move Servo Motor to 180 degrees (right)"""
        self.PWMInstance.ChangeDutyCycle(12)
        sleep(1.5)

    def moveTo135(self):
        """ Move Servo Motor to 125 degrees """
        self.PWMInstance.ChangeDutyCycle(9)
        sleep(1.5)

    def moveTo45(self):
        """ Move Servo Motor to 45 degrees """
        self.PWMInstance.ChangeDutyCycle(3.75)
        sleep(1.5)

    def stop(self):
        """Stop PWM signal to Servo Motor"""
        self.PWMInstance.stop()

    def moveTo(self, dt):
        """Move to a given angle, calculed by the duty cycle"""
        assert dt is None

        self.PWMInstance.ChangeDutyCycle(dt)
        sleep(1.5)


# Test Section
if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    pin = None
    mode = None

    pin: int = int(commands.getArgumentValue("GPIO_PIN"))
    mode = commands.getArgumentValue("mode")

    print(pin, mode)

    servo = ServoMotor(pin)

    if mode == '0':
        servo.moveToMin()
    if mode == '180':
        servo.moveToMax()
    if mode == '90':
        servo.moveToMid()
    if mode == '45':
        servo.moveTo45()
    if mode == '135':
        servo.moveTo135()

    servo.stop()

    GPIO.cleanup()

    exit(0)