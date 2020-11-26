import os
import codecs
import configparser

class ReadConfig:
    def __init__(self):
        proDir = os.getcwd()#获取当前目录
        self.configPath = os.path.join(proDir, "configurationfile\config.ini")
    
    def read_config(self):
        try:
            self.fb = open(self.configPath,encoding='utf-8-sig')
            data = self.fb.read()

            #  remove BOM
            if data[:3] == codecs.BOM_UTF8:
                data = data[3:]
                file = codecs.open(self.configPath, "w")
                file.write(data)
                file.close()
            self.fb.close()

            self.cf = configparser.ConfigParser()
            self.cf.read(self.configPath,encoding='utf-8-sig')
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)
    
    #获取ini所有session
    def get_sections(self):
        self.read_config()
        sections =  self.cf.sections()
        return sections

    #获取ini所有Session中的options
    def get_options(self,section):
        self.read_config()
        options =  self.cf.options(section)
        return options

    #获取INTERFACE信息
    def get_data(self,sessionname,optionname):
        self.read_config()
        value = self.cf.get(sessionname,optionname)
        return value

    ##重设ini信息
    def set_data(self,sessionname,optionname,value):
        self.read_config()
        self.cf.set(sessionname,optionname,value)
        self.cf.write(open(self.configPath, "w",encoding='utf-8-sig'))