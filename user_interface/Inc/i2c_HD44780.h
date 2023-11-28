#ifndef __I2C_HD44780__H__
#define __I2C_HD44780__H__

#ifdef __cpluspluse
extern "C" {
#endif
#include "stm32f4xx_hal.h"

void lcd_init (void);   // initialize lcd
//void lcd_send_cmd (char cmd);  // send command to the lcd
//void lcd_send_data (char data);  // send data to the lcd
void lcd_disp_on(void);
void lcd_disp_off(void);
void lcd_home(void);
void lcd_clear_display(void);
void lcd_locate(uint8_t row, uint8_t column);
void lcd_put_cur(int row, int col);
void lcd_printchar(unsigned char ascode);
void lcd_print_string (char *str);  // print string to the lcd
void lcd_printf(const char *fmt, ...);
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin);

#ifdef __cplusplus
}
#endif

#endif
