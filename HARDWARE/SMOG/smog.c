/**********************************************************************************
 * �ļ���  ��key.c
 * ����    ������ɨ��(ϵͳ�δ�ʱ��SysTickʵ��ɨ����ʱ)
 * ʵ��ƽ̨��NiRen_TwoHeartϵͳ��
 * Ӳ�����ӣ�  PB1 -> KEY1     
 *             PB2 -> KEY2       
 * ��汾  ��ST_v3.5
**********************************************************************************/
#include "stm32f10x.h"
#include "smog.h" 
#include "delay.h"
#include "sys.h" 

/*******************************************************************************
* ������  : Key_GPIO_Config
* ����    : KEY IO����
* ����    : ��
* ���    : ��
* ����    : �� 
* ˵��    : KEY���õ�����Ϊ:PA4-7
*******************************************************************************/
void Smoke_GPIO_Config(void)
{
	GPIO_InitTypeDef  GPIO_InitStructure;				//����һ��GPIO_InitTypeDef���͵�GPIO��ʼ���ṹ��
	
	RCC_APB2PeriphClockCmd(Smokedt_RCC, ENABLE);			//ʹ��GPIOA������ʱ��	
	
	GPIO_InitStructure.GPIO_Pin = SK;			//ѡ��Ҫ��ʼ����GPIOA����(PB1,PB2)
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;		//�������Ź���ģʽΪ�������� 		
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;	//������������������Ϊ50MHz
	GPIO_Init(Smokedt_PORT, &GPIO_InitStructure);			//���ÿ⺯���е�GPIO��ʼ����������ʼ��GPIOA�е�PB1,PB2����
}

/*******************************************************************************
* ������  : Smoke_Detection
* ����    : ������
* ����    : GPIOx��������Ӧ��GPIO��GPIO_Pin����Ӧ�����˿�
* ���    : ��
* ����    : KEY_DOWN(0):��Ӧ�������£�KEY_UP(1):��Ӧ����û����
* ˵��    : KEY���õ�����Ϊ:PA4-7
*******************************************************************************/
u8 Smoke_Detection(void)
{			
	if(GPIO_ReadInputDataBit(GPIOA,SK) == Smokedt_Y)	//����Ƿ������� 
	{	   
		delay_ms(10);	//��ʱ����		
		if(GPIO_ReadInputDataBit(GPIOA,SK) == Smokedt_Y)	//����Ƿ�������  
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

