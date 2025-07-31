import os
import cv2
import datetime
import time
import RPi.GPIO as GPIO
import serial  # 导入串口库
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device
from gpiozero import LED, Servo
from base.detection import Detection
from base.recognition import Recognition
import pandas as pd  # 导入pandas用于处理Excel
import openpyxl  # 确保已安装：pip install openpyxl

# ---------------- 串口初始化 ----------------
# 定义USB串口配置
SERIAL_PORT = '/dev/ttyUSB0'  # 根据实际连接修改
BAUD_RATE = 9600
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)  # 1秒超时

# ---------------- GPIO + 舵机 + LED 初始化 ----------------
Device.pin_factory = LGPIOFactory(chip=0)

# LED GPIO 引脚
blue = LED(71)
green = LED(72)
red = LED(73)

# 舵机 GPIO 引脚
servo = Servo(70, min_pulse_width=0.0005, max_pulse_width=0.0025, frame_width=0.02)

# ---------------- DHT11 初始化 ----------------
DHTPIN = 18  # DHT11 所接 GPIO 引脚
GPIO.setmode(GPIO.BCM)

# ---------------- Excel文件初始化 ----------------
EXCEL_FILE = "attendance_records.xlsx"

# 创建Excel文件，如果不存在
if not os.path.exists(EXCEL_FILE):
    # 创建DataFrame并保存为Excel
    df = pd.DataFrame(columns=["姓名", "时间", "DHT温度(°C)", "DHT湿度(%)", "STM32温度(°C)", "烟雾浓度(ppm)"])
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
    print(f"📄 创建新的考勤记录文件: {EXCEL_FILE}")

def delay_ms(ms):
    time.sleep(ms / 1000.0)

def delay_us(us):
    time.sleep(us / 1000000.0)

def DHT11_Rst():
    GPIO.setup(DHTPIN, GPIO.OUT)
    GPIO.output(DHTPIN, GPIO.LOW)
    delay_ms(20)
    GPIO.output(DHTPIN, GPIO.HIGH)
    delay_us(30)

def DHT11_Check():
    GPIO.setup(DHTPIN, GPIO.IN)
    retry = 0
    while GPIO.input(DHTPIN) and retry < 100:
        retry += 1
        delay_us(1)
    if retry >= 100:
        return 1
    retry = 0
    while not GPIO.input(DHTPIN) and retry < 100:
        retry += 1
        delay_us(1)
    if retry >= 100:
        return 1
    return 0

def DHT11_Read_Bit():
    retry = 0
    while GPIO.input(DHTPIN) and retry < 100:
        retry += 1
        delay_us(1)
    retry = 0
    while not GPIO.input(DHTPIN) and retry < 100:
        retry += 1
        delay_us(1)
    delay_us(40)
    return GPIO.input(DHTPIN)

def DHT11_Read_Byte():
    data = 0
    for i in range(8):
        data <<= 1
        if DHT11_Read_Bit():
            data |= 1
    return data

def DHT11_Read_Data():
    DHT11_Rst()
    if DHT11_Check() == 0:
        data = [DHT11_Read_Byte() for _ in range(5)]
        if sum(data[:4]) & 0xFF == data[4]:
            humidity = data[0]
            temperature = data[2]
            return 0, temperature, humidity
    return 1, None, None

# ---------------- 串口数据读取 ----------------
def read_serial_data():
    """从串口读取STM32发送的温度和烟雾数据"""
    try:
        if ser.in_waiting > 0:
            # 读取一行数据并解码
            line = ser.readline().decode('utf-8').strip()
            # 假设数据格式: "TEMP:25.5,SMOKE:120" 或类似
            if line.startswith("TEMP") and "SMOKE" in line:
                parts = line.split(',')
                temp_data = parts[0].split(':')[1]
                smoke_data = parts[1].split(':')[1]
                
                # 转换为浮点数
                stm_temp = float(temp_data)
                smoke = float(smoke_data)
                return stm_temp, smoke
    except Exception as e:
        print(f"⚠️ 串口读取错误: {e}")
    return None, None  # 返回None表示无有效数据

