from h_bridges import Doors
from lcd import lcd
import time
from fan_cooler import FanCooler
from gpiozero import Servo
import smtplib
from datetime import datetime as dt
from numpy.random import randint
import json
import pytz

def hora_locacion(locacion):
    """Función para dar hora actual de lugar en específico
        :param locacion: Ciudad con el uso horario a pedir (America/Caracas)
        :type locacion: str
        
        :return: Datetime con tzinfo requerido
        :rtype: Datetime
        """
    tz = locacion
    utcmoment_naive = dt.utcnow()
    utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
    return utcmoment.astimezone(pytz.timezone(tz))

def open_all(servo,fan,doors):
    servo.max()
    fan.activate()
    doors.opening(timeout = 0.07)

def close_all(servo,fan,doors):
    servo.min()
    fan.desactivate()
    doors.closing(timeout = 0.07)

def send_report_email(message):
    """Function to send the report of an action to the user
    
        :param message: Message to send
        :type message: str
        
        :return: Boolean if the message was sent.
        :rtype: bool
        """
    print('Enviando email...')
    email = "TEG.usuarioCO2@gmail.com"
    password = "alertaCO2."
    destinatary = "fcmloaiza@gmail.com"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)

    server.sendmail(email, destinatary, message)

    server.quit()
    print('Email enviado.')
    return True

if __name__ == '__main__':
    process = 0
    concentration = 421
    opened = False
    display = lcd()
    doors = Doors(6,13,26,19)
    fan = FanCooler(21)
    servo = Servo(2)

    while process == 0:
        actual_data = {f"{hora_locacion('America/Caracas').timestamp()}" : concentration}
        with open("data.txt", "r") as file:
            file_read = file.read()
            print(file_read)
        data_dict = json.loads(str(file_read))
        print(type(data_dict))
        new_data = dict(data_dict,**actual_data)
        json_data = json.dumps(new_data)
        print(new_data)
        print(json_data)
        with open("data.txt", "w") as file_writer:
             file_writer.write(json_data)
             file_writer.close()
        time.sleep(1)
        display.clear()
        time_moment = hora_locacion("America/Caracas")
        if (concentration > 800) and (opened == False):
            servo.max()
            fan.activate()
            doors.opening(timeout = 0.07)
            opened = True
            display.message("Ventilando...")
            subject = "ALERTA!"
            message = f'El nivel de concentracion de CO2 en el ambiente a las {time_moment.strftime("%I:%M%p")} \
del {time_moment.strftime("%d/%m/%y")} es de {concentration}ppm, superando los 800ppm recomendados. Se iniciara la ventilacion preventiva del area.'
            message = f"Subject: {subject}\n\n{message}"
            send_report_email(message)
            time.sleep(3)
        elif (concentration < 500) and opened:
            servo.min()
            fan.desactivate()
            doors.closing(timeout = 0.07)
            opened = False
            subject = f'Nivel de CO2 estable'
            message = f'El nivel de concentracion de CO2 se encuentra por debajo de 800ppm. El sistema de ventilacion preventiva del area se apagara.'
            message = f'Subject: {subject}\n\n{message}'
            send_report_email(message)
            process +=1
        else:
            display.message(f"CO2: {concentration} PPM")
            if opened:
                concentration -= 9
            else:
                concentration += 47
    while True:
        display.clear()
        display.message(f"CO2: {concentration} PPM")
        time.sleep(10)
        if concentration % 2 == 0:
            concentration += randint(low=0, high=9)
        else:
            concentration -= randint(low=0, high=9)
