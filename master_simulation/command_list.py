import serial
import time
from serial_config import PORT, BAUDRATE
from termcolor import colored


PROCESS_SUCCESS = 0
PROCESS_FAIL = 1

SER_PORT = PORT
SER_BAUD = BAUDRATE

ser_hndl = serial.Serial()
ser_hndl.baudrate = SER_BAUD
ser_hndl.timeout = 1  
ser_hndl.setDTR(False)
ser_hndl.setPort(SER_PORT)
ser_hndl.open()

""" 
COMMAND DEFINITIONS FOR MASTER SIMULATION 

1. GET DISTANCE
    REQ : 01 03 00 00 00 01 84 0A
    RES : 01 03 02 02 BC B8 95


2. GET DISTANCE AND SIGNAL STRENGTH
    REQ : 01 03 00 00 00 02 C4 0B
    RES : 01 03 04 00 64 03 E8 BB 52


3. SET FRAME RATE
    REQ : 01 06 00 86 00 0A E8 24
    RES : 01 06 00 86 00 0A E8 24


4. SET SLAVE ID
    REQ : 01 06 00 85 00 03 D8 22
    RES : 01 06 00 85 00 03 D8 22

    REQ : 01 06 00 80 00 00 88 22
    RES : 01 06 00 80 00 00 88 22

    
5. SET WORKING MODE (0x01: continuous detecting mode, 0x00: trigger mode)
    REQ : 01 06 00 87 00 01 F8 23
    RES : 01 06 00 87 00 01 F8 23

    REQ : 01 06 00 80 00 00 88 22
    RES : 01 06 00 80 00 00 88 22

6. GET FIRMWARE VERSION
    REQ :01 03 00 06 00 02 24 0A   
    RES : 01 03 04 00 03 05 0A 89 64

7. RESET SENSOR
    REQ : 01 06 00 89 00 00 58 20
    RES : 01 06 00 89 00 00 58 20
"""




def calculate_crc16(data: bytes) -> bytes:
    """Calculate Modbus RTU CRC-16."""
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return bytes([crc & 0xFF, (crc >> 8) & 0xFF])

def get_distance(slave_id: bytes) -> int:

    SER_PACKET_HEAD = b'\x03\x00\x00\x00\x01'
    PAYLOAD = slave_id + SER_PACKET_HEAD
    CRC = calculate_crc16(PAYLOAD)
    SER_PACKET = PAYLOAD + CRC

    print(colored(f"[REQ_INFO] SLAVE ID: {slave_id[0]:02X}", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] FUNCTION CODE: 0x03 (Read Holding Registers)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] START ADDRESS: 0x0000", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] NUMBER OF REGISTERS: 0x0001", "cyan", "on_white"))
    try:
        ser_hndl.reset_input_buffer()
        print(colored(f"[REQ_DATA] {' '.join([f'{b:02X}' for b in SER_PACKET])}", "blue", "on_white"))
        
        ser_hndl.write(SER_PACKET)
        response = ser_hndl.read(7)

        if not response:
            print(colored("[ERROR] Timeout: No response received from SENSOR", "white", "on_red"))
            return PROCESS_FAIL
        
        print(colored(f"[RES_DATA] {' '.join([f'{b:02X}' for b in response])}", "blue", "on_white"))

        if len(response) == 7 and response[0] == slave_id[0] and response[1] == 0x03:
            if calculate_crc16(response[:-2]) == response[-2:]:
                distance = (response[3] << 8) | response[4]
                print(colored(f"[GET_DISTANCE] Distance: {distance} cm", "green", "on_white"))
                return PROCESS_SUCCESS
            else:
                print(colored("[ERROR] CRC mismatch in received response.", "white", "on_red"))
                return PROCESS_FAIL
        else:
            print(colored("[ERROR] Invalid response format or incomplete frame.", "white", "on_red"))
            return PROCESS_FAIL

    except serial.SerialException as e:
        print(f"[ERROR] Serial interface exception: {e}")
        return PROCESS_FAIL

