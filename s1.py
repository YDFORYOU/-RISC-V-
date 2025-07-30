import os
import cv2
import datetime
import numpy as np
import time
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device
from gpiozero import LED
from base.detection import Detection
from base.recognition import Recognition

# 初始化GPIO设备
Device.pin_factory = LGPIOFactory(chip=0)
blue = LED(71)
green = LED(72)
red = LED(73)

def setup_leds():
    """初始化所有LED为关闭状态"""
    red.off()
    green.off()
    blue.off()

def control_leds(name):
    """根据识别到的人名控制不同的LED灯"""
    # 关闭所有LED
    setup_leds()
    
    # 根据识别到的人名点亮对应的LED
    if name == "Person1":
        red.on()
    elif name == "Person2":
        green.on()
    elif name == "Person3":
        blue.on()
    else:
        # 未知人员，保持所有灯关闭
        setup_leds()

def recognize_face():
    print("🟢 启动人脸识别模式：")
    det_model_path = "onnx_model/yolov5n-face_320_cut.q.onnx"
    rec_model_path = "onnx_model/arcface_mobilefacenet_cut.q.onnx"
    faces_path = "faces"

    det = Detection(det_model_path)
    rec = Recognition(rec_model_path, faces_path)

    cap = cv2.VideoCapture(20)  # 根据摄像头编号调整

    # 初始化LED状态
    setup_leds()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ 无法读取摄像头")
                break

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
                    
                    # 控制LED灯
                    if name != "Unknown":
                        control_leds(name)

            for name, box in results.items():
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                if name != "Unknown":
                    cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"✅ 识别到: {name} - 时间: {now}")

            cv2.imshow("Face Recognition", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("🛑 按下 q，程序退出识别模式")
                break

    finally:
        setup_leds()  # 退出时关闭所有LED
        cap.release()
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
            setup_leds()  # 退出时关闭所有LED
            break

if __name__ == "__main__":
    main()