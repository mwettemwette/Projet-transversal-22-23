/*
 * telemetre_ir.c
 *
 *  Created on: Apr 18, 2023
 *      Author: siben
 */

#include <math.h>

#include "stm32f4xx_hal.h"

int raw;
extern ADC_HandleTypeDef hadc1;

int telemetre_ir(){
	HAL_ADC_Start(&hadc1);
	HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);
	raw = HAL_ADC_GetValue(&hadc1);

	return (ceil)(-1)*(raw/41 - 3550/41);

}


