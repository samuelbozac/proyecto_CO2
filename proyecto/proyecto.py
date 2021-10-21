from signal import signal, SIGTERM, SIGHUP, pause
from gpiozero import Servo
from rpi_lcd import LCD
import mh_Z19
import psycopg2
import pandas as pd
import time
import smtplib

lcd = LCD()
servo = Servo(25)
reading = True
opened = False

if __name__ == '__main__':
    while reading:
        try:
            resp = mh_z19.read_all()
            co2 = resp.get('co2')
            lcd.text(f"CO2: {co2}", 1)
            if co2 >= 800:
                # Activación de motores para apertura de puertas y ventanas
                servo.max()
            elif (co2 < 800) and opened:
                # Activación de motores para cierre de puerta
                servo.min()
            time.sleep(1)
        except KeyboardInterrupt:
            reading = False
        finally:
            lcd.clear()
