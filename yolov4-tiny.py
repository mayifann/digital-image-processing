# yolov4-tiny目标检测
import cv2
import numpy as np
from myFunction import drawButton


#（1）导入yolov4-tiny网络模型结构
# 传入模型结构.cfg文件，模型权重参数.weight文件
net = cv2.dnn.readNet('dnn_model\yolov4-tiny.cfg', 'dnn_model\yolov4-tiny.weights')

# 定义一个目标检测模型，将模型传进去
model = cv2.dnn_DetectionModel(net)

'''
设置模型的输入
size：将输入的图像缩放至指定大小。size越大检测效果越好，但是检测速度越慢
scale：像素值的缩放大小。在opencv中每个像素值的范围在0-255之间，而在神经网络中每个像素值在0-1之间
'''
model.setInputParams(size=(416, 416), scale=1/255)


#（2）获取分类文本的信息
classes = []  # 存放每个分类的名称
with open('dnn_model\classes.txt') as file_obj:
    # 获取文本中的每一行
    for class_name in file_obj.readlines():
        # 删除文本中的换行符、空格等
        class_name = class_name.strip()
        # 将每个分类名保存到列表中
        classes.append(class_name)


#（3）视频捕获
filepath = 'F:\\yolov4-tiny\\1.mp4'
cap = cv2.VideoCapture(filepath)  


#（4）创建鼠事件
# 创建按钮，默认停用
button_class = False
button_index = None  # 存放哪个按键被点亮了

# 定义鼠标回调函数
def click_button(event, x, y, flags, params):
    
    # 调用外部变量
    global button_class
    global button_index
    
    # 设置事鼠标件event为点击鼠标左键
    if event == cv2.EVENT_LBUTTONDOWN:
        
        # 检查鼠标的坐标是否在矩形框按键内部，index代表第几个按钮
        # 遍历每个矩形框，每个框包含四个角的坐标
        for index, pt in enumerate(np.array(buttonList)):  # 要转换成numpy类型  
            
            # 如果设为True，计算鼠标左键距离矩形框的距离
            is_inside = cv2.pointPolygonTest(pt, (x,y), False)
            
            if is_inside > 0:  # 鼠标在矩形框内部
                
                print(f'click in the No.{index+1}', (x,y))
                
                # 如果鼠标点击位置在矩形框内部，并且上一次没点击
                if button_class == False:
                    # 激活按钮
                    button_class = True
                    # 激活哪个分类的检测框
                    button_index = index
                    
            
            # 如果鼠标点击位置不在矩形框内部
            else:
                  button_class = False
                

#（5）创建窗口
cv2.namedWindow('Image')  # 窗口名和显示图像的窗口名相同

# 设置鼠标回调，窗口名和上面相同，自定义回调函数
cv2.setMouseCallback('Image', click_button)

# 创建按钮
usenames = ['all', 'person', 'car', 'bus', 'truck']
button = drawButton(usenames)


#（6）定义检测框绘制函数
colorline = (0,255,0)  # 角点线段颜色
angerline = 13  # 角点线段长度

def drawbbx(img, x, y, w, h, predName, score):
    
    # 检测框
    cv2.rectangle(img, (x, y), (x+w, y+h), (255,255,0), 1)
    # 角点美化
    cv2.line(img, (x,y), (x+angerline,y), colorline, 2)
    cv2.line(img, (x,y), (x,y+angerline), colorline, 2)    
    cv2.line(img, (x+w,y), (x+w,y+angerline), colorline, 2)
    cv2.line(img, (x+w,y), (x+w-angerline,y), colorline, 2)
    cv2.line(img, (x,y+h), (x,y+h-angerline), colorline, 2)
    cv2.line(img, (x,y+h), (x+angerline,y+h), colorline, 2)
    cv2.line(img, (x+w,y+h), (x+w,y+h-angerline), colorline, 2)    
    cv2.line(img, (x+w,y+h), (x+w-angerline,y+h), colorline, 2)
    
    # 显示预测的类别
    cv2.putText(img, predName, (x,y+h+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
    
    # 显示预测概率
    cv2.putText(img, str(int(score*100))+'%', (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)
    


#（6）对每一帧视频图像处理
while True:
    
    # 返回是否读取成功ret和读取的帧图像frame
    ret, frame = cap.read()
    
    # 图像比较大把它缩小一点
    frame = cv2.resize(frame, (1280,720))
    
    # 视频比较短，循环播放
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        
        # 如果当前帧==总帧数，那就重置当前帧为0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    
    # 目标检测
    '''
    返回值
    classids：检测得到的类别
    score：检测得到的目标的概率
    bbox：检测框的85项信息
    参数
    confThreshold：目标检测最小置信度
    nmsThreshold：非极大值抑制的自定义参数
    '''
    classids, scores, bboxes = model.detect(frame, 0.5, 0.3)
    
    # 在画面上创建按钮
    button.drawRec_many(frame)
    
    # 获取所有矩形框的四个角的坐标
    buttonList = button.recList  
    
    
    #（7）显示检测结果
    # 遍历所有的检测框信息，把它们绘制出来
    for class_id, score, bbox in zip(classids, scores, bboxes):
        
        # 获取检测框的左上角坐标和宽高
        x, y, w, h = bbox
        
        # 获取检测框对应的分类名
        class_name = classes[class_id]
        
        
        # 遍历四个按键的名称
        for index, name in enumerate(usenames):
        
            # 设置检测条件，只有检测到的类别是person并且鼠标点击位置在矩形框内
            if class_name == name and index == button_index:
            
                # 绘制class_name类别的检测框
                drawbbx(frame, x, y, w, h, class_name, score)                
            
            elif name == 'all' and index == button_index:
                
                # 绘制所有类别的检测框
                drawbbx(frame, x, y, w, h, class_name, score)

    # 显示图像
    cv2.imshow('Image', frame)  #窗口名，图像变量
    if cv2.waitKey(30) & 0xFF==27:  #每帧滞留1毫秒后消失
        break

# 释放视频资源
cap.release()
cv2.destroyAllWindows()

