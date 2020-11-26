from tools import ReadConfig,ReadJson
from common import FormatConversion

class DisposeApi:
    def __init__(self,casename = None):
        self.readconfighandle = ReadConfig.ReadConfig()
        self.version = self.readconfighandle.get_data('INTERFACE','version_num')
        self.formatconversionhandle = FormatConversion.FormatConversion()
        self.readrelyjsonhandle = ReadJson.ReadJson('RelyOn','RELYON')
        self.readcasejsonhandle = ReadJson.ReadJson(casename,'CASE')

    #获取接口完整地址
    def get_url(self,data):
        if data['模块'] == 'system':
            url = self.readconfighandle.get_data('INTERFACE','url_system')
        elif data['模块'] == 'app':
            url = self.readconfighandle.get_data('INTERFACE','url_app')
        else:
            url = self.readconfighandle.get_data('INTERFACE','url_other')
        case_api = data['请求API']
        case_api_isrely = data['API是否依赖']
        if case_api_isrely == '是':
            case_data = {}
            case_api_rely= data['API依赖字段'].split(',')
            case_api_relyed = data['API被依赖字段'].split(',')
            for i in range(len(case_api_rely)):
                if "case_" in case_api_relyed[i]:
                    case_data[case_api_rely[i]] = self.get_case_json(case_api_relyed[i])
                elif "rely_" in case_api_relyed[i]:
                    case_data[case_api_rely[i]] = self.get_rely_json(case_api_relyed[i])
            case_url = url + case_api.format(version = self.version,**case_data)
        else:
            case_url = url + case_api.format(version = self.version)
        return case_url

    #获取依赖json值
    def get_rely_json(self,case_api_relyed):
        jsondata = self.readrelyjsonhandle.get_json_data()
        jsonrelydata  = self.formatconversionhandle.FormatConversion(case_api_relyed,jsondata)
        return jsonrelydata

    #获取用例json值
    def get_case_json(self,case_api_relyed):
        jsondata = self.readcasejsonhandle.get_json_data()
        jsonrelydata  = self.formatconversionhandle.FormatConversion(case_api_relyed,jsondata)
        return jsonrelydata
        

        