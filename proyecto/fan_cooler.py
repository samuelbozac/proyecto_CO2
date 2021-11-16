from time import sleep
import gpiozero

class FanCooler():
    
    def __init__(self, relay_pin):
        self.relay = gpiozero.OutputDevice(relay_pin, active_high=True, initial_value=False)
    
    def desactivate(self):
        self.relay.off() # switch off
    
    def activate(self):
        self.relay.on() # switch on

    