from command_list import PROCESS_FAIL, set_frame_rate

SLAVE_ID = b'\x01'
FRAME_RATE = 10

if set_frame_rate(SLAVE_ID, FRAME_RATE) == PROCESS_FAIL:
    print("Failed to set frame rate on the sensor.")