def get_distance_and_signal_strength(slave_id: bytes) -> int:

    SER_PACKET_HEAD = b'\x03\x00\x00\x00\x02'
    PAYLOAD = slave_id + SER_PACKET_HEAD
    CRC = calculate_crc16(PAYLOAD)
    SER_PACKET = PAYLOAD + CRC

    print(colored(f"[REQ_INFO] SLAVE ID: {slave_id[0]:02X}", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] FUNCTION CODE: 0x03 (Read Holding Registers)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] START ADDRESS: 0x0000", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] NUMBER OF REGISTERS: 0x0002", "cyan", "on_white"))
    
    try:
        ser_hndl.reset_input_buffer()
        print(colored(f"[REQ_DATA] {' '.join([f'{b:02X}' for b in SER_PACKET])}", "blue", "on_white"))
        
        ser_hndl.write(SER_PACKET)
        response = ser_hndl.read(9)

        if not response:
            print(colored("[ERROR] Timeout: No response received from SENSOR", "white", "on_red"))
            return PROCESS_FAIL
        
        print(colored(f"[RES_DATA] {' '.join([f'{b:02X}' for b in response])}", "blue", "on_white"))

        if len(response) == 9 and response[0] == slave_id[0] and response[1] == 0x03 and response[2] == 0x04:
            if calculate_crc16(response[:-2]) == response[-2:]:
                
                distance = (response[3] << 8) | response[4]
                signal_strength = (response[5] << 8) | response[6] 
                
                print(colored(f"[GET_DISTANCE] Distance: {distance} cm", "green", "on_white"))
                print(colored(f"[GET_SIGNAL] Signal Strength: {signal_strength}", "green", "on_white"))
                return PROCESS_SUCCESS
            else:
                print(colored("[ERROR] CRC mismatch in received response.", "white", "on_red"))
                return PROCESS_FAIL
        else:
            print(colored("[ERROR] Invalid response format or incomplete frame.", "white", "on_red"))
            return PROCESS_FAIL

    except serial.SerialException as e:
        print(colored(f"[ERROR] Serial interface exception: {e}", "white", "on_red"))
        return PROCESS_FAIL

def set_frame_rate(slave_id: bytes, frame_rate: int) -> int:
    if frame_rate < 1 or frame_rate > 100:
        print(colored("[ERROR] Invalid frame rate. Must be between 1 and 100 FPS.", "white", "on_red"))
        return PROCESS_FAIL

    frame_rate_value = frame_rate & 0xFF
    SER_PACKET_HEAD = b'\x06\x00\x86\x00' + bytes([frame_rate_value])
    PAYLOAD = slave_id + SER_PACKET_HEAD
    CRC = calculate_crc16(PAYLOAD)
    SER_PACKET = PAYLOAD + CRC

    print(colored(f"[REQ_INFO] SLAVE ID: {slave_id[0]:02X}", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] FUNCTION CODE: 0x06 (Write Single Register)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] REGISTER ADDRESS: 0x0086 (Frame Rate)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] FRAME RATE VALUE: {frame_rate} FPS", "cyan", "on_white"))
    
    try:
        ser_hndl.reset_input_buffer()
        print(colored(f"[REQ_DATA] {' '.join([f'{b:02X}' for b in SER_PACKET])}", "blue", "on_white"))
        
        ser_hndl.write(SER_PACKET)
        response = ser_hndl.read(8)

        if not response:
            print(colored("[ERROR] Timeout: No response received from SENSOR", "white", "on_red"))
            return PROCESS_FAIL
        
        print(colored(f"[RES_DATA] {' '.join([f'{b:02X}' for b in response])}", "blue", "on_white"))

        if len(response) == 8 and response[0] == slave_id[0] and response[1] == 0x06 and response[2] == 0x00 and response[3] == 0x86:
            if calculate_crc16(response[:-2]) == response[-2:]:
                print(colored(f"[SET_FRAME_RATE] Frame rate set to {frame_rate} Hz.", "green", "on_white"))
                return PROCESS_SUCCESS
            else:
                print(colored("[ERROR] CRC mismatch in received response.", "white", "on_red"))
                return PROCESS_FAIL
        else:
            print(colored("[ERROR] Invalid response format or incomplete frame.", "white", "on_red"))
            return PROCESS_FAIL
    except serial.SerialException as e:
        print(colored(f"[ERROR] Serial interface exception: {e}", "white", "on_red"))
        return PROCESS_FAIL
    
