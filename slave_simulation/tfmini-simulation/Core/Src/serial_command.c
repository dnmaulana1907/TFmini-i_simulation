/*
 * serial_command.c
 *
 *  Created on: Mar 1, 2026
 *      Author: danimaulana
 */

#include "serial_command.h"
#include "usart.h"
#include "crc_mod.h"

#define UART_TIMEOUT	100

extern uint8_t slave_id;
uint8_t id_update_flag;
uint8_t id_change;

const static struct scp_cmd_func_binding_s scp_cmd_func_table[] = {
//		command TAG					 function binding
		{GET_DISTANCE_AND_SIGNAL	 , read_distance_signal},
		{SET_FRAME_RATE				 , set_frame_rate},
		{SET_SLAVE_ID				 , set_slave_id},
		{SET_WORK_MODE				 , set_work_mode},
		{GET_FIRMWARE_VER		     , read_firmware_version},
		{SAVE_SENSOR_CONFIG			 , save_configuration},
		{SENSOR_RESET				 , reset_sensor}
};

const uint8_t cmd_vect_table_len	= sizeof(scp_cmd_func_table)/sizeof(struct scp_cmd_func_binding_s);

int scp_worker_execute_cmd(uint8_t* scp_buf){

	uint8_t target_id = scp_buf[3];
	scp_cmd_e internal_cmd = CMD_UNKNOWN;

	switch(target_id){
	case DISTANCE_SIGNAL:
		internal_cmd = GET_DISTANCE_AND_SIGNAL;
		break;
	case FIRMWARE_VER :
		internal_cmd = GET_FIRMWARE_VER;
		break;
	case SLAVE_ID :
		internal_cmd = SET_SLAVE_ID;
		break;
	case FRAME_RATE:
		internal_cmd = SET_FRAME_RATE;
		break;
	case WORKING_MODE:
		internal_cmd = SET_WORK_MODE;
		break;
	case FACTORY_RESET:
		internal_cmd = SENSOR_RESET;
		break;
	case SAVE_CONFIG:
		internal_cmd = SAVE_SENSOR_CONFIG;
		break;
	default:
		break;

	}

	if (internal_cmd > cmd_vect_table_len - 1)
	{
		return ERROR;
	}
	else
	{
		scp_cmd_func_table[internal_cmd].func_ptr(scp_buf);
		return SUCCESS;
	}

}

static void read_distance_signal(uint8_t *scp_buf){
	uint8_t read_distance_buf[9];

	if (scp_buf[5] == DISTANCE_ONLY){
		read_distance_buf[0] = slave_id;
		read_distance_buf[1] = READ_MODE;
		read_distance_buf[2] = 0x02U;
		read_distance_buf[3] = 0x02U;
		read_distance_buf[4] = 0xBCU;
		insert_crc(read_distance_buf, 5U);

		HAL_UART_Transmit(&huart1, read_distance_buf, 7, UART_TIMEOUT);
	}

	if(scp_buf[5] == DISTANCE_AND_SIGNAL)
	{
		read_distance_buf[0] = slave_id;
		read_distance_buf[1] = READ_MODE;
		read_distance_buf[2] = 0x04U;
		read_distance_buf[3] = 0x00U;
		read_distance_buf[4] = 0x64U;
		read_distance_buf[5] = 0x03U;
		read_distance_buf[6] = 0xE8U;
		insert_crc(read_distance_buf, 7U);

		HAL_UART_Transmit(&huart1, read_distance_buf, 9, UART_TIMEOUT);
	}
}

static void read_firmware_version (uint8_t* scp_buf) {
	uint8_t read_firm_ver_buf[9];

	read_firm_ver_buf[0] = slave_id;
	read_firm_ver_buf[1] = READ_MODE;
	read_firm_ver_buf[2] = 0x04U;
	read_firm_ver_buf[3] = 0x00U;
	read_firm_ver_buf[4] = 0x03U;
	read_firm_ver_buf[5] = 0x05U;
	read_firm_ver_buf[6] = 0x0AU;

	insert_crc(read_firm_ver_buf, 7);

	HAL_UART_Transmit(&huart1, read_firm_ver_buf, 9, UART_TIMEOUT);

}

static void set_frame_rate(uint8_t* scp_buf)
{
	HAL_UART_Transmit(&huart1, scp_buf, 8, UART_TIMEOUT);
}

static void set_slave_id(uint8_t* scp_buf)
{
	HAL_UART_Transmit(&huart1, scp_buf, 8, UART_TIMEOUT);
	id_update_flag = SET;
	id_change = scp_buf[5];
}

static void set_work_mode(uint8_t* scp_buf)
{
	HAL_UART_Transmit(&huart1, scp_buf, 8, UART_TIMEOUT);
}

static void save_configuration(uint8_t* scp_buf)
{
	HAL_UART_Transmit(&huart1, scp_buf, 8, UART_TIMEOUT);
	if(id_update_flag == SET)
	{
		id_update_flag = RESET;
		slave_id = id_change;
	}
}

static void reset_sensor(uint8_t* scp_buf)
{
	HAL_UART_Transmit(&huart1, scp_buf, 8, UART_TIMEOUT);
	HAL_NVIC_SystemReset();
}
