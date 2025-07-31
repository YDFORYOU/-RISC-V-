/**********************************************************************************
 * 文件名  ：key.c
 * 描述    ：按键扫描(系统滴答时钟SysTick实现扫描延时)
 * 实验平台：NiRen_TwoHeart系统板
 * 硬件连接：  PB1 -> KEY1     
 *             PB2 -> KEY2       
 * 库版本  ：ST_v3.5
**********************************************************************************/
#include "stm32f10x.h"
#include "smog.h" 
#include "delay.h"
#include "sys.h" 

/*******************************************************************************
* 函数名  : Key_GPIO_Config
* 描述    : KEY IO配置
* 输入    : 无
* 输出    : 无
* 返回    : 无 
* 说明    : KEY设置的引脚为:PA4-7
*******************************************************************************/
void Smoke_GPIO_Config(void)
{
	GPIO_InitTypeDef  GPIO_InitStructure;				//定义一个GPIO_InitTypeDef类型的GPIO初始化结构体
	
	RCC_APB2PeriphClockCmd(Smokedt_RCC, ENABLE);			//使能GPIOA的外设时钟	
	
	GPIO_InitStructure.GPIO_Pin = SK;			//选择要初始化的GPIOA引脚(PB1,PB2)
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;		//设置引脚工作模式为上拉输入 		
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;	//设置引脚输出最大速率为50MHz
	GPIO_Init(Smokedt_PORT, &GPIO_InitStructure);			//调用库函数中的GPIO初始化函数，初始化GPIOA中的PB1,PB2引脚
}

/*******************************************************************************
* 函数名  : Smoke_Detection
* 描述    : 烟雾检测
* 输入    : GPIOx：按键对应的GPIO，GPIO_Pin：对应按键端口
* 输出    : 无
* 返回    : KEY_DOWN(0):对应按键按下，KEY_UP(1):对应按键没按下
* 说明    : KEY设置的引脚为:PA4-7
*******************************************************************************/
u8 Smoke_Detection(void)
{			
	if(GPIO_ReadInputDataBit(GPIOA,SK) == Smokedt_Y)	//检测是否有烟雾 
	{	   
		delay_ms(10);	//延时消抖		
		if(GPIO_ReadInputDataBit(GPIOA,SK) == Smokedt_Y)	//检测是否有烟雾  
		{	 
			// while(GPIO_ReadInputDataBit(GPIOA,SK) == Smokedt_Y); 
			return Smokedt_Y; 
		}
		else
		{
			return Smokedt_N;
		}
	}
	else
	{
		return Smokedt_N;
	}
}

