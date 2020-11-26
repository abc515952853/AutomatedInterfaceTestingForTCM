from tools import ReadConfig,ReadJson,ReadExcl
from common import FormatConversion
import json


class DisposeCase:
    def __init__(self,casename=None):
        if casename is not None:
            self.casedata = ReadExcl.ReadExcl(casename).get_xls_next()

        readconfighandle = ReadConfig.ReadConfig()
        self.url = readconfighandle.get_data('INTERFACE','url_app')
        self.version = readconfighandle.get_data('INTERFACE','version_num')
        self.formatconversionhandle = FormatConversion.FormatConversion()
        self.readcasejsonhandle = ReadJson.ReadJson(casename)
        self.readrelyjsonhandle = ReadJson.ReadJson('RelyOn','RELYON')

    #剔除是否执行为否的用例
    def get_case_data(self):
        casedata = []
        for data in self.casedata:
            if data['是否执行'] == '是':
                casedata.append(data)
        return casedata

    def get_payload(self,data):
        case_payload = data['请求参数']
        if case_payload == '':
            return None

        case_payload = self.readcasejsonhandle.get_parameter(case_payload)

        case_payload_isrely = data['请求参数是否依赖']
        if case_payload_isrely == '是':
            case_payload_rely= data['请求参数依赖字段'].split(',')
            case_payload_relyed = data['请求参数被依赖字段'].split(',')
            for i in range(len(case_payload_rely)):
                # case_payload[case_payload_rely[i]] = self.get_rely_json(case_payload_relyed[i])
                # print(case_payload,case_payload_rely[i],self.get_rely_json(case_payload_relyed[i]))
                self.set_case_payload(case_payload,case_payload_rely[i],self.get_rely_json(case_payload_relyed[i]))
        return case_payload

    #获取依赖json值
    def get_rely_json(self,case_api_relyed):
        jsondata = self.readrelyjsonhandle.get_json_data()
        jsonrelydata  = self.formatconversionhandle.FormatConversion(case_api_relyed,jsondata)
        return jsonrelydata

    def set_case_payload(self,case_payload,case_payload_rely,get_rely_json):
        for c in case_payload.keys():
            if c == case_payload_rely:
                case_payload[c] = get_rely_json
            else:
                if type(case_payload[c]) is list:
                
                elif type(case_payload[c]) is list:






