from h_bridges import Doors
from lcd import lcd
import time
from fan_cooler import FanCooler
from gpiozero import Servo

def open_all(servo,fan,doors):
    servo.max()
    fan.activate()
    doors.opening(timeout = 0.07)

def close_all(servo,fan,doors):
    servo.min()
    fan.desactivate()
    doors.closing(timeout = 0.07)

if __name__ == '__main__':
    concentration = 415
    opened = False
    display = lcd()
    doors = Doors(6,13,26,19)
    fan = FanCooler(21)
    servo = Servo(2)
    while True:
        time.sleep(1)
        display.clear()
        if (concentration > 800) and (opened == False):
            open_all(servo,fan,doors)
            opened = True
            display.message("Ventilando...")
        elif (concentration < 500) and opened:
            close_all()
            opened = False
        else:
            display.message(f"CO2: {concentration}")
            if opened:
                concentration -=10
            else:
                concentration += 50