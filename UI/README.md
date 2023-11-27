This directory explains how to operate the UI of BoardMaestro

We are going to establish UART connection between a STM32 board and another device through bluetooth interface

The LCD board diplays an array of numbers and letters that shows where the cursor is

# How to run
1. Installation IDE

   
[STM32cubeIDE install][stm32] (Window / Linux / Mac)

[stm32]: https://www.st.com/en/development-tools/stm32cubeide.html#get-software


2. Setup completed

    `You can find information about the settings below`

3. STM32 code Run

![run](https://github.com/pjb8051/BoardMaestro/assets/143582470/219a6aae-040e-4d23-b5a4-4ae755e1adcb)


4. Connect Bluetooth with PC

5. Python code run

# Setup imformaiton
`Warining : Need to check pin number location`
1.  IDE Settings
    * Board : stm32 NUCLEO-F429Zl
    * IDE : STM32cubeIDE

1-1 GPIO settings

![GPIO_setting](https://github.com/pjb8051/BoardMaestro/assets/143582470/06171568-49cf-4050-92ab-d5af98ad5a63)


PC0 = GPIO_EXTI0 / Pull-down

PC3 = GPIO_EXTI3 / Pull-down

1-2 I2C settings

![i2c_setting](https://github.com/pjb8051/BoardMaestro/assets/143582470/65b2312b-dfc7-4e58-b843-9bc74479a65f)


PB6 = SCL
PB9 = SDA

1-3 UART settings

![uart_setting](https://github.com/pjb8051/BoardMaestro/assets/143582470/c7225d91-f5ed-4ddc-95bd-8b5857868dc4)


USART2 = Asynchronous
Baud Rate = 9600 Bits/s

1-4 NVIC settings

![nvic_setting](https://github.com/pjb8051/BoardMaestro/assets/143582470/ee336114-41ed-42d5-ad9e-8266dd6d527a)


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


![1](https://github.com/pjb8051/BoardMaestro/assets/143582470/137cdc54-c36e-4a0f-a116-42f9887f09df)

