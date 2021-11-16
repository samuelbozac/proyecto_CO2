from signal import signal, SIGTERM, SIGHUP, pause
from gpiozero import Servo
from datetime import datetime as dt, timedelta
import json
from fan_cooler import FanCooler
from lcd import lcd
from bridges_h import bridge_h
import mh_z19
import pandas as pd
import time
import smtplib
import sys, os

fan = FanCooler(21)
bridge_1 = bridge_h(pin1 = 32, pin2 = 33)
bridge_2 = bridge_h(pin1 = 34, pin2 = 35)
lcd2 = lcd() # Configurate LCD2 address before execute
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
    email = "TEG.usuarioCO2@gmail.com"
    password = "alertaCO2"
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
            co2 = float(resp.get('co2'))
            resp.update({"datetime":time_moment.timestamp()})
            print(f'Niveles de CO2: {co2}')
            lcd2.message(f"CO2: {co2}", 1)
            if co2 >= 800:
                print('Por encima del limite recomendado.\nIniciando proceso de ventilación')
                # Open doors and windows
                servo.max()
                # Activate "H-Bridge"
                bridge_1.opens()
                bridge_2.opens()
                fan.activate()
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
            elif (co2 < 550) and opened:
                # Close doors and windows
                servo.min()
                bridge_1.close()
                bridge_2.close()
                fan.desactivate()
                opened = False
                subject = f'Nivel de CO2 estable'
                message = f'El nivel de concentración de CO2 se encuentra por debajo de 800ppm. El sistema de ventilación preventiva del área se apagará.'
                message = f'Subject: {subject}\n\n{message}'
                send_report_email(message)
            if not os.path.exists('data.txt'):
                with open('data.txt', 'w') as file:
                    json_data = json.dumps([resp])
                    file.write(json_data)
                    file.close()
            else:
                with open('data.txt', 'r') as file:
                    txt_last_data = file.read()
                    last_data = json.loads(txt_last_data)
                data = last_data.append(resp)
                with open('data.txt', 'w') as file:
                    json_data = json.dumps(data)
                    file.write(json_data)
                    file.close()
            time.sleep(1)
        except KeyboardInterrupt:
            reading = False
        finally:
            lcd2.clear()
