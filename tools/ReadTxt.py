import sys
import os
from common import IsSkip

class ReadTxt:
    def __init__(self,filename):
        proDir = os.getcwd()#获取当前目录
        self.txtPath = os.path.join(proDir, "configurationfile\{0}.txt".format(filename))
        self.caseList = []

    def read_txt(self):
        try:
            self.fb = open(self.txtPath)
            IsSkip.IsSkip().write_isskip('Yes')
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)
    
    def close_txt(self):
        self.fb.close()

    #获取txt文件中需要执行的接口
    def get_case_list(self):
        self.read_txt()
        for value in self.fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        self.close_txt()
        return self.caseList

    #获取txt文件中需要清除数据库数据语句
    def get_clear_data(self):
        self.read_txt()
        return self.fb.readlines()


# if __name__ == "__main__":
#     a = ReadTxt()
#     a.get_case_list()
