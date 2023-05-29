void Start_DMA_Rcvd(UART_HandleTypeDef *huart);
void Init_DMA_Rcvd(UART_HandleTypeDef *huart);
void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size);
int Retrieve_Msg(uint8_t *InterpretBuf, char *dev);

void HAL_UART_TxHalfCpltCallback(UART_HandleTypeDef *huart);
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart);
void UART_Send_Messages(UART_HandleTypeDef *huart0, UART_HandleTypeDef *huart1);
void Send_Msg(char *msg, int Size, char *dev);
