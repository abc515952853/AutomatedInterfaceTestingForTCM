from tools import ReadConfig,ReadJson,ReadDB,ReadRedis
from common import FormatConversion
import json,time

class DisposeReport:
    def __init__(self,casename=None):
        readconfighandle = ReadConfig.ReadConfig()
        self.url = readconfighandle.get_data('INTERFACE','url_app')
        self.version = readconfighandle.get_data('INTERFACE','version_num')
        self.formatconversionhandle = FormatConversion.FormatConversion()

        self.readreportjsonhandle = ReadJson.ReadJson(casename,'REPORT')
        self.readcasejsonhandle = ReadJson.ReadJson(casename)
        self.readdbhandle = ReadDB.ReadDB()
        self.readredishandle = ReadRedis.ReadRedis()

        self.readrelyjsonhandle = ReadJson.ReadJson('RelyOn','RELYON')

    #获取预期结果
    def get_report(self,data):
        time.sleep(2)
        case_report = data['预期结果']
        if case_report == '':
            return None
        #获取预期结果的json
        expecteddata = {}
        case_report = self.readreportjsonhandle.get_parameter(case_report)
        case_status_code = case_report['status_code']
        expecteddata["status_code"] = case_status_code

        #判断有无sql断言，如果没有则返回接口状态
        if "expected" in case_report:
            sql = case_report['expected']['sql']
            if "keyword" in case_report['expected']:
                # jsondata = self.readcasejsonhandle.get_json_data()
                keyword = case_report['expected']['keyword'].split(',') 
                #通过keyword从当前用例获得sql条件，拼装完整查询sql
                sqlword = {}
                for i in range(len(keyword)):
                    if "rely_" in keyword[i]:
                        jsondata = self.readrelyjsonhandle.get_json_data()
                    elif "case_" in keyword[i]:
                        jsondata = self.readcasejsonhandle.get_json_data()
                    sqlword[keyword[i].split('.')[-1]] = self.formatconversionhandle.FormatConversion(keyword[i],jsondata)
                sql = sql.format(**sqlword)

            #查询数据库获得需要断言字段
            if case_report['expected']['type'] == 'ONE':
                dbdata = self.readdbhandle.search_one(sql)
                if dbdata is not None:
                    if "datalist" in case_report['expected']:
                        for dl in case_report['expected']['datalist']:
                            dbdata[dl] = dbdata[dl].split(',')
                    if "expected2" in case_report['expected']:
                        for ex in case_report['expected']['expected2']:
                            if ex['type'] =='sql':
                                dbdata[ex['key']] = self.readdbhandle.search_all(ex['value'])
                else:
                    dbdata = {}
            elif case_report['expected']['type'] == 'ALL':
                dbdata = self.readdbhandle.search_all(sql)
                if dbdata is not None:
                    if "datalist" in case_report['expected']:
                        for dl in case_report['expected']['datalist']:
                            for data in dbdata:
                                if data[dl] is None:
                                    data[dl] = []
                                else:
                                    data[dl] = data[dl].split(',')
                    if "expected2" in case_report['expected']:
                        for ex in case_report['expected']['expected2']:
                            if ex['type'] =='sql':
                                dddata = self.readdbhandle.search_all(ex['value'])
                                for i in range(len(dbdata)):
                                    dbdata[i][ex['key']] = dddata[i]
                else:
                    dbdata = []
            expecteddata["expecteddata"] = dbdata
        
        if "expectedredis" in case_report:
            for redis in case_report['expectedredis']:
                redisql = redis['name']
                rediskey = redis['key']
                resultdata = {}
                if "keyword" in redis:
                    if "name" in redis['keyword']:
                        redisword = {}
                        for i in range(len(redis['keyword']['name'])):
                            if "rely_" in redis['keyword']['name'][i]:
                                jsondata = self.readrelyjsonhandle.get_json_data()
                            elif "case_" in redis['keyword']['name'][i]:
                                pass
                            keyword = redis['keyword']['name'][i].split(',') 
                            for ii in range(len(keyword)):
                                redisword[keyword[i].split('.')[-1]]=self.formatconversionhandle.FormatConversion(keyword[ii],jsondata)
                        name = redisql.format(**redisword)
                    if "key" in redis['keyword']:
                        redisword = {}
                        for i in range(len(redis['keyword']['key'])):
                            if "rely_" in redis['keyword']['key'][i]:
                                jsondata = self.readrelyjsonhandle.get_json_data()
                            elif "case_" in redis['keyword']['key'][i]:
                                pass
                            keyword = redis['keyword']['key'][i].split(',') 
                            for ii in range(len(keyword)):
                                redisword[keyword[i].split('.')[-1]]=self.formatconversionhandle.FormatConversion(keyword[ii],jsondata)
                        key = rediskey.format(**redisword)   
            if redis['nodetype'] == 'Hash':
                    pass
            elif redis['nodetype'] == 'String':
                pass
            elif redis['nodetype'] == 'List':
                pass
            elif redis['nodetype'] == 'Set':
                if redis['nodeoperation'] =='Get':
                    result = self.readredishandle.setsismember(name,key)
                    if result:
                        resultdata = redisword            
            if  "expecteddata" in expecteddata:
                expecteddata["expecteddata"].update(resultdata)
            else:
                expecteddata["expecteddata"] = resultdata

        #获取expectedother的预期结果
        if "expectedother" in case_report:
            if "expecteddata" in expecteddata:
                expecteddata["expecteddata"].update(case_report["expectedother"])
            else:
                expecteddata["expecteddata"] = case_report["expectedother"]

        if "asserttype" in case_report:
            if "expecteddata" in expecteddata:
                expecteddata['asserttype'].update(case_report['asserttype'])
            else:
                expecteddata['asserttype'] = case_report['asserttype']

        #遍历dict中的每个值
        expecteddata = self.get_dict_value(expecteddata)

        return expecteddata

    def get_dict_value(self,in_dict):
        if type(in_dict) is dict:
            for key in in_dict.keys():  # 迭代当前的字典层级
                data = in_dict[key]  # 将当前字典层级的第一个元素的值赋值给data

                # 如果当前data属于dict类型, 进行回归
                if isinstance(data, dict):
                    self.get_dict_value(data)
                elif isinstance(data, list):
                    for data1 in data:
                        self.get_dict_value(data1)
                else:
                    if type(data) is bytes:
                        if data == bytes([1]):
                            in_dict[key]  = True
                        else:
                            in_dict[key]  = False
                    if data is None:
                        in_dict[key] =""
        return in_dict
