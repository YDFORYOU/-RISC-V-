# 环境安装

<!-- ## 下载代码

下载源码压缩包：[face_det_rec.zip](code/ai_demo/face_det_rec.zip)

解压命令：

```bash
unzip face_det_rec.zip -d ~/
``` -->

## 安装系统依赖

```
sudo apt update
sudo apt install python3-venv
```

## 安装Python依赖

（1）创建Python虚拟环境

```
python3 -m venv ~/.venv
```

（2）配置 pip 源为进迭时空镜像源

```
pip config set global.extra-index-url https://git.spacemit.com/api/v4/projects/33/packages/pypi/simple
```

（3）安装项目依赖

```
cd ~/face_det_rec
source ~/.venv/bin/activate
pip install opencv-python==4.6.8.1
pip install pillow==11.2.1
```

# 程序启动

进入项目目录并激活虚拟环境

```
cd ~/face_det_rec
source ~/.venv/bin/activate
```

## 人脸注册

首先需要注册人脸到人脸库中，在终端中执行以下程序：

```python
python save_face.py
```

检测到人脸后，尽量保证正面的人脸出现在检测框内；点击摄像头界面，按s进入人脸名输入环节，在终端可以看到"请输入人脸名"的提示，点击终端，输入人脸名，最后人脸保存在faces目录下。保存完之后，按q键退出。

## 人脸识别主程序

执行以下程序开始人脸检测：

```python
python face_det_rec.py
```

检测到人脸后，会框出人脸并标记提前录好的人脸名。