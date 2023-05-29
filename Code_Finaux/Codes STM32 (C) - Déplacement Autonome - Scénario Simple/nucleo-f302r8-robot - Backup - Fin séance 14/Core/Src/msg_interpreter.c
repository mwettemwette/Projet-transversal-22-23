#ifndef __MAIN_C__
	#define __MAIN_C__
	#include "main.h"
#endif

#include "transceiver_uart.h"
#include "string.h"
#include "stdio.h"
#include "stdlib.h"
#include "msg_interpreter.h"

// Buffer sizes
#define RxBuf_SIZE		50

// MIN/MAX number of cells on the robot
#define CELL_NUM_MIN	1
#define CELL_NUM_MAX	5

// Variable for not having multiple instances of the interpreter function running simultaneously
uint8_t interpreter_running = 0;

// Useful buffers
uint8_t InterpretBuf[RxBuf_SIZE];

// Variables to store the commands
uint16_t rpi_auto_start = 0;
uint16_t rpi_angle = 0;
uint16_t rpi_distance = 0;
char rpi_error_qr[8];
uint16_t rpi_distance_qr = 0;
/**
  * @brief Interprets a new message, given using Retrieve_Msg function
  * @retval None
  */
void Interpret_Message_Recv()
{
	// Make sure this is the only instance of this function running currently
	if (interpreter_running == 0)
	{
		interpreter_running = 1; // Function cannot be executed twice

		/* Get one message from the input buffer, along with the UART Handle
		   from which it was received */
		char dev[4];
		int Size = Retrieve_Msg(InterpretBuf, dev);

		/**********************************************************************************/
		/******************** Interpret data found now in InterpretBuf ********************/
		/**********************************************************************************/
		if (Size > 0)
		{
			if (strncmp("rpi", dev, 3) == 0)
			{
				// Able to see the QR Code
				if (strncmp("START_AUTONOMOUS:", (char *)InterpretBuf, 17) == 0)
				{
					rpi_auto_start = 1;
				}

				// Initial direction received: DIR_INIT:[ANGLE]:[DIST]:
				if (strncmp("DIR_INIT:", (char *)InterpretBuf, 9) == 0)
				{
					sscanf((char *)InterpretBuf,"DIR_INIT:[%d]:[%d]", rpi_angle, rpi_distance );
				}

				// Unable to see the QR code
				if (strncmp("ERROR_QR", (char *)InterpretBuf, 8) == 0)
				{
					sscanf((char *)InterpretBuf,"ERROR_QR", rpi_error_qr );
				}

				// Able to see the QR Code
				if (strncmp("DIST_QR:", (char *)InterpretBuf, 8) == 0)
				{
					sscanf((char *)InterpretBuf,"DIST_QR:[%d]", rpi_distance_qr );
				}
				/************** Command to open a specific cell of the letter box *****************/
//				if (strncmp("OPEN_CELL:", (char *)InterpretBuf, 11) == 0)
//				{
//					int cell_number = 0;
//					char cell_number_str[10];
//
//					// Convert to integer the number sent alongside the command
//					strncpy(cell_number_str, (char *)InterpretBuf+10, Size-10);
//					cell_number = atoi(cell_number_str);
//
//					// Ask to open the corresponding cell
//					Open_Cell(cell_number);
//				}
//
//				/*********************** Confirmation cell can be opened **************************/
//				else if (strncmp("OK_CELL", (char *)InterpretBuf, 8) == 0)
//				{
//					// Send back acknowledge signal to signal good reception of valid message
//					Send_Msg("ACK", 3, "rpi");
//				}

//				else if (strncmp("u", (char *)InterpretBuf, 2) == 0)
//				{
//					// Send back acknowledge signal to signal good reception of valid message
//					Send_Msg("digo", 4, "ser");
//				}

				/****************************** Incorrect command *********************************/
//				else
//				{
//					// Send back error message, meaning the command isn't a valid one
//					Send_Msg((char *)"INVALID_COMMAND", 15, "rpi");
//				}
			}

			else if (strncmp("ser", dev, 3) == 0)
			{
				if (strncmp("nop", (char *)InterpretBuf, 3) == 0)
				{
					Send_Msg((char *)"nope xd", 7, "ser");
				}
				else if (strncmp("u", (char *)InterpretBuf, 2) == 0)
				{
					// Send back acknowledge signal to signal good reception of valid message
					Send_Msg("digo", 4, "rpi");
				}
				else
				{
					// Send back error message, meaning the command isn't a valid one
					Send_Msg((char *)"INVALID_COMMAND", 15, "ser");
				}

			}
		}

		interpreter_running = 0; // Function can be executed now
	}
}

/**
  * @brief Opens the cell identified by cell_number, if possible
  * @retval None
  */
void Open_Cell(int cell_number)
{
	char open_cell_str[20];

	// Valid cell
	if (cell_number >= CELL_NUM_MIN && cell_number <= CELL_NUM_MAX)
	{
		// Send back a confirmation question about the cell to open (prevent data corruption)
		sprintf(open_cell_str, "CONF_CELL:%i", cell_number);
		Send_Msg((char *)open_cell_str, strlen(open_cell_str), "rpi");
	}
	else // Invalid cell number
	{
		Send_Msg((char *)"INVALID_CELL_NB", 15, "rpi");
	}
}
