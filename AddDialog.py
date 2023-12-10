import wx
from MyFile import MyFile
class AddDialog(wx.Dialog):
    def __init__(self, parent,MyFile,*args, **kw):
        super(AddDialog, self).__init__(parent, *args, **kw)

        self.panel = wx.Panel(self)
        self.MyFile = MyFile
    
        self.operations=[]
        self.filepath=""
        
        
        self.UpButton = wx.Button(self,label="向上",pos=(40,50),size=(40,30))
        self.DownButton = wx.Button(self,label="向下",pos=(90,50),size=(40,30))
        self.LeftButton = wx.Button(self,label="向左",pos=(140,50),size=(40,30))
        self.RightButton = wx.Button(self,label="向右",pos=(190,50),size=(40,30))
        self.DelButton = wx.Button(self,label="删除",pos=(240,50),size=(40,30))
        self.ChooseButton = wx.Button(self,label="选择文件",pos=(40,120),size=(60,30))
        self.ConfirmButton = wx.Button(self,label="确认添加",pos=(140,150),size=(120,30))
        self.operaLabel = wx.StaticText(
            self, label="操作:", pos=(10, 20))
        self.fileLabel = wx.StaticText(
            self, label="文件:", pos=(10, 90))
        
        self.UpButton.Bind(wx.EVT_BUTTON,self.click_Up_Button)
        self.DownButton.Bind(wx.EVT_BUTTON,self.click_Down_Button)
        self.LeftButton.Bind(wx.EVT_BUTTON,self.click_Left_Button)
        self.RightButton.Bind(wx.EVT_BUTTON,self.click_Right_Button)
        self.DelButton.Bind(wx.EVT_BUTTON,self.click_Del_Button)
        self.ChooseButton.Bind(wx.EVT_BUTTON,self.click_Choose_Button)
        self.ConfirmButton.Bind(wx.EVT_BUTTON,self.click_Confirm_Button)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Centre()
        self.ShowModal()
        self.Destroy()

    def on_close(self, event):
        self.Destroy()
    
    def refresh_OperaLabel(self):
        temp_str="操作:"
        for item in self.operations:
            temp_str+=item+" "
        self.operaLabel.SetLabel(temp_str)
    
    def click_Up_Button(self,event):
        if(len(self.operations)==3):
            wx.MessageBox("至多写入3个操作", "提示", wx.OK | wx.ICON_INFORMATION)
        elif(len(self.operations)==0 or self.operations[-1]!="Up"):
            self.operations.append("Up")
            self.refresh_OperaLabel()
        else:
            wx.MessageBox("不能连续输入两个相同的操作","提示",wx.OK | wx.ICON_INFORMATION)

    def click_Down_Button(self,event):
        if(len(self.operations)==3):
            wx.MessageBox("至多写入3个操作", "提示", wx.OK | wx.ICON_INFORMATION)
        elif(len(self.operations)==0 or self.operations[-1]!="Down"):
            self.operations.append("Down")
            self.refresh_OperaLabel()
        else:
            wx.MessageBox("不能连续输入两个相同的操作","提示",wx.OK | wx.ICON_INFORMATION)

    def click_Left_Button(self,event):
        if(len(self.operations)==3):
            wx.MessageBox("至多写入3个操作", "提示", wx.OK | wx.ICON_INFORMATION)
        elif(len(self.operations)==0 or self.operations[-1]!="Left"):
            self.operations.append("Left")
            self.refresh_OperaLabel()
        else:
            wx.MessageBox("不能连续输入两个相同的操作","提示",wx.OK | wx.ICON_INFORMATION)
    
    def click_Right_Button(self,event):
        if(len(self.operations)==3):
            wx.MessageBox("至多写入3个操作", "提示", wx.OK | wx.ICON_INFORMATION)
        elif(len(self.operations)==0 or self.operations[-1]!="Right"):
            self.operations.append("Right")
            self.refresh_OperaLabel()
        else:
            wx.MessageBox("不能连续输入两个相同的操作","提示",wx.OK | wx.ICON_INFORMATION)
    
    def click_Del_Button(self,event):
        if(len(self.operations)>0):
            self.operations.pop()
            self.refresh_OperaLabel()
    
    def refresh_FileLabel(self):
        self.fileLabel.SetLabel(self.filepath)
    
    def click_Choose_Button(self,event):
         with wx.FileDialog(self, "选择文件", wildcard="All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            self.filepath = file_dialog.GetPath()
            self.refresh_FileLabel()
    
    def click_Confirm_Button(self,event):
        temp_str=str(self.operations)
        if (temp_str=="[]"):
            wx.MessageBox("请输入操作","提示",wx.OK|wx.ICON_INFORMATION)
        elif(self.filepath==""):
            wx.MessageBox("请选择文件","提示",wx.OK|wx.ICON_INFORMATION)
        elif(temp_str in self.MyFile.Operation_to_File):
            wx.MessageBox("该操作已被使用", "提示", wx.OK | wx.ICON_INFORMATION)
        else:
            self.MyFile.Add_Dict(temp_str,self.filepath)
            self.operations=[]
            self.filepath=""
            self.refresh_FileLabel()
            self.refresh_OperaLabel()
            wx.MessageBox("添加成功", "提示", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)

MyFile_Object=MyFile()
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(400, 300))

        panel = wx.Panel(self)
        button = wx.Button(panel, label="Show Dialog", pos=(10, 10))
        self.Bind(wx.EVT_BUTTON, self.on_show_dialog, button)

        self.Centre()
        self.Show()

    def on_show_dialog(self, event):
        dialog = AddDialog(self,MyFile_Object)

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, "Frame Example")
    app.MainLoop()

    