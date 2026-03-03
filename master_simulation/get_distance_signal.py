from command_list import PROCESS_FAIL, get_distance_and_signal_strength

SLAVE_ID = b'\x01'  

if get_distance_and_signal_strength(SLAVE_ID) == PROCESS_FAIL:
    print("Failed to read distance and signal strength from the sensor.")