def set_slave_id(current_id: bytes, new_id: bytes) -> int:
    if new_id[0] < 1 or new_id[0] > 247:
        print(colored("[ERROR] Invalid Slave ID. Must be between 1 and 247.", "white", "on_red"))
        return PROCESS_FAIL

    SER_PACKET_HEAD = b'\x06\x00\x85\x00' + new_id
    PAYLOAD = current_id + SER_PACKET_HEAD
    CRC = calculate_crc16(PAYLOAD)
    SER_PACKET = PAYLOAD + CRC

    print(colored(f"[REQ_INFO] CURRENT SLAVE ID: {current_id[0]:02X}", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] FUNCTION CODE: 0x06 (Write Single Register)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] REGISTER ADDRESS: 0x0085 (Slave ID)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] NEW SLAVE ID: {new_id[0]:02X}", "cyan", "on_white"))
    
    try:
        ser_hndl.reset_input_buffer()
        print(colored(f"[REQ_DATA] {' '.join([f'{b:02X}' for b in SER_PACKET])}", "blue", "on_white"))
        
        ser_hndl.write(SER_PACKET)
        response = ser_hndl.read(8)

        if not response:
            print(colored("[ERROR] Timeout: No response received from SENSOR", "white", "on_red"))
            return PROCESS_FAIL
        
        print(colored(f"[RES_DATA] {' '.join([f'{b:02X}' for b in response])}", "blue", "on_white"))

        if len(response) == 8 and response[0] == current_id[0] and response[1] == 0x06 and response[2] == 0x00 and response[3] == 0x85:
            if calculate_crc16(response[:-2]) == response[-2:]:
                print(colored(f"[SET_SLAVE_ID] Slave ID changed to {new_id[0]:02X}.", "green", "on_white"))
                return PROCESS_SUCCESS
            else:
                print(colored("[ERROR] CRC mismatch in received response.", "white", "on_red"))
                return PROCESS_FAIL
        else:
            print(colored("[ERROR] Invalid response format or incomplete frame.", "white", "on_red"))
            return PROCESS_FAIL
    except serial.SerialException as e:
        print(colored(f"[ERROR] Serial interface exception: {e}", "white", "on_red"))
        return PROCESS_FAIL
    
def save_sensor_config(slave_id: bytes) -> int:
    SER_PACKET_HEAD = b'\x06\x00\x80\x00\x00'
    PAYLOAD = slave_id + SER_PACKET_HEAD
    CRC = calculate_crc16(PAYLOAD)
    SER_PACKET = PAYLOAD + CRC

    print(colored(f"[REQ_INFO] SLAVE ID: {slave_id[0]:02X}", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] FUNCTION CODE: 0x06 (Write Single Register)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] REGISTER ADDRESS: 0x0080 (Save Config)", "cyan", "on_white"))
    
    try:
        ser_hndl.reset_input_buffer()
        print(colored(f"[REQ_DATA] {' '.join([f'{b:02X}' for b in SER_PACKET])}", "blue", "on_white"))
        
        ser_hndl.write(SER_PACKET)
        response = ser_hndl.read(8)

        if not response:
            print(colored("[ERROR] Timeout: No response received from SENSOR", "white", "on_red"))
            return PROCESS_FAIL
        
        print(colored(f"[RES_DATA] {' '.join([f'{b:02X}' for b in response])}", "blue", "on_white"))

        if len(response) == 8 and response[0] == slave_id[0] and response[1] == 0x06 and response[2] == 0x00 and response[3] == 0x80:
            if calculate_crc16(response[:-2]) == response[-2:]:
                print(colored(f"[SAVE_CONFIG] Sensor configuration saved and reboot initiated.", "green", "on_white"))
                return PROCESS_SUCCESS
            else:
                print(colored("[ERROR] CRC mismatch in received response.", "white", "on_red"))
                return PROCESS_FAIL
        else:
            print(colored("[ERROR] Invalid response format or incomplete frame.", "white", "on_red"))
            return PROCESS_FAIL
    except serial.SerialException as e:
        print(colored(f"[ERROR] Serial interface exception: {e}", "white", "on_red"))
        return PROCESS_FAIL
    
def set_working_mode(slave_id: bytes, mode: int) -> int:
    if mode not in (0, 1):
        print(colored("[ERROR] Invalid working mode. Must be 0 (trigger mode) or 1 (continuous mode).", "white", "on_red"))
        return PROCESS_FAIL

    SER_PACKET_HEAD = b'\x06\x00\x87\x00' + bytes([mode])
    PAYLOAD = slave_id + SER_PACKET_HEAD
    CRC = calculate_crc16(PAYLOAD)
    SER_PACKET = PAYLOAD + CRC

    print(colored(f"[REQ_INFO] SLAVE ID: {slave_id[0]:02X}", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] FUNCTION CODE: 0x06 (Write Single Register)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] REGISTER ADDRESS: 0x0087 (Working Mode)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] WORKING MODE: {'Continuous' if mode == 1 else 'Trigger'}", "cyan", "on_white"))
    
    try:
        ser_hndl.reset_input_buffer()
        print(colored(f"[REQ_DATA] {' '.join([f'{b:02X}' for b in SER_PACKET])}", "blue", "on_white"))
        
        ser_hndl.write(SER_PACKET)
        response = ser_hndl.read(8)

        if not response:
            print(colored("[ERROR] Timeout: No response received from SENSOR", "white", "on_red"))
            return PROCESS_FAIL
        
        print(colored(f"[RES_DATA] {' '.join([f'{b:02X}' for b in response])}", "blue", "on_white"))

        if len(response) == 8 and response[0] == slave_id[0] and response[1] == 0x06 and response[2] == 0x00 and response[3] == 0x87:
            if calculate_crc16(response[:-2]) == response[-2:]:
                print(colored(f"[SET_WORKING_MODE] Working mode set to {'Continuous' if mode == 1 else 'Trigger'}.", "green", "on_white"))
                return PROCESS_SUCCESS
            else:
                print(colored("[ERROR] CRC mismatch in received response.", "white", "on_red"))
                return PROCESS_FAIL
        else:
            print(colored("[ERROR] Invalid response format or incomplete frame.", "white", "on_red"))
            return PROCESS_FAIL
    except serial.SerialException as e:
        print(colored(f"[ERROR] Serial interface exception: {e}", "white", "on_red"))
        return PROCESS_FAIL
    
