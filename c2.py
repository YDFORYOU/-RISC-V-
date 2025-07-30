import os
import cv2
import datetime
import numpy as np
from base.detection import Detection
from base.recognition import Recognition

def record_face():
    print("🚀 启动人脸录入模式：")
    os.system("python3 save_face.py")

def recognize_face():
    print("🟢 启动人脸识别模式：")
    det_model_path = "onnx_model/yolov5n-face_320_cut.q.onnx"
    rec_model_path = "onnx_model/arcface_mobilefacenet_cut.q.onnx"
    faces_path = "faces"

    det = Detection(det_model_path)
    rec = Recognition(rec_model_path, faces_path)

    cap = cv2.VideoCapture(20)  # 根据摄像头编号调整，如果你使用20号，就写20

    seen_names = set()

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

            for name, box in results.items():
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                if name != "Unknown":
                    cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # 输出信息到终端，不去重，可多次识别输出
                    print(f"✅ 识别到: {name} - 时间: {now}")

            cv2.imshow("Face Recognition", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("🛑 按下 q，程序退出识别模式")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

def main():
    print("🔵 正在进入人脸录入流程...")
    record_face()

    while True:
        user_input = input("👉 录入完成后请输入 '1' 启动识别模式，其他任意键退出：")
        if user_input.strip() == "1":
            recognize_face()
        else:
            print("🔚 程序已退出")
            break

if __name__ == "__main__":
    main()
