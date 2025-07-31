#ifndef __KEY_H
#define	__KEY_H

#include "stm32f10x.h"

//KEY端口定义
#define Smokedt_RCC   RCC_APB2Periph_GPIOA 
#define Smokedt_PORT	GPIOA 
#define SK GPIO_Pin_12
//#define KEY_RCC     RCC_APB2Periph_GPIOA                           
//#define KEY_PORT	GPIOA  
//#define KEY0        GPIO_Pin_4    
//#define KEY1        GPIO_Pin_5
//#define KEY2        GPIO_Pin_6    
//#define KEY3        GPIO_Pin_7 

// 烟雾传感器状态
#define Smokedt_Y			0	// 有烟雾检出  
#define Smokedt_N			1	// 无烟雾检出
//#define KEY_DOWN	0
//#define KEY_UP		1

void Smokedt_GPIO_Config(void);
u8 Smoke_Detection(void);
//u16 Key_Down_Scan(void);

#endif 

