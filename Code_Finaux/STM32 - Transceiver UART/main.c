

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "transceiver_uart.h"
#include "msg_interpreter.h"
#include "string.h"


/* USER CODE BEGIN PV */
uint8_t transceiver_clk = 0;

/* USER CODE END PV */


/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  	if (htim==&htim3) // Every 100µs
  	{
  		transceiver_clk = 1;
  	}
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
 
  /* USER CODE BEGIN 2 */
  Init_DMA_Rcvd(&huart1);
  Init_DMA_Rcvd(&huart6);
  Start_DMA_Rcvd(&huart1); // Start reception of messages
  Start_DMA_Rcvd(&huart6);
  HAL_TIM_Base_Start_IT(&htim3); // Start timer

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	if (transceiver_clk == 1)
	{
		transceiver_clk = 0;
		UART_Send_Messages(&huart1, &huart6); // Send to-send messages through UART
		// Retrieve and interpret a message received through UART
		Interpret_Message_Recv();
	}
  }
  /* USER CODE END 3 */
}

