/*
 * ble.c
 *
 *  Created on: Oct 18, 2023
 *      Author: IoT08
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "string.h"
#include "main.h"
#include "led.h"
#include "cli.h"
#include "uart.h"
#include "ble.h"
#include "i2c_hd44780.h"

extern UART_HandleTypeDef huart2;

void ble_init(void){
  printf("HELLO!!!\n");
}

void ble(void){
  uart_init();
  led_init();
  cli_init();
  ble_init();
  lcd_init();
  lcd_disp_on();
  lcd_clear_display();
  lcd_home();

  while(1)
     {
       uart_proc();
     }
 }

