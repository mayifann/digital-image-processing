# 定义创建按钮的函数
import cv2

# 定义类
class drawButton:
    
    # 定义类属性
    w = 200
    h = 60
    angerLine = 15  # 角点线段长度
    thick = 3  # 角点线段厚度
    
    # 矩形框颜色
    colorBG = (255,255,0)  # 底色
    colorBL = (255,0,255) # 边界
    colorBA = (0,255,255) # 角点边线颜色
    
    # 初始化
    def __init__(self, classnames:list):
        
        # 分配属性
        self.classnames = classnames
        self.len = len(classnames)
    
    
    # 美化角点
    def drawAnger(self, img, x, y):
        
        cv2.line(img, (x,y), (x,y+self.angerLine), self.colorBA, self.thick)
        cv2.line(img, (x,y), (x+self.angerLine,y), self.colorBA, self.thick)
        cv2.line(img, (x+self.w,y), (x+self.w,y+self.angerLine), self.colorBA, self.thick)
        cv2.line(img, (x+self.w,y), (x+self.w-self.angerLine,y), self.colorBA, self.thick)
        cv2.line(img, (x,y+self.h), (x,y+self.h-self.angerLine), self.colorBA, self.thick)
        cv2.line(img, (x,y+self.h), (x+self.angerLine,y+self.h), self.colorBA, self.thick)
        cv2.line(img, (x+self.w,y+self.h), (x+self.w,y+self.h-self.angerLine), self.colorBA, self.thick)
        cv2.line(img, (x+self.w,y+self.h), (x+self.w-self.angerLine,y+self.h), self.colorBA, self.thick)

    
    # 定义绘图方法
    def drawRec_alone(self, img, x, y, name):
        
        # 透明矩形参数设置
        alphaReserve = 0.5  # 透明度
        BChannel, GChannel, RChannel = self.colorBG  # 设置矩形颜色 
        yMin, yMax = y, y+self.h  # 矩形框的y坐标范围
        xMin, xMax = x, x+self.w  # 矩形框的y坐标范围
        
        # 绘制透明矩形
        img[yMin:yMax, xMin:xMax, 0] = img[yMin:yMax, xMin:xMax, 0] * alphaReserve + BChannel * (1 - alphaReserve)
        img[yMin:yMax, xMin:xMax, 1] = img[yMin:yMax, xMin:xMax, 1] * alphaReserve + GChannel * (1 - alphaReserve)
        img[yMin:yMax, xMin:xMax, 2] = img[yMin:yMax, xMin:xMax, 2] * alphaReserve + RChannel * (1 - alphaReserve)
        
        # 矩形框边界
        cv2.rectangle(img, (x,y), (x+self.w, y+self.h), self.colorBL, 2)
        
        # 美化角点
        self.drawAnger(img, x, y)
        
        # 显示文本
        cv2.putText(img, name, (x+20, y+40), cv2.FONT_HERSHEY_COMPLEX, 1.3, (255,255,255), 3)


    # 绘制多个按钮框，保存每个按钮的左上坐标
    def drawRec_many(self, img):

        self.recList = []  # 存放每个矩形框的左上角坐标        

        # 每个分类绘制一个矩形框
        for i in range(self.len):
            
            # 分类名
            name = self.classnames[i]
            
            # 每个矩形框的左上角坐标
            recx = 10
            recy = 100*i+50
            
            # 保存在列表中
            self.recList.append([[recx, recy],  # 左上角
                                [recx+self.w, recy],  # 右上角
                                [recx+self.w, recy+self.h],  # 右下角
                                [recx, recy+self.h]  # 左下角
                                ])  
            
            # 每一个分类画一个矩形框
            # 10代表x位置，y=110*i+50，矩形框之间纵向间隔50
            self.drawRec_alone(img, recx, recy, name)
            
            
            




# filepath = 'C:\\GameDownload\\Deep Learning\\kings.jpg'
# img = cv2.imread(filepath)

# img = cv2.resize(img, (1280,720))

# draw = drawButton(['person', 'bus', 'car', 'mot', 'tree'])
# draw.drawRec_many(img)

# print(draw.recList)

# cv2.imshow('img', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
