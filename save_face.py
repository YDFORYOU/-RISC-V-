import cv2
import onnxruntime as ort
import os
from base.detection import Detection
from base.recognition import Recognition
import numpy as np

def main():
    det_model_path = "onnx_model/yolov5n-face_320_cut.q.onnx"  
    rec_model_path = "onnx_model/arcface_mobilefacenet_cut.q.onnx"

    faces_folder = "faces"
    if not os.path.exists(faces_folder):
        os.makedirs(faces_folder)
    det = Detection(det_model_path)
    rec = Recognition(rec_model_path,faces_folder)
    

    cap = cv2.VideoCapture(20)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法获取摄像头画面")
            break

        # 检测人脸 
        face_img,boxes = det.infer_face(frame)
        
        # 画框
        if boxes is not None:
            for box in boxes:            
                x1, y1, x2, y2 = box  
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        cv2.imshow("Face Detection", frame)

        # 按 's' 键保存人脸
        print("点击摄像头界面,按 's' 键保存人脸,按 'q' 键退出")
        key = cv2.waitKey(1)
        if key == ord('s'):
            face_name = input("请输入人脸名: ")
            save_folder = "faces"
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            face_vec = rec.infer(face_img[0])

            save_path = os.path.join(save_folder, f"{face_name}.npy")
            np.save(save_path, face_vec)
            # cv2.imwrite(save_path, face_img)            
            print(f"人脸特征已保存到 {save_path}")

        # 按 'q' 键退出
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()