import wx
import cv2
import numpy as np
import time
from MyFile import MyFile
from MainPanel import MainPanel
from SettingPanel import SettingPanel

MyFile_Object=MyFile()
class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.MainPanelObject = MainPanel(self,MyFile_Object)
        self.SettingPanelObject = SettingPanel(self,MyFile_Object)
        self.SetWindowStyleFlag(wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)  # 禁止调整窗口大小
        #设置主界面大小及位置
        self.MainPanelObject.SetSize((500,400))
        self.MainPanelObject.SetPosition((0,0))
        
        self.SettingPanelObject.SetSize((400,300))
        self.SettingPanelObject.SetPosition((0,0))
        self.MainPanelObject.Show()
        self.SettingPanelObject.Hide()

        self.setting_button = wx.Button(self.MainPanelObject, label="设置",pos=(300,0))
        self.back_button = wx.Button(self.SettingPanelObject,label="返回",pos=(100,230))
        self.setting_button.Bind(wx.EVT_BUTTON, self.on_setting_button)
        self.back_button.Bind(wx.EVT_BUTTON,self.click_back_button)

        #

        self.Bind(wx.EVT_CLOSE, self.on_close)
        

    def on_setting_button(self, event):
        self.MainPanelObject.Hide()
        self.SettingPanelObject.Show()
        
    def click_back_button(self,event):
        self.SettingPanelObject.Hide()
        self.MainPanelObject.Show()

    def on_close(self, event):
        MyFile_Object.Dict_Save()
        event.Skip()

app = wx.App(False)
frame = MyFrame(None, title="OpenCV + wxPython 示例", size=(400, 300))
frame.Show()
app.MainLoop()
