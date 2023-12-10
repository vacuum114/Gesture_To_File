import wx
import cv2
import numpy as np
import time
from MyFile import MyFile

class MainPanel(wx.Panel):
    def __init__(self, parent,MyFile_Object):
        super(MainPanel, self).__init__(parent)

        self.MyFile=MyFile_Object

        self.last_time=time.time()
        self.drawing = False
        self.direction = None
        self.pre_direction = None
        self.confirm_directions = []
        self.confirm_cnt = 0
        self.ix, self.iy = -1, -1 #ix,iy为移动前的坐标
        self.x,self.y=-1,-1
        self.img = np.ones((300, 400, 3), np.uint8) * 255  # 初始化为白色背景

        self.bitmap = wx.Bitmap(self.img.shape[1], self.img.shape[0])
        self.buffer = wx.Bitmap(self.img.shape[1], self.img.shape[0])

        self.direction_text = wx.StaticText(
            self, label="操作: 无", pos=(10, 10))
        self.file_text = wx.StaticText(
            self, label="文件: 无", pos=(10, 30))

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_window)

        self.Refresh()


    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)
        dc.DrawBitmap(self.bitmap, 0, 0)

    def on_left_down(self, event):
        self.drawing = True
        self.ix, self.iy = event.GetPosition()
        self.last_time=time.time()

    def on_mouse_move(self, event):
        if self.drawing:
            self.x, self.y = event.GetPosition()
            cv2.line(self.img, (self.ix, self.iy), (self.x, self.y), (0, 0, 0), 2)  # 画线为黑色
            self.bitmap.CopyFromBuffer(self.img)
            #设置每次判断的间隔：25ms
            if(time.time()-self.last_time>0.010):
                self.check_mouse_direction(event)
                self.last_time=time.time()
            self.Refresh()

    def on_left_up(self, event):
        self.drawing = False
        self.ix, self.iy = -1, -1  # 重置起始点
        self.img = np.ones((300, 400, 3), np.uint8) * 255  # 清除线条，重置为白色背景
        self.Open_File()
        self.confirm_directions.clear()
        self.direction_text.SetLabel("操作: 无")
        self.file_text.SetLabel("文件: 无")
        self.bitmap.CopyFromBuffer(self.img)
        self.Refresh()
    
    def on_leave_window(self, event):
        if self.drawing:
            # 模拟一个虚拟的 EVT_LEFT_UP 事件
            fake_left_up_event = wx.MouseEvent(wx.wxEVT_LEFT_UP)
            wx.PostEvent(self, fake_left_up_event)

    def check_mouse_direction(self, event):
        dx = self.x - self.ix
        dy = self.y - self.iy
        
        #判断是否原地不动
        if(dx**2+dy**2<100):
            self.direction="Stay"
            return 
        #判断移动角度
        angle = np.arctan2(dy, dx) * 180 / np.pi
        if angle < 0:
            angle += 360
        self.pre_direction=self.direction
        if 45 <= angle < 135:
            self.direction = "Down"
        elif 135 <= angle < 225:
            self.direction = "Left"
        elif 225 <= angle < 315:
            self.direction = "Up"
        else:
            self.direction = "Right"
        self.ix=self.x
        self.iy=self.y
        self.confirm_direction()
        
    def confirm_direction(self):
        if(self.pre_direction == None or self.direction == None or self.direction == "Stay"):
            return
        if(self.direction == self.pre_direction):
            self.confirm_cnt += 1
            if(self.confirm_cnt == 3):
                if(len(self.confirm_directions) == 0 or self.confirm_directions[len(self.confirm_directions)-1] != self.direction):
                    self.confirm_directions.append(self.direction)
                    self.direction_text.SetLabel(f"操作: {self.confirm_directions}")
                    self.file_text.SetLabel(self.MyFile.Which_File(str(self.confirm_directions)))
                self.confirm_cnt = 0
        else:
            self.confirm_cnt = 0
    def Open_File(self):
        temp_str=str(self.confirm_directions)
        if(temp_str in self.MyFile.Operation_to_File):
            self.MyFile.Open_File(temp_str)