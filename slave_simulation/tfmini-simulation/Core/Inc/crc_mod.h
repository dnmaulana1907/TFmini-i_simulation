/*
 * crc_mod.h
 *
 *  Created on: Mar 1, 2026
 *      Author: danimaulana
 */

#ifndef INC_CRC_MOD_H_
#define INC_CRC_MOD_H_

#include "stm32f4xx_hal.h"

uint16_t crc16_modbus(uint8_t *buf, uint8_t length);
void insert_crc(uint8_t *packet_head, uint8_t len);
uint8_t crc_check(uint8_t *packet_head);

#endif /* INC_CRC_MOD_H_ */
