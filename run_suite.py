import unittest
import datetime
import os
from tools import ReadTxt,HTMLTestReportCN,Smtp,ReadJson

class Runtest:
    def __init__(self):
        proDir = os.getcwd()#获取当前目录
        self.executionPath = os.path.join(proDir, "testcaseperform")
        self.reportPath = os.path.join(proDir, "testreport")
        
    def set_case_suite(self):
        caseList = ReadJson.ReadJson('caselist',"CASELIST").get_case_list()
        print("本轮接口测试总计接口:"+str(len(caseList))+"个")
        print("本次接口测试涉及接口:"+str(caseList))
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in caseList:
            case_name = case.split("/")[-1]
            discover = unittest.defaultTestLoader.discover(self.executionPath, pattern=case_name + '.py', top_level_dir=None)
            suite_module.append(discover)

        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    def run(self):
        suit = self.set_case_suite()

        # if suit is not None:
        #     year = datetime.datetime.now().strftime('%Y')+'年'
        #     mon = datetime.datetime.now().strftime('%m')+'月'
        #     day = datetime.datetime.now().strftime('%d')+'日'
        #     hour = datetime.datetime.now().strftime('%H')+'时'
        #     min = datetime.datetime.now().strftime('%M')+'分'
        #     sec = datetime.datetime.now().strftime('%S')+'秒'
        #     TextReport=os.path.join(self.reportPath, ('陪伴APP接口测试'+ '-'+year+mon+day+hour+min+sec+'.html'))
        #     with open(TextReport,'wb') as f:
        #         runner = HTMLTestReportCN.HTMLTestRunner(stream=f,title='测试报告',description='generated by HTMLTestRunner.',verbosity=2)
        #         runner.run(suit) 
            
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suit)

        # smtp = Smtp.Smtp()
        # smtp.add_accessory(TextReport)
        # smtp.send_email()

if __name__ =='__main__':
    obj = Runtest()
    obj.run()

