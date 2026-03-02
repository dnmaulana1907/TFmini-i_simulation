/*
 * serial_command.h
 *
 *  Created on: Mar 1, 2026
 *      Author: danimaulana
 */

#ifndef INC_SERIAL_COMMAND_H_
#define INC_SERIAL_COMMAND_H_

#include "stm32f4xx_hal.h"

typedef void ( *volatile scp_func_ptr)(uint8_t *);

typedef enum {

	DISTANCE_SIGNAL = 0x00,
	FIRMWARE_VER = 0x06,
	SLAVE_ID = 0x85,
	FRAME_RATE = 0x86,
	WORKING_MODE = 0x87,
	FACTORY_RESET = 0x89

}RegisterID_e;

typedef enum {
	FIRST_VALUE,
	SECOND_VALUE,
}RegisterVale_e;

typedef enum {
	GET_DISTANCE,
	GET_DISTANCE_AND_SIGNAL,
	SET_FRAME_RATE,
	SET_SLAVE_ID,
	SET_WORK_MODE,
	GET_FIRMWARE_VER,
	SENSOR_RESET
}scp_cmd_e;

struct scp_cmd_func_binding_s{
	scp_cmd_e cmd_id;
	scp_func_ptr		 func_ptr;
};

#endif /* INC_SERIAL_COMMAND_H_ */
