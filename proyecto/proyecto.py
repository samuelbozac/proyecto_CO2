from signal import signal, SIGTERM, SIGHUP, pause
from gpiozero import Servo
from datetime import datetime as dt, timedelta
from servo import ServoMotor
# NOTE En prueba las dos ultimas clases a ver cual es más eficiente.
from rpi_lcd import LCD
import mh_Z19
import psycopg2
import pandas as pd
import time
import smtplib
import sys, os 

lcd = LCD()
servo = Servo(25)
reading = True
opened = False

def send_report_email(message):
    """Function to send the report of an action to the user
    
        :param message: Message to send
        :type message: str
        
        :return: Boolean if the message was sent.
        :rtype: bool
        """
    print('Enviando email...')
    email = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    destinatary = os.environ.get('USER_EMAIL')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)

    server.sendmail(email, destinatary, message)

    server.quit()
    print('Email enviado.')
    return True

if __name__ == '__main__':
    print('Iniciando lectura')
    while reading:
        time_moment = dt.now()
        try:
            resp = mh_z19.read_all()
            co2 = resp.get('co2')
            print(f'Niveles de CO2: {co2}')
            lcd.text(f"CO2: {co2}", 1)
            if co2 >= 800:
                print('Por encima del limite recomendado.\nIniciando proceso de ventilación')
                # Open doors and windows
                servo.max()
                opened = True
                subject = "¡ALERTA!"
                message = f'El nivel de concentración de CO2 en el ambiente a las {time_moment.strftime("%I:%M%p")} \
del {time_moment.strftime("%d/%m/%y")} es de {co2}ppm, superando los 800ppm recomendados. Se iniciará la ventilación preventiva del área.'
                message = f"Subject: {subject}\n\n{message}"
                send_report_email(message)
            elif co2 >= 550:
                subject = "¡Precaución!"
                message = f'El nivel de concentración de CO2 en la habitación es de {co2}ppm a las \
{time_moment.strftime("%I:%M%p")} del {time_moment.strftime("%d/%m/%y")}. Tomar precauciones!'
                message = f'Subject: {subject}\n\n{message}'
                send_report_email(message)  
            elif (co2 < 800) and opened:
                # Close doors and windows
                servo.min()
                opened = False
                subject = f'Nivel de CO2 estable'
                message = f'El nivel de concentración de CO2 se encuentra por debajo de 800ppm. El sistema de ventilación preventiva del área se apagará.'
                message = f'Subject: {subject}\n\n{message}'
                send_report_email(message)
            time.sleep(1)
        except KeyboardInterrupt:
            reading = False
        finally:
            lcd.clear()
