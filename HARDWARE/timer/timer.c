#include "timer.h"
#include "led.h"

void TIM2_Int_Init(u16 arr,u16 psc)
{
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStrue;
	NVIC_InitTypeDef NVIC_InitStructure;
	
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2,ENABLE);
	
	TIM_TimeBaseInitStrue.TIM_Period=arr;
	TIM_TimeBaseInitStrue.TIM_Prescaler=psc;
	TIM_TimeBaseInitStrue.TIM_CounterMode=TIM_CounterMode_Up;
	TIM_TimeBaseInitStrue.TIM_ClockDivision=TIM_CKD_DIV1;
	TIM_TimeBaseInit(TIM2,&TIM_TimeBaseInitStrue);
	
	TIM_ITConfig(TIM2,TIM_IT_Update,ENABLE);
	
	NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;  //TIM3�ж�
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;  //��ռ���ȼ�0��
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 3;  //�����ȼ�3��
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; //IRQͨ����ʹ��
	NVIC_Init(&NVIC_InitStructure);  //����NVIC_InitStruct��ָ���Ĳ�����ʼ������NVIC�Ĵ���
	
	TIM_Cmd(TIM2,ENABLE);
	
}

void TIM2_IRQHandler(void)
{
	if(TIM_GetITStatus(TIM2,TIM_IT_Update)!=RESET)
	{
		//LED0=!LED0;
		TIM_ClearITPendingBit(TIM2,TIM_IT_Update);
	}
	
}


void TIM2_PWM_Init(u16 arr,u16 psc)
{
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStrue;
	GPIO_InitTypeDef  GPIO_InitStructure;
	TIM_OCInitTypeDef TIM_OCInitTypeStrue;
	
	GPIO_PinRemapConfig(GPIO_Remap_SWJ_JTAGDisable, ENABLE);	
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2,ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA|RCC_APB2Periph_AFIO,ENABLE);
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_15;				 //LED0-->PB.5 �˿�����
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP; 		 //�������
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;		 //IO���ٶ�Ϊ50MHz
	GPIO_Init(GPIOA, &GPIO_InitStructure);					 //�����趨������ʼ��GPIOB.5
	GPIO_SetBits(GPIOA,GPIO_Pin_15);
	
	GPIO_PinRemapConfig(GPIO_PartialRemap1_TIM2,ENABLE);
	
	TIM_TimeBaseInitStrue.TIM_Period=arr;
	TIM_TimeBaseInitStrue.TIM_Prescaler=psc;
	TIM_TimeBaseInitStrue.TIM_CounterMode=TIM_CounterMode_Up;
	TIM_TimeBaseInitStrue.TIM_ClockDivision=TIM_CKD_DIV1;
	TIM_TimeBaseInit(TIM2,&TIM_TimeBaseInitStrue);
	
	TIM_OCInitTypeStrue.TIM_OCMode=TIM_OCMode_PWM2;
	TIM_OCInitTypeStrue.TIM_OCPolarity=TIM_OCPolarity_High;
	TIM_OCInitTypeStrue.TIM_OutputState=TIM_OutputState_Enable;
	TIM_OC1Init(TIM2,&TIM_OCInitTypeStrue);
	
	TIM_OC1PreloadConfig(TIM2,TIM_OCPreload_Enable);
	
	TIM_Cmd(TIM2,ENABLE);
}


