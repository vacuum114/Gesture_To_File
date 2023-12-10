import wx
import cv2
import numpy as np
import time
import os
from MyFile import MyFile
from AddDialog import AddDialog


class SettingPanel(wx.Panel):
    def __init__(self, parent,MyFile_Object):
        super(SettingPanel, self).__init__(parent)
        self.MyFile_Object=MyFile_Object

        self.AddButton = wx.Button(self,label="添加操作",pos=(50,200))

        self.DelButton = wx.Button(self,label="删除操作",pos=(150,200))

        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10),size=(350,160))

        self.init_List_Ctrl()

        self.DelButton.Bind(wx.EVT_BUTTON, self.delete_confirm)
        self.AddButton.Bind(wx.EVT_BUTTON,self.add)

    def init_List_Ctrl(self):
        self.list_ctrl.InsertColumn(0, "操作")
        self.list_ctrl.InsertColumn(1, "文件")
        self.list_ctrl.SetColumnWidth(0,100)
        self.list_ctrl.SetColumnWidth(1,246)
        temp_dict=self.MyFile_Object.Operation_to_File
        temp_cnt=0
        for opera , file in temp_dict.items():
            self.list_ctrl.InsertItem(temp_cnt, opera)
            filename = os.path.basename(file)
            self.list_ctrl.SetItem(temp_cnt, 1, filename)
            temp_cnt+=1
    
    def refresh_List_Ctrl(self):
        self.list_ctrl.DeleteAllItems()
        temp_dict=self.MyFile_Object.Operation_to_File
        temp_cnt=0
        for opera , file in temp_dict.items():
            self.list_ctrl.InsertItem(temp_cnt, opera)
            filename = os.path.basename(file)
            self.list_ctrl.SetItem(temp_cnt, 1, str(filename))
            temp_cnt+=1
    
    def delete_confirm(self,event):
        index = self.list_ctrl.GetFirstSelected()
        if(index!=-1):
            opera = self.list_ctrl.GetItemText(index, col=0)
            file = self.list_ctrl.GetItemText(index, col=1)
            dlg = wx.MessageDialog(self, f"是否删除：\n操作:{opera}, 文件:{file}\n", "确认", wx.YES_NO | wx.ICON_INFORMATION)
            result = dlg.ShowModal()
            dlg.Destroy()

            if(result == wx.ID_YES):
                self.delete(opera)
        else:
            wx.MessageBox("没有选中的行！", "提示", wx.OK | wx.ICON_INFORMATION)
    
    def delete(self,opera):
        self.MyFile_Object.Del_Dict(opera)
        self.refresh_List_Ctrl()

    def add(self,event):
        dialog = AddDialog(self,self.MyFile_Object)
        self.refresh_List_Ctrl()

if __name__ == '__main__':
    MyFile_Object=MyFile()
    app = wx.App(False)
    frame = wx.Frame(None, title="Panel 位置设置示例", size=(400, 300))
    panel = SettingPanel(frame,MyFile_Object)
    frame.Show()
    app.MainLoop()