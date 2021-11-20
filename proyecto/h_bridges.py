import time
import gpiozero

class H_Bridge():
    def __init__(self, pin1, pin2):
        self.opener = gpiozero.OutputDevice(pin1, active_high=True, initial_value=False)
        self.closer = gpiozero.OutputDevice(pin2, active_high=True, initial_value=False)

class Doors():
    def __init__(self, open1, close1, open2, close2):
        self.door1 = H_Bridge(open1, close1)
        self.door2 = H_Bridge(open2, close2)

    def opening(self, timeout):
        self.door1.opener.on()
        self.door2.opener.on()
        time.sleep(timeout)
        self.door1.opener.off()
        self.door2.opener.off()
    
    def closing(self, timeout):
        self.door1.closer.on()
        self.door2.closer.on()
        time.sleep(timeout)
        self.door1.closer.off()
        self.door2.closer.off()        