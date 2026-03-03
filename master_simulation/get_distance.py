from command_list import get_distance,PROCESS_FAIL

SLAVE_ID = b'\x01'  

if get_distance(SLAVE_ID) == PROCESS_FAIL:
    print("Failed to read distance from the sensor.")