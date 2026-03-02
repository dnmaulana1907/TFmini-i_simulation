/*
 * serial_command.c
 *
 *  Created on: Mar 1, 2026
 *      Author: danimaulana
 */

#include "serial_command.h"

const static struct scp_cmd_func_binding_s scp_cmd_func_table[] = {
//		command TAG					 function binding
		{GET_DISTANCE				, NULL},
		{GET_DISTANCE_AND_SIGNAL	, NULL},
		{SET_FRAME_RATE				, NULL},
		{SET_SLAVE_ID				, NULL},
		{SET_WORK_MODE				, NULL},
		{GET_FIRMWARE_VER			, NULL},
		{SENSOR_RESET				, NULL}
};

const uint8_t cmd_vect_table_len	= sizeof(scp_cmd_func_table)/sizeof(struct scp_cmd_func_binding_s);

int scp_worker_execute_cmd(uint8_t* scp_buf){

}
