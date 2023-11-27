This directory explains how to operate the UI of BoardMaestro

We are going to establish UART connection between a STM32 board and another device through bluetooth interface

The LCD board diplays an array of numbers and letters that shows where the cursor is

# How to run
1. Installation IDE
<br>
[STM32cubeIDE install][stm32] (Window / Linux / Mac)

[stm32]: https://www.st.com/en/development-tools/stm32cubeide.html#get-software


2. Setup completed

    `You can find information about the settings below`

3. STM32 code Run

![](/images/run.png)

4. Connect Bluetooth with PC

5. Python code run

# Setup imformaiton
`Warining : Need to check pin number location`
1.  IDE Settings
    * Board : stm32 NUCLEO-F429Zl
    * IDE : STM32cubeIDE

1-1 GPIO settings

![](/images/GPIO_setting.png)

PC0 = GPIO_EXTI0 / Pull-down

PC3 = GPIO_EXTI3 / Pull-down

1-2 I2C settings

![](/images/i2c_setting.png)

PB6 = SCL
PB9 = SDA

1-3 UART settings

![](/images/uart_setting.png)

USART2 = Asynchronous
Baud Rate = 9600 Bits/s

1-4 NVIC settings

![](/images/nvic_setting.png)

Endable list : 
    * EXTI line0 interrupt 
    * EXTI line3 interrupt 
    * I2C1 event interrupt 
    * I2C1 error interrupt 
    * USART2 global interrupt 
    * USART3 global interrupt 
    * EXTI line[15:10] interrupt

2. Use Module
    * I2C_LCD = LCD1602
    * Bluetooth = HC-06

3. Result


![](/images/1.gif)
