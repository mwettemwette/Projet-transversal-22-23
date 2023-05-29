/*
 * etats_obstacles.c
 *
 *  Created on: Apr 18, 2023
 *      Author: siben
 */


#include "servo.h"
#include "main.h"
#include "adc.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"
#include "msg_interpreter.h"

#include "stm32f4xx_hal.h"

#include "math.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#define ROBOT_RADIUS 115
#define WHEEL_TICKS_ONE_TURN 624
#define WHEEL_DIST_ONE_TURN 188

//extern UART_HandleTypeDef huart1;

/*Flags Negatifs pour les observations du LIDAR.
 * 0 = ERROR. Reboucle dans etat_detecte_lidar.
 * 1 = Trigger via l'angle positif.
 * 2 = Trigger via l'angle negatif.
 *
 */
uint16_t nega20 = 0;
uint16_t nega45 = 0;
uint16_t nega90 = 0;


/**
  * @brief Add InsertStr data at the specified insertPos inside scr. Returns dest, the filled line.
  * @retval None
  */
void str_insert(char *dest, char *src, char *insertStr, uint16_t insertPos){

	//uint16_t insertPos
	//char *insertStr

	//char dest[strlen(insertStr)+strlen(src)+1]

	memcpy(dest, src, insertPos);
	memcpy(dest+insertPos, insertStr, strlen(insertStr));
	memcpy(dest+insertPos+strlen(insertStr), src+insertPos, strlen(dest)-insertPos);

	dest[insertPos+strlen(insertStr)] = '\0';

}

void etat_obstacle_immediat(int *p_etat){

	}


void etat_esquive_obstacle_proche(int *p_etat){

	}


void etat_suivie_de_mur(int *p_etat){

	}


/** ETAT 5
  * @brief The robot has arrived in front of the QR Code.
  * For now, it just stops.
  * @retval None
  */
void etat_QR_atteint(int *p_etat){

	Send_Msg("stop\r", strlen("stop\r"), "ser");
	*p_etat = 9;
	}


/** ETAT 4
  * @brief The robot must get closer to the QR code
  * @retval None
  */
void etat_QR_detecte(int *p_etat){

	// ======== Calcul de distance into nb_tick à faire
	int distance_qr = rpi_distance_qr - 500;	// Get a distance from raspberry. In millimeter
	int tick_num = (distance_qr * WHEEL_TICKS_ONE_TURN)/(WHEEL_DIST_ONE_TURN); // Calculating
	// ========

	// ======== Command to move the robot this distance in a straight line
	char command[35];
	sprintf(command, "digo 1:%d:10 2:%d:10\r", tick_num, tick_num);
	Send_Msg(command, strlen(command), "ser");

	*p_etat = 3;
	}


/** ETAT 3
  * @brief When the full distance has been done
  * Distance done depends from the distance indicated by the raspberry
  * Turns the cam 4 times. Ask every turn for cam activation.
  * @retval None
  */
void etat_destination_atteinte(int *p_etat){

	servo(0); // Locks the cam in its starting angle
	HAL_Delay(3000);

	char command[9] = "START_CAM"; // Ask for the cam to be active
	Send_Msg(command, strlen(command), "rpi"); // Send the cam request

	// ======== Moves the cam to complete the scan
	servo(45);
	Send_Msg(command, strlen(command), "rpi"); // Send the cam request
	HAL_Delay(3000);

	servo(90);
	Send_Msg(command, strlen(command), "rpi"); // Send the cam request
	HAL_Delay(3000);

	servo(135);
	Send_Msg(command, strlen(command), "rpi"); // Send the cam request
	HAL_Delay(3000);

	servo(0); // Reset the position. Deactivate the cam.
	char command2[8] = "STOP_CAM"; // Ask for the cam to be active
	Send_Msg(command2, strlen(command2), "rpi"); // Send the cam request
	HAL_Delay(3000);
	// ========

	// ======== Wait for cam confirmation and acts on it
	CAM_ANSWER = rpi_cam_answer; // Instantiates the cam's answer
	char error[8] = "ERROR_QR";
	if (strcmp(error, rpi_error_qr) == 0)
	{
		*p_etat = 9; // Null State
		rpi_error_qr = "\0";
	}
	else
	{
		int distance_qr = rpi_distance_qr;	// Get a distance from raspberry
		if (distance_qr < 500) // 500 mm
			*p_etat = 5; // Si proche le robot se stop
		else
			*p_etat = 4; // Si loin on se rapproche
	}
}


