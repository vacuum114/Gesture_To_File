import os
import json


class MyFile(object):
    def __init__(self):
        self.Operation_to_File={"0":"1"}
        self.Dict_Init()

    def Dict_Init(self):
        current_file_path = os.path.abspath(__file__)
        # 获取当前文件所在文件夹
        current_file_path = os.path.dirname(current_file_path)
        current_file_path += "\\Operation_to_File.json"
        if not os.path.isfile(current_file_path):
            # 如果文件不存在，则创建文件
            temp_data={}
            with open(current_file_path, 'w') as file:
                json.dump(temp_data, file)
                
        with open(current_file_path,'r') as savejson:
            self.Operation_to_File=json.load(savejson)
    
    def Dict_Save(self):
        current_file_path = os.path.abspath(__file__)
        # 获取当前文件所在文件夹
        current_file_path = os.path.dirname(current_file_path)
        current_file_path += "\\Operation_to_File.json"
        with open(current_file_path,'w') as savejson:
            json.dump(self.Operation_to_File, savejson)
    
    def Add_Dict(self,Operation,File):
        #添加新操作失败，因为该操作已有
        if(Operation in self.Operation_to_File):
            return False
        self.Operation_to_File[Operation]=File
        return True
    
    def Del_Dict(self,Operation):
        self.Operation_to_File.pop(Operation)

    
    def Which_File(self,Operation):
        #检查该操作是否被定义
        if(Operation in self.Operation_to_File):
            return self.Operation_to_File[Operation]
        else:
            return "无效操作"
        
    def Open_File(self,Operation):
        # 要打开的.doc文件路径
        file_path = self.Operation_to_File[Operation]
        # 检查文件是否存在
        if os.path.exists(file_path):
            try:
                # 使用默认关联程序打开文件
                os.startfile(file_path)
                print(f"文件 '{file_path}' 已在桌面上打开")
            except Exception as e:
                print(f"发生错误：{e}")
        else:
            print(f"文件 '{file_path}' 不存在")


    
    


    