# ---------------- Excel记录函数 ----------------
def save_to_excel(name, time_str, temp, hum, stm_temp, smoke):
    """将记录保存到Excel表格"""
    try:
        # 读取现有Excel文件
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
        
        # 创建新记录
        new_record = pd.DataFrame([{
            "姓名": name,
            "时间": time_str,
            "DHT温度(°C)": temp,
            "DHT湿度(%)": hum,
            "STM32温度(°C)": stm_temp if stm_temp is not None else "",
            "烟雾浓度(ppm)": smoke if smoke is not None else ""
        }])
        
        # 合并新记录
        df = pd.concat([df, new_record], ignore_index=True)
        
        # 保存到Excel
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        print(f"📝 记录已保存到: {EXCEL_FILE}")
        
    except Exception as e:
        print(f"⚠️ Excel保存错误: {e}")

# ---------------- 控制方法 ----------------
def setup_leds():
    red.off()
    green.off()
    blue.off()

def control_leds(name):
    setup_leds()
    if name == "Person1":
        red.on()
    elif name == "Person2":
        green.on()
    elif name == "Person3":
        blue.on()

def rotate_servo():
    try:
        servo.value = 0.5
        time.sleep(0.3)
        servo.detach()
    except Exception as e:
        print(f"⚠️ 舵机控制错误: {e}")

# ---------------- 主识别逻辑 ----------------
def recognize_face():
    print("🟢 启动人脸识别模式：")
    det_model_path = "onnx_model/yolov5n-face_320_cut.q.onnx"
    rec_model_path = "onnx_model/arcface_mobilefacenet_cut.q.onnx"
    faces_path = "faces"

    det = Detection(det_model_path)
    rec = Recognition(rec_model_path, faces_path)

    cap = cv2.VideoCapture(20)
    setup_leds()
    
    # 初始化STM32传感器数据变量
    stm_temp = None
    smoke = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ 无法读取摄像头")
                break
                
            # 读取STM32的传感器数据（非阻塞式）
            new_stm_temp, new_smoke = read_serial_data()
            if new_stm_temp is not None:
                stm_temp = new_stm_temp
            if new_smoke is not None:
                smoke = new_smoke

            face_imgs, boxes = det.infer_face(frame)
            results = {}

            if face_imgs is not None:
                for i, (face_img, box) in enumerate(zip(face_imgs, boxes)):
                    face_vector = rec.infer(face_img)
                    name = "Unknown"
                    max_score = 0.0

                    for key, value in rec.face_bank.items():
                        score = face_vector @ value.T
                        if score[0][0] > max_score and score[0][0] > 0.6:
                            name = key
                            max_score = score[0][0]

                    results[name] = box

                    if name != "Unknown":
                        control_leds(name)
                        rotate_servo()

                        # 每次识别成功后读取温湿度
                        result, temperature, humidity = DHT11_Read_Data()
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # 组合所有传感器数据输出
                        output = f"✅ 识别到: {name} - 时间: {now} - TEMP: {temperature}°C HUM: {humidity}%"
                        
                        # 添加STM32传感器数据
                        if stm_temp is not None:
                            output += f" - STM_TEMP: {stm_temp}°C"
                        if smoke is not None:
                            output += f" - SMOKE: {smoke}ppm"
                            
                        print(output)
                        
                        # 保存记录到Excel
                        save_to_excel(name, now, temperature, humidity, stm_temp, smoke)

            for name, box in results.items():
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                if name != "Unknown":
                    cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("🛑 按下 q，退出识别模式")
                break

    finally:
        setup_leds()
        cap.release()
        GPIO.cleanup()
        ser.close()  # 关闭串口
        cv2.destroyAllWindows()

def record_face():
    print("🚀 启动人脸录入模式：")
    os.system("python3 save_face.py")

def main():
    print("🔵 正在进入人脸录入流程...")
    record_face()

    while True:
        user_input = input("👉 录入完成后请输入 '1' 启动识别模式，其他任意键退出：")
        if user_input.strip() == "1":
            recognize_face()
        else:
            print("🔚 程序已退出")
            setup_leds()
            GPIO.cleanup()
            ser.close()  # 关闭串口
            break

if __name__ == "__main__":
    main()