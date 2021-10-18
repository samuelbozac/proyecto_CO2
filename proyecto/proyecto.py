from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import mh_Z19
import psycopg2
import pandas as pd
import 


lcd = LCD()
while True:
    resp = mh_z19.read_all()
    lcd.text("
