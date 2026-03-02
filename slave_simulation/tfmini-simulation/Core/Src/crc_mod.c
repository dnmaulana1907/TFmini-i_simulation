/*
 * crc_mod.c
 *
 *  Created on: Mar 1, 2026
 *      Author: danimaulana
 */


#include "crc_mod.h"

#define POLY_CRC_MOD	0x80050000
#define	LENGTH_CHECK	0x06U

uint16_t crc16_modbus(uint8_t *buf, uint8_t length)
{
	uint16_t crc = 0xFFFF;

	    for (uint8_t pos = 0; pos < length; pos++) {
	        crc ^= (uint16_t)buf[pos];

	        for (uint8_t i = 8; i != 0; i--) {
	            if ((crc & 0x0001) != 0) {
	                crc >>= 1;
	                crc ^= __RBIT(POLY_CRC_MOD);
	            } else {
	                crc >>= 1;
	            }
	        }
	    }
	    return crc;
}


void insert_crc(uint8_t *packet_head)
{
	uint16_t crc_ret;
	crc_ret = crc16_modbus(&packet_head[0], LENGTH_CHECK);

	packet_head[6] = (uint8_t) crc_ret;
	packet_head[7] = (uint8_t) (crc_ret >> 8);

}

uint8_t crc_check(uint8_t *buf)
{
	uint16_t crc_cal = crc16_modbus(buf, LENGTH_CHECK);
	uint16_t crc_buf = (uint16_t) buf[6] |
					   (uint16_t) buf[7] << 8;

	if (crc_cal == crc_buf) return SUCCESS;
	else return ERROR;
}
