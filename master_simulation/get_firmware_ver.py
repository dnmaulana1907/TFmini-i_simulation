from command_list import PROCESS_FAIL, get_firmware_version

SLAVE_ID = b'\x01'

if get_firmware_version(SLAVE_ID) == PROCESS_FAIL:
    print("Failed to read firmware version from the sensor.")  