/** ETAT 2
  * @brief When there is nothing at the front, go forth
  * Distance done depends from the distance indicated by the raspberry
  * @retval None
  */
void etat_detecte_rien(int *p_etat){

	// ======== Calcul de distance into nb_tick à faire
	int distance = rpi_distance;	// Get a distance from raspberry
	int tick_num = (distance * WHEEL_TICKS_ONE_TURN)/(WHEEL_DIST_ONE_TURN); // Calculating
	// ========

	// ======== Command to move the robot this distance in a straight line
	char command[35];
	sprintf(command, "digo 1:%d:10 2:%d:10\r", tick_num, tick_num);
	Send_Msg(command, strlen(command), "ser");
	// ========

	*p_etat = 3;	// Etat 3 is to scan the environment with the cam
	}


/** ETAT 1
  * @brief Distance detection. The STM acts on what the environment is, based on what the Lidar sees.
  * @retval None
  */
void etat_detection_lidar(int *p_etat){
	char data[26] ="30 45 60 100 60 45 30";
	uint16_t info_90, info_45, info_20, info0, info20, info45, info90;
	uint16_t n =sscanf(data, "%d %d %d %d %d %d %d", &info_90, &info_45, &info_20, &info0, &info20, &info45, &info90);
	if (n == 7){
		if (info2 > 90)
			*p_etat = 2;
		else if (info2 < 30)
			HAL_UART_Transmit_IT(&huart1, (unsigned char*)"stop\r", 5);
	}
	else
		HAL_UART_Transmit_IT(&huart1, (unsigned char*)"error\r", 6);

	/* if (info0 < 20)
			*p_etat = 8;
		else if (info20 < 20)
			*p_etat = 7;
			nega20 = 1;
		else if (info_20 < 20)
			*p_etat = 7;
			nega20 = 2;
		else if (info90 < 20)
			*p_etat = 6;
			nega90 = 1;
		else if (info_90 < 20)
			*p_etat = 6;
			nega90 = 2;
	}
	else
		HAL_UART_Transmit_IT(&huart1, (unsigned char*)"error\r", 6);
	 *
	 */
}

/** ETAT 0
  * @brief The state must turn the robot of a given angle.
  * @retval None
  */
void etat_initial(int *p_etat){

	// Compute tick number from direction angle
	float angle = rpi_angle*M_PI/180;
	int tick_num = (angle * ROBOT_RADIUS * WHEEL_TICKS_ONE_TURN)/(2*M_PI*WHEEL_DIST_ONE_TURN);

	// Turn the robot in the destination direction (from angle)
	char command[35];
	sprintf(command, "digo 1:%d:10 2:-%d:10\r", tick_num, tick_num);
	Send_Msg(command, strlen(command), "ser");

	// Prochain état
	*p_etat = 3;

}

/**
  * @brief
  * @retval None
  */
void control_etat(int *p_etat){

		if (*p_etat == 0)
		{// Tells the Raspberry the state machines are on
			char command_on[8] = "ASK_INIT"; // Message init
			Send_Msg(command_on, strlen(command_on), "ser"); // Sends the message
			etat_initial(p_etat);
		}
		else if (*p_etat == 1)
			etat_detection_lidar(p_etat);
		else if (*p_etat == 2)
			etat_detecte_rien(p_etat);
		else if (*p_etat == 3)
			etat_destination_atteinte(p_etat);
		else if (*p_etat == 4)
			etat_QR_detecte(p_etat);
		else if (*p_etat == 5)
			etat_QR_atteint(p_etat);
		else if (*p_etat == 6)
				etat_suivie_du_mur(p_etat);
		else if (*p_etat == 7)
				etat_esquive_obstacle_proche(p_etat);
		else if (*p_etat == 8)
				etat_obstacle_immediat(p_etat);
		else if (*p_etat == 9)
			return;

}
