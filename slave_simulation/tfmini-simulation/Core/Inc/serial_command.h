/*
 * serial_command.h
 *
 *  Created on: Mar 1, 2026
 *      Author: danimaulana
 */

#ifndef INC_SERIAL_COMMAND_H_
#define INC_SERIAL_COMMAND_H_

#include "main.h"

typedef void ( *volatile scp_func_ptr)(uint8_t *);

typedef enum {

	DISTANCE_SIGNAL = 0x00,
	FIRMWARE_VER = 0x06,
	SAVE_CONFIG = 0x80,
	SLAVE_ID = 0x85,
	FRAME_RATE = 0x86,
	WORKING_MODE = 0x87,
	FACTORY_RESET = 0x89
}RegisterID_e;

typedef enum {
	DISTANCE_ONLY = 0x01,
	DISTANCE_AND_SIGNAL = 0x02,
}RegisterVale_e;

typedef enum {
	READ_MODE = 0x03,
	WRITE_MODE = 0x06
}RegMode_e;

typedef enum {
	GET_DISTANCE_AND_SIGNAL,
	SET_FRAME_RATE,
	SET_SLAVE_ID,
	SET_WORK_MODE,
	GET_FIRMWARE_VER,
	SAVE_SENSOR_CONFIG,
	SENSOR_RESET,
	CMD_UNKNOWN
}scp_cmd_e;

struct scp_cmd_func_binding_s{
	scp_cmd_e cmd_id;
	scp_func_ptr		 func_ptr;
};



extern int scp_worker_execute_cmd(uint8_t* scp_buf);
static void read_distance_signal(uint8_t *scp_buf);
static void read_firmware_version (uint8_t* scp_buf);
static void set_frame_rate(uint8_t* scp_buf);
static void set_slave_id(uint8_t* scp_buf);
static void set_work_mode(uint8_t* scp_buf);
static void save_configuration(uint8_t* scp_buf);
static void reset_sensor(uint8_t* scp_buf);
#endif /* INC_SERIAL_COMMAND_H_ */
