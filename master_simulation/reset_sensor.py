from command_list import PROCESS_FAIL, reset_sensor

SLAVE_ID = b'\x01'

if reset_sensor(SLAVE_ID) == PROCESS_FAIL:
    print("Failed to reset the sensor.")