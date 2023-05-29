#ifndef __MAIN_C__
	#define __MAIN_C__
	#include "main.h"
#endif

#include "stdio.h"
#include "string.h"
#include "transceiver_uart.h"

// Buffer sizes
#define RxBuf_SIZE		50
#define MainRxBuf_SIZE	300
#define TxBuf_SIZE		300
#define MSG_MAX_SIZE	50

// Maximum number of messages to be received/rdy to transmit before being processed
#define NB_RX_MSG_MAX		20
#define NB_TX_MSG_MAX		20

#define NB_UART				2
#define UART0_NAME			"rpi" // Name to refer to Rpi on Send_Message
#define UART1_NAME			"ser" // Name to refer to Serializer on Send_Message

// Global handlers

UART_HandleTypeDef huartArr[2];


/**********************************************************************************/
/******************** Variables for the reception of messages *********************/
/**********************************************************************************/

// UART buffers
uint8_t Rx_Buf1[RxBuf_SIZE];
uint8_t Rx_Buf2[RxBuf_SIZE];
uint8_t MainRxBuf[MainRxBuf_SIZE];

// Buffers positions pointers
uint16_t oldPos_Rx;
uint16_t newPos_Rx;

/* Variables and buffers for keeping track of messages received and not yet processed */
uint16_t recv_msg_read_pos = 0; // Position for reading oldest msg start/size still to be processed
uint16_t recv_msg_write_pos = 0; // Position for writing next msg start/size
uint16_t recv_msg_cnt = 0; // Number of messages to be processed
uint16_t recv_msg_start[NB_RX_MSG_MAX]; // Starting index for all messages still to be processed
uint16_t recv_msg_size[NB_RX_MSG_MAX]; // Size of all messages still to be processed
//UART_HandleTypeDef *recv_msg_huart[NB_RX_MSG_MAX]; // UART Handle for each message received
char recv_msg_dev[NB_RX_MSG_MAX][4]; // Devices from which msg is received

/* Arrays for managing the list of devices connected to UART ports */
/* List of names for devices
 * Here : Raspberry Pi (rpi), Serializer (ser)
 */
//char deviceArr[2][4] = ["rpi", "ser"};
//UART_HandleTypeDef *deviceHandleArr[2] = {NULL, NULL};

/**********************************************************************************/
/******************** Functions for the reception of messages *********************/
/**********************************************************************************/

void Init_DMA_Rcvd(UART_HandleTypeDef *huart)
{
	if (huart->Instance == USART1)
	{
		huartArr[0] = *huart;
	}
	else if (huart->Instance == USART3)
	{
		huartArr[1] = *huart;
	}
}

/**
  * @brief Initialize DMA Reception and save UART Handlers (huart) in an array
  * @retval None
  */
void Start_DMA_Rcvd(UART_HandleTypeDef *huart)
{
	if (huart->Instance == USART1)
	{
		//SCB_InvalidateDCache_by_Addr((uint32_t*)(((uint32_t)Rx_Buf1) & ~(uint32_t)0x1F), RxBuf_SIZE+32);
		HAL_UARTEx_ReceiveToIdle_DMA(huart, (uint8_t *) Rx_Buf1, RxBuf_SIZE);
	}
	else if (huart->Instance == USART3)
	{
		//SCB_InvalidateDCache_by_Addr((uint32_t*)(((uint32_t)Rx_Buf2) & ~(uint32_t)0x1F), RxBuf_SIZE+32);
		HAL_UARTEx_ReceiveToIdle_DMA(huart, (uint8_t *) Rx_Buf2, RxBuf_SIZE);
	}
}

/**
  * @brief Callback function for RX uart, dont forget to start DMA in main file (use last two lines of this function)
  * @retval None
  */