def get_firmware_version(slave_id: bytes) -> int:
    SER_PACKET_HEAD = b'\x03\x00\x06\x00\x02'
    PAYLOAD = slave_id + SER_PACKET_HEAD
    CRC = calculate_crc16(PAYLOAD)
    SER_PACKET = PAYLOAD + CRC

    print(colored(f"[REQ_INFO] SLAVE ID: {slave_id[0]:02X}", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] FUNCTION CODE: 0x03 (Read Holding Registers)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] START ADDRESS: 0x0006", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] NUMBER OF REGISTERS: 0x0002", "cyan", "on_white"))
    
    try:
        ser_hndl.reset_input_buffer()
        print(colored(f"[REQ_DATA] {' '.join([f'{b:02X}' for b in SER_PACKET])}", "blue", "on_white"))
        
        ser_hndl.write(SER_PACKET)
        response = ser_hndl.read(9)

        if not response:
            print(colored("[ERROR] Timeout: No response received from SENSOR", "white", "on_red"))
            return PROCESS_FAIL
        
        print(colored(f"[RES_DATA] {' '.join([f'{b:02X}' for b in response])}", "blue", "on_white"))

        if len(response) == 9 and response[0] == slave_id[0] and response[1] == 0x03 and response[2] == 0x04:
            if calculate_crc16(response[:-2]) == response[-2:]:
                major_version = response[3]
                minor_version = response[4]
                patch_version = response[5]
                build_number = response[6]
                
                print(colored(f"[FIRMWARE_VERSION] Version: {major_version}.{minor_version}.{patch_version} Build {build_number}", "green", "on_white"))
                return PROCESS_SUCCESS
            else:
                print(colored("[ERROR] CRC mismatch in received response.", "white", "on_red"))
                return PROCESS_FAIL
        else:
            print(colored("[ERROR] Invalid response format or incomplete frame.", "white", "on_red"))
            return PROCESS_FAIL

    except serial.SerialException as e:
        print(colored(f"[ERROR] Serial interface exception: {e}", "white", "on_red"))
        return PROCESS_FAIL
    
def reset_sensor(slave_id: bytes) -> int:
    SER_PACKET_HEAD = b'\x06\x00\x89\x00\x00'
    PAYLOAD = slave_id + SER_PACKET_HEAD
    CRC = calculate_crc16(PAYLOAD)
    SER_PACKET = PAYLOAD + CRC

    print(colored(f"[REQ_INFO] SLAVE ID: {slave_id[0]:02X}", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] FUNCTION CODE: 0x06 (Write Single Register)", "cyan", "on_white"))
    print(colored(f"[REQ_INFO] REGISTER ADDRESS: 0x0089 (Reset Sensor)", "cyan", "on_white"))
    
    try:
        ser_hndl.reset_input_buffer()
        print(colored(f"[REQ_DATA] {' '.join([f'{b:02X}' for b in SER_PACKET])}", "blue", "on_white"))
        
        ser_hndl.write(SER_PACKET)
        response = ser_hndl.read(8)

        if not response:
            print(colored("[ERROR] Timeout: No response received from SENSOR", "white", "on_red"))
            return PROCESS_FAIL
        
        print(colored(f"[RES_DATA] {' '.join([f'{b:02X}' for b in response])}", "blue", "on_white"))

        if len(response) == 8 and response[0] == slave_id[0] and response[1] == 0x06 and response[2] == 0x00 and response[3] == 0x89:
            if calculate_crc16(response[:-2]) == response[-2:]:
                print(colored(f"[RESET_SENSOR] Sensor reset command acknowledged.", "green", "on_white"))
                return PROCESS_SUCCESS
            else:
                print(colored("[ERROR] CRC mismatch in received response.", "white", "on_red"))
                return PROCESS_FAIL
        else:
            print(colored("[ERROR] Invalid response format or incomplete frame.", "white", "on_red"))
            return PROCESS_FAIL
    except serial.SerialException as e:
        print(colored(f"[ERROR] Serial interface exception: {e}", "white", "on_red"))
        return PROCESS_FAIL

