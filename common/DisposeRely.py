from tools import ReadJson,ReadDB
from common import FormatConversion
import json


class DisposeRely:
    def __init__(self):
        self.formatconversionhandle = FormatConversion.FormatConversion()
        self.readrelyjsonhandle = ReadJson.ReadJson('RelyOn','RELYON')
        self.readdbhandle = ReadDB.ReadDB()

    def set_rely(self,data,r):
        #是否存入依赖
        if data['是否存入依赖'] == '是':
            jsondata = self.readrelyjsonhandle.get_json_data()
            if data['存入字段'] != '':
                fromdata = data['存入字段'].split(',')
                todata = data['保存字段'].split(',')
                jsondata = self.readrelyjsonhandle.get_json_data()
                for i in range(len(fromdata)):
                    #从返回json数据中获取存入字段的值
                    reportdatavalue = self.formatconversionhandle.FormatConversion(fromdata[i],r.json())
                    #重新赋值relyjson
                    self.formatconversionhandle.FormatSet(reportdatavalue,todata[i],jsondata)
            if data['存入sql'] != '':
                dbdata = self.readdbhandle.search_one(data['存入sql'])
                todata = data['保存sql值'].split(',')
                for i in range(len(todata)):
                    self.formatconversionhandle.FormatSet(dbdata[todata[i].split('.')[-1]],todata[i],jsondata)
            self.readrelyjsonhandle.set_json_data(jsondata)


