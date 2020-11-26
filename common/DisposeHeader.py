from tools import ReadConfig,ReadJson
from common import FormatConversion
import json

class DisposeHeader:
    def __init__(self):
        readconfighandle = ReadConfig.ReadConfig()
        self.url = readconfighandle.get_data('INTERFACE','url_app')
        self.version = readconfighandle.get_data('INTERFACE','version_num')
        self.systemtoken = readconfighandle.get_data('INTERFACE','system_token')
        self.formatconversionhandle = FormatConversion.FormatConversion()
        self.readheaderjsonhandle = ReadJson.ReadJson('Header','HEADER')
        self.readrelyjsonhandle = ReadJson.ReadJson('RelyOn','RELYON')

    #获取接口完整地址
    def get_header(self,data):
        case_header = data['请求头']
        if case_header == '':
            return None

        case_header = self.readheaderjsonhandle.get_parameter(case_header)
        if data['模块'] == 'system':
            case_header['Authorization'] = self.systemtoken
            return case_header

        if "Authorization" not in case_header:
            return case_header
        
        case_header_isrely = data['请求头是否依赖']
        if case_header_isrely == '是':
            case_header_rely= data['请求头依赖字段'].split(',')
            case_header_relyed = data['请求头被依赖字段'].split(',')
            for i in range(len(case_header_rely)):
                case_header[case_header_rely[i]] = self.get_rely_json(case_header_relyed[i])
        return case_header

    #获取依赖json值
    def get_rely_json(self,case_api_relyed):
        jsondata = self.readrelyjsonhandle.get_json_data()
        jsonrelydata  = self.formatconversionhandle.FormatConversion(case_api_relyed,jsondata)
        return jsonrelydata
