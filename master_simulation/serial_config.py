import serial
from serial.tools import list_ports

ser = serial.Serial()
port = list_ports.comports()
def search_port(port):
    for p in port:
        # print(p.manufacturer)
        if 'Prolific' in str(p.manufacturer):
            # print(p.device)
            return p.device

PORT = search_port(port)
BAUDRATE = 115200