void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size)
{
	uint16_t datatocopy;

	if (recv_msg_cnt < NB_RX_MSG_MAX)
	{
		uint8_t *Rx_Buf;
		if ((&huartArr[0])->Instance == huart->Instance)
		{
			Rx_Buf = Rx_Buf1;
			strncpy(recv_msg_dev[recv_msg_write_pos], UART0_NAME, 4);
		}
		else if ((&huartArr[1])->Instance == huart->Instance)
		{
			Rx_Buf = Rx_Buf2;
			strncpy(recv_msg_dev[recv_msg_write_pos], UART1_NAME, 4);
		}

		// Position updating
		oldPos_Rx = newPos_Rx; // Update the last position before copying new data
		//uint16_t currPos_Rx = newPos_Rx;

		// Copy to MainRxBuf from Rx_Buf
		if (oldPos_Rx+Size > MainRxBuf_SIZE)  // If the current position + new data size is greater than the main buffer
		{
			datatocopy = MainRxBuf_SIZE-oldPos_Rx;  // find out how much space is left in the main buffer
			newPos_Rx = (Size-datatocopy);  // update the position
			memcpy ((uint8_t *)MainRxBuf+oldPos_Rx, Rx_Buf, datatocopy);  // copy data in that remaining space
			memcpy ((uint8_t *)MainRxBuf, (uint8_t *)Rx_Buf+datatocopy, (Size-datatocopy));  // copy the remaining data
		}
		else
		{
			newPos_Rx = Size+oldPos_Rx;
			memcpy ((uint8_t *)MainRxBuf+oldPos_Rx, Rx_Buf, Size);
		}

		recv_msg_start[recv_msg_write_pos] = oldPos_Rx; // Add new msg's start position
		recv_msg_size[recv_msg_write_pos] = Size; // Add new msg's size
		recv_msg_cnt++; // New message added
		recv_msg_write_pos++; // Update position for next msg
		if (recv_msg_write_pos == NB_RX_MSG_MAX) // Cycle position if at the end of array
		{
			recv_msg_write_pos = 0;
		}
	}

	/* start the DMA again */
	Start_DMA_Rcvd(huart);
}

/**
  * @brief Retrieves one new message in main buffer (FIFO)
  * @retval Size of message, 0 if no new message
  */
int Retrieve_Msg(uint8_t *InterpretBuf, char *dev)
{
	if (recv_msg_cnt > 0) // Make sure there is a new msg to interpret
	{
		/**********************************************************************************/
		/*************** Copy new message from Main Buffer to InterpretBuf ****************/
		/**********************************************************************************/
		/* Buffer for copying from MainBuf when processing data
		 * to avoid */
		//uint8_t InterpretBuf[RxBuf_SIZE];

		// Get Position, Size and Source of received message
		uint16_t startPos = recv_msg_start[recv_msg_read_pos];
		uint16_t Size = recv_msg_size[recv_msg_read_pos];
		strncpy(dev, recv_msg_dev[recv_msg_read_pos], 4);

		// Update position of next message and message count
		recv_msg_read_pos++;
		recv_msg_cnt--; // One less message to interpret
		if (recv_msg_read_pos == NB_RX_MSG_MAX) // Cycle position if at the end of array
		{
			recv_msg_read_pos = 0;
		}

		/* Copy data from MainBuf to InterpretBuf */
		if (startPos+Size > MainRxBuf_SIZE) // Data looped back at some point to beginning of buffer
		{
			uint16_t datatocopy = MainRxBuf_SIZE-startPos;  // find out how much space is left in the main buffer
			memcpy (InterpretBuf, (uint8_t *)MainRxBuf+startPos, datatocopy);  // Copy first half to beginning of InterpretBuf
			memcpy ((uint8_t *)InterpretBuf+datatocopy, MainRxBuf, (Size-datatocopy));  // copy the remaining data
			InterpretBuf[Size-datatocopy] = '\0'; // End copied string with null char (signal end of string)
		}
		else // Data isn't looped from end to start of buffer (continuous ;D)
		{
			memcpy (InterpretBuf, (uint8_t *)MainRxBuf+startPos, Size);  // copy the remaining data
			InterpretBuf[Size] = '\0'; // End copied string with null char (signal end of string)
		}

		return Size;
	}
	else
	{
		return 0;
	}
}


/**********************************************************************************/
/****************** Variables for the transmission of message *********************/
/**********************************************************************************/

// Management of when interruptions should call send functions
uint8_t uart_sending_msgs = 0; // To 1 when UART_Send_Messages is being executed

// UART buffer for sending messages messages
uint8_t Tx_Buf[TxBuf_SIZE];
uint8_t UART_send_buff[MSG_MAX_SIZE]; // Concatenation buffer for circular capability
//uint8_t UART_send_buff2[MSG_MAX_SIZE]; // Concatenation buffer for circular capability

// Buffers positions pointers
uint16_t oldPos_Tx = 0;
uint16_t newPos_Tx = 0;

/* Variables and buffers for keeping track of messages to be sent */
uint16_t send_msg_read_pos = 0; // Position for reading oldest msg start/size still to be sent
uint16_t send_msg_write_pos = 0; // Position for writing next msg start/size to be sent
uint16_t send_msg_cnt = 0; // Number of messages to be sent
uint16_t send_msg_start[NB_TX_MSG_MAX]; // Starting index for all messages still to be sent
uint16_t send_msg_size[NB_TX_MSG_MAX]; // Size of all messages still to be sent
char send_msg_dev[NB_TX_MSG_MAX][4]; // Devices to send messages to

