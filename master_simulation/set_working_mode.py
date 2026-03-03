from command_list import PROCESS_FAIL, set_working_mode, save_sensor_config
import time
import sys

SLAVE_ID = b'\x01'
WORKING_MODE = 1  

print(["SET_WORKING_MODE: Setting working mode on the sensor..."])

if set_working_mode(SLAVE_ID, WORKING_MODE) == PROCESS_FAIL:
    print("Failed to set working mode.")
    sys.exit(1)

time.sleep(1)

print("SAVE_CONFIG: Saving new configuration to the sensor...")
if save_sensor_config(SLAVE_ID) == PROCESS_FAIL:
    print("Failed to save sensor configuration.")
    sys.exit(1)