import os
import subprocess

def main():
    while True:
        print("\n请选择功能：")
        print("1. 人脸录入")
        print("2. 人脸识别")
        print("q. 退出程序")
        choice = input("请输入选项 (1/2/q)：").strip()

        if choice == '1':
            print("🟢 启动人脸录入模块，请按提示操作...")
            os.system("python3 save_face.py")
        elif choice == '2':
            print("🟢 启动人脸识别模块，请按 'q' 键退出识别...")
            os.system("python3 face_det_rec.py --use_single_thread")
        elif choice.lower() == 'q':
            print("👋 退出程序，再见！")
            break
        else:
            print("❗ 无效输入，请重新选择。")

if __name__ == '__main__':
    main()
11