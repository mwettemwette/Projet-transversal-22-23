/*
 * encoder.c
 *
 *  Created on: Apr 20, 2023
 *      Author: siben
 */


#include "stm32f4xx_hal.h"


extern UART_HandleTypeDef huart1;


void clear_count_encoder(){
	HAL_UART_Transmit_IT(&huart1, (unsigned char*)"clrenc\r", 7);
	HAL_Delay(100);
}




int get_count_encoder1(){
	int count1;
	unsigned char* ret1;
	HAL_UART_Transmit_IT(&huart1, (unsigned char*)"getenc 1\r", 9);

	HAL_UART_Receive_IT(&huart1, &ret1, 5);

	HAL_Delay(50);
	return count1;
}




