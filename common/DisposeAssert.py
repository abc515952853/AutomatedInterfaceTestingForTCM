import unittest
import types

class DisposeAssert(unittest.TestCase):
    def AssertReport(self,expectedreport,apireport):
        print('----------------------------------------------')
        print("用例预期结果：")
        print(expectedreport)
        print("接口返回结果：")
        print(apireport)
        print('----------------------------------------------')
        if type(expectedreport) is dict:
            for c in expectedreport.keys():
                default = self.dict_get(apireport,c,None)
                self.assertIsNotNone(default)
                self.assertEqual(expectedreport[c],default)
        elif type(expectedreport) is list:
            # self.assertListEqual(expectedreport,apireport)
            self.assertEqual(len(expectedreport),len(apireport))
            for i in range(len(expectedreport)):
                if type(expectedreport[i]) is dict:
                    for c in expectedreport[i].keys():
                        default = self.dict_get(apireport[i],c,None)
                        self.assertIsNotNone(default)
                        self.assertEqual(expectedreport[i][c],default)
                else:
                    self.assertEqual(expectedreport[i],apireport[i])
            
    def dict_get(self,dict, objkey, default):
        tmp = dict
        for k,v in tmp.items():
            if k == objkey:
                return v
            else:
                if type(v) is dict:
                    ret = self.dict_get(v, objkey, default)
                    if ret is not default:
                        return ret
        return default
