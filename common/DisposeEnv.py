from tools import ReadJson,ReadRedis,ReadDB,ReadConfig
from common import FormatConversion,RunMain
import json


class DisposeEnv:
    def __init__(self):
        self.readenvjsonhandle = ReadJson.ReadJson('Env','ENV')
        self.readrelyjsonhandle = ReadJson.ReadJson('RelyOn','RELYON')
        self.readredishandle = ReadRedis.ReadRedis()
        self.readdbhandle = ReadDB.ReadDB()

        self.readconfighandle = ReadConfig.ReadConfig()
        self.version = self.readconfighandle.get_data('INTERFACE','version_num')

        self.formatconversionhandle = FormatConversion.FormatConversion()
        self.runmethodhandle = RunMain.RunMethod()

    def set_env(self,data):
        if data['环境是否依赖'] == '是':
            jsondata = self.readenvjsonhandle.get_json_data()[data['依赖数据']]
            if "redis" in jsondata:
                for envdata in jsondata['redis']:
                    if envdata['nodetype'] == 'Hash':
                        if envdata['nodeoperation'] == 'Add':
                            self.readredishandle.hashsetall(envdata['name'],envdata['key'],envdata['value'])
                        elif envdata['nodeoperation'] == 'Delete':
                            self.readredishandle.hashdelall(envdata['name'],envdata['key'])
                    elif envdata['nodetype'] == 'String':
                        pass
                    elif envdata['nodetype'] == 'List':
                        pass
                    elif envdata['nodetype'] == 'Set':
                        pass                             
            if "sql" in jsondata:
                self.readdbhandle.modify_data(jsondata['sql'])

            if "api" in jsondata:
                relydata = self.readrelyjsonhandle.get_json_data()
                for envdata in jsondata['api']:
                    data = self.set_dict_value(envdata,relydata)
                
                if data["url"] == 'url_system':
                    url = self.readconfighandle.get_data('INTERFACE','url_system')
                else:
                    url = self.readconfighandle.get_data('INTERFACE','url_app')
                all_url = url + data["api"].format(version = self.version)
                all_header = data["header"]
                all_payload = data["payload"]
                all_method = data["method"]

                r = self.runmethodhandle.run_main(all_url,all_method,all_header,all_payload)
                if r.status_code == 200:
                    if "set_rely" in data:
                        self.set_rely(data['set_rely'],r)
                else:
                    print('接口创建测试环境失败')
    
    #查询每个value，如果存在rely_开头,直接替换并返回
    def set_dict_value(self,env_dict,rely_dict):
        if type(env_dict) is dict:
            for key in env_dict.keys():  # 迭代当前的字典层级
                data = env_dict[key]  # 将当前字典层级的第一个元素的值赋值给data

                # 如果当前data属于dict类型, 进行回归
                if isinstance(data, dict):
                    if key =='set_rely':
                        continue
                    self.set_dict_value(data,rely_dict)
                elif isinstance(data, list):
                    for data1 in data:
                        self.set_dict_value(data1,rely_dict)
                else:
                    if "rely_" in data:
                        env_dict[key] = self.get_rely_json(data)
        return env_dict

    #获取依赖json值
    def get_rely_json(self,case_api_relyed):
        jsondata = self.readrelyjsonhandle.get_json_data()
        jsonrelydata  = self.formatconversionhandle.FormatConversion(case_api_relyed,jsondata)
        return jsonrelydata

    def set_rely(self,data,r):
        jsondata = self.readrelyjsonhandle.get_json_data()
        fromdata = data["fromdata"]
        todata = data["todata"]
        #从返回json数据中获取存入字段的值
        reportdatavalue = self.formatconversionhandle.FormatConversion(fromdata,r.json())
        #重新赋值relyjson
        self.formatconversionhandle.FormatSet(reportdatavalue,todata,jsondata)
        self.readrelyjsonhandle.set_json_data(jsondata)

                    
                


