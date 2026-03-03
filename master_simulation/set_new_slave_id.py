from command_list import PROCESS_FAIL, save_sensor_config, set_slave_id
import time
import sys

CURRENT_SLAVE_ID = b'\x01'
NEW_SLAVE_ID = b'\x03'

print("UPDATE_SLAVE_ID: Setting new slave ID on the sensor...")

if set_slave_id (CURRENT_SLAVE_ID, NEW_SLAVE_ID) == PROCESS_FAIL:
    print("Failed to set new slave ID on the sensor.")
    sys.exit(1)

time.sleep(1)  

print("SAVE_CONFIG: Saving new configuration to the sensor...")

if save_sensor_config(CURRENT_SLAVE_ID) == PROCESS_FAIL:
    print("Failed to save sensor configuration.")
    sys.exit(1)