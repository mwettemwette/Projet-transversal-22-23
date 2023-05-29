/*
 * servo.c
 *
 *  Created on: Apr 18, 2023
 *      Author: siben
 */

#include "stm32f4xx_hal.h"

int32_t CH1_DC = 1500;

void servo(int angle){
	//angle allant de 0 a 180 degre ; 0°=500, 45°=1000, 90°=1500
	TIM1->CCR1 = CH1_DC;
	CH1_DC = angle * 11 + 500; //135 degré ---- 1500 =90
	HAL_Delay(500);
}
