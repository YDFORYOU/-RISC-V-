import time
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device
from gpiozero import LED

# 显式指定/dev/gpiochip0
Device.pin_factory = LGPIOFactory(chip=0)

# 初始化 GPIO 控制的设备
blue = LED(71)
green = LED(72)
red = LED(73)

# 定义控制灯的函数
def blink_lights():
    while True:
        # 红灯亮，绿蓝灯灭
        red.on()
        green.off()
        blue.off()
        time.sleep(1)

        # 绿灯亮，红蓝灯灭
        red.off()
        green.on()
        blue.off()
        time.sleep(1)

        # 蓝灯亮，红绿灯灭
        red.off()
        green.off()
        blue.on()
        time.sleep(1)

# 启动灯光交替闪烁
blink_lights()
