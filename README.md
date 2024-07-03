# digital-image-processing
# 道路目标检测系统

本项目实现了一个基于YOLOv4-Tiny的选择性目标检测系统。系统可以检测视频流中的车辆、卡车、公交车和行人，并允许用户通过交互按钮选择需要检测的对象类别。

## 功能
- 检测视频中的车辆、卡车、公交车和行人。
- 用户可通过按钮选择要检测的对象类别。
- 实时视频处理和目标检测。

## 使用
1. **运行目标检测脚本**：
    ```sh
    python yolov4-tiny.py
    ```

2. **选择目标类别**：
    - 使用视频窗口上的按钮选择要检测的目标类别（车辆、卡车、公交车、行人）。

3. **退出**：
    - 按`ESC`键停止检测并关闭视频窗口。

## 文件说明
- `yolov4-tiny.py`：主脚本，运行目标检测系统。
- `myFunction.py`：包含用于创建和处理交互按钮的`drawButton`类。
- `dnn_model/`：包含YOLOv4-Tiny模型配置和权重的目录。
    - `yolov4-tiny.cfg`：YOLOv4-Tiny配置文件。
    - `yolov4-tiny.weights`：YOLOv4-Tiny预训练权重。
    - `classes.txt`：包含YOLOv4-Tiny模型类别名称的文件。
