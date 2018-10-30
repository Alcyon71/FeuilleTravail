import pyautogui
from serial_interface import SerialInterface
from mettler_toledo_device import MettlerToledoDevice


#on ouvre le port serie
Bal = SerialInterface(port='/dev/ttyUSB0', baudrate=9600, stopbits=1, debug='debug', write_read_delay=0.05, timeout=0.05)
#Bal = MettlerToledoDevice(port='/dev/ttyUSB0', debug='debug')

response = Bal.read_all()

print(response)

Bal.close()