uint8_t msg_end_of_tx = 1; // Indicates if transmission of msg is done


/**********************************************************************************/
/******************* Functions for the transmission of messages *******************/
/**********************************************************************************/

void HAL_UART_TxHalfCpltCallback(UART_HandleTypeDef *huart){}

/**
  * @brief Callback function for TX uart, signaling end of transmission with variable inside
  * @retval None
  */
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
	msg_end_of_tx = 1; // Ready to send a new message
}

void UART_Send_Messages(UART_HandleTypeDef *huart0, UART_HandleTypeDef *huart1)
{
	// Remaining msgs to send, none currently being transmitted and only instance
	// of this function currently being executed
	if (send_msg_cnt > 0 && msg_end_of_tx == 1 && uart_sending_msgs == 0)
	{
		char dev[4];

		uart_sending_msgs = 1; // So this function does not compute twice
							   // at the same time.
		msg_end_of_tx = 0; // Indicate a message is to be sent shortly  to prevent
						   // trying to send through uart 2 msgs at the same time

		uint16_t startPos = send_msg_start[send_msg_read_pos];
		uint16_t Size = send_msg_size[send_msg_read_pos];
		strncpy(dev, send_msg_dev[send_msg_read_pos], 4);
		send_msg_cnt--; // One less message to interpret
		// Update the position of msgs info read
		send_msg_read_pos++;
		if (send_msg_read_pos == NB_TX_MSG_MAX) // Cycle position if at the end of array
		{
			send_msg_read_pos = 0;
		}

		if (startPos+Size > TxBuf_SIZE)  // If the current position + new data size is greater than the main buffer
		{
			uint16_t datatocopy = TxBuf_SIZE-startPos;  // find out how much space is left in the main buffer

			memcpy (UART_send_buff, Tx_Buf+startPos, datatocopy);
			memcpy (UART_send_buff+datatocopy, Tx_Buf, Size-datatocopy);
		}
		else
		{
			memcpy (UART_send_buff, Tx_Buf + startPos, Size);
		}

		/* Clean D-cache */
		/* Make sure the address is 32-byte aligned and add 32-bytes to length, in case it overlaps cacheline */
		//SCB_CleanDCache_by_Addr((uint32_t*)(((uint32_t)UART_send_buff) & ~(uint32_t)0x1F), MSG_MAX_SIZE+32);

		/* DMA Transmit */
		if (strncmp(dev, UART0_NAME, 3) == 0)
		{
			//HAL_UART_Transmit_DMA(&huartArr[0], UART_send_buff, Size);
			HAL_UART_Transmit_IT(huart0, UART_send_buff, Size);

		}
		else if (strncmp(dev, UART1_NAME, 3) == 0)
		{
			//HAL_UART_Transmit_DMA(&huartArr[1], UART_send_buff, Size);
			HAL_UART_Transmit_IT(huart1, UART_send_buff, Size);
		}

		uart_sending_msgs = 0; // Function ready to be called again
	}
}

/**
  * @brief Add a new message to the buffer of messages to be sent through UART
  * @retval None
  */
void Send_Msg(char *msg, int Size, char *dev)
{
	uint16_t currPos_Tx = newPos_Tx; // Store start of current message received (to transmit to interpreter later)
	uint16_t datatocopy;

	if (send_msg_cnt < NB_TX_MSG_MAX)
	{
		oldPos_Tx = newPos_Tx;  // Update the last position before copying new data

		if (currPos_Tx+Size > TxBuf_SIZE)  // If the current position + new data size is greater than the main buffer
		{
			datatocopy = TxBuf_SIZE-currPos_Tx;  // find out how much space is left in the main buffer
			newPos_Tx = (Size-datatocopy);  // update the position
			memcpy ((uint8_t *)Tx_Buf+currPos_Tx, msg, datatocopy);  // copy data in that remaining space
			memcpy ((uint8_t *)Tx_Buf, (uint8_t *)msg+datatocopy, (Size-datatocopy));  // copy the remaining data
		}
		else
		{
			newPos_Tx = Size+currPos_Tx;
			memcpy ((uint8_t *)Tx_Buf+currPos_Tx, msg, Size);
		}

		send_msg_start[send_msg_write_pos] = currPos_Tx; // Add new msg's start position
		send_msg_size[send_msg_write_pos] = Size; // Add new msg's size
		strncpy(send_msg_dev[send_msg_write_pos], dev, 4); // Copy device name
		send_msg_cnt++; // New message added
		send_msg_write_pos++; // Update position for next msg
		if (send_msg_write_pos == NB_TX_MSG_MAX) // Cycle position if at the end of array
		{
			send_msg_write_pos = 0;
		}
	}
}


