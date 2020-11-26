import json
import datetime

class DisposeSpecial:
    def DictToList(self,expectedreport):
        expectedreport1 = {}
        expecteddata1 = []
        expectedreport1['status_code'] = expectedreport['status_code']
        for i in expectedreport['expecteddata']:
            expecteddata1 = expecteddata1+list(i.values())
        expectedreport1['expecteddata'] = expecteddata1
        return expectedreport1

    #接口DoctorArea特殊处理
    def DoctorAreaSpecial(self,expectedreport):
        expectedreport1 = self.DictToList(expectedreport)
        return expectedreport1

    #接口FullDate特殊处理
    def FullDateSpecial(self,expectedreport):
        expectedreport1 = self.DictToList(expectedreport)
        #时间范围12点
        d_time =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'12:00', '%Y-%m-%d%H:%M')
        # 当前时间
        n_time = datetime.datetime.now()
        # 判断当前时间是否在范围时间内
        if n_time > d_time:
            expectedreport1['expecteddata'].append(str(datetime.datetime.now().date())+' 上午')
        return expectedreport1

    #接口MeDynamic特殊处理
    def MeDynamicSpecial(self,expectedreport):
        for data in expectedreport['expecteddata']:
            for i in range(len(data['images'])):
                data['images'][i] = 'http://i.peiban85.com/'+data['images'][i]
            if len(data['cover']) !=0:
                data['cover'] = 'http://i.peiban85.com/'+data['cover']
            if len(data['voice']) != 0:
                data['voice'] = 'http://i.peiban85.com/'+data['voice'] 
            if  len(data['publisher']['avatar']) !=0:
                data['publisher']['avatar'] ='http://i.peiban85.com/'+data['publisher']['avatar']
            data['isCanDelete'] = True
            data['isPraised'] = False
            if len(data['images']) != 0:
                data['share']['shareImage'] = data['images'][0]
            if data['type'] == 2:
                data['content'] = ''
                data['share']['shareTitle'] = data['title']
                data['share']['shareDesc'] = data['description']
                data['share']['shareImage'] = data['cover']
                
        return expectedreport

    #接口Follow特殊处理
    def FollowSpecial(self,expectedreport):
        if  "expecteddata" in expectedreport:
            expectedreport['expecteddata']['followId'] = expectedreport['expecteddata'].pop('userid')
        return expectedreport
    
    #接口ChinaDoctorAgentMy特殊处理
    def ChinaDoctorAgentMySpecial(self,expectedreport):
        if  "expecteddata" in expectedreport:
            expectedreport['expecteddata']['sales'] = float(expectedreport['expecteddata']['sales'])
        return expectedreport

    #接口SquareSearch特殊处理
    def SquareSearch(self,expectedreport):
        for data in expectedreport['expecteddata']:
            for i in range(len(data['images'])):
                data['images'][i] = 'http://i.peiban85.com/'+data['images'][i]
            if len(data['cover']) !=0:
                data['cover'] = 'http://i.peiban85.com/'+data['cover']
            if len(data['voice']) != 0:
                data['voice'] = 'http://i.peiban85.com/'+data['voice'] 
            if  len(data['publisher']['avatar']) !=0:
                data['publisher']['avatar'] ='http://i.peiban85.com/'+data['publisher']['avatar']
            data['isCanDelete'] = False
            data['isPraised'] = False
            data['isContainVideo'] = False
            data['videoUrl'] =''
            if len(data['images']) != 0:
                data['share']['shareImage'] = data['images'][0]
            if data['type'] == '2':
                data['content'] = ''
                data['share']['shareTitle'] = data['title']
                data['share']['shareDesc'] = data['description']
                data['share']['shareImage'] = data['cover']
        return expectedreport

    #接口Article特殊处理
    def ArticleSpecial(self,expectedreport):
        return expectedreport


    def MyLinesSpecial(self,expectedreport):
        for data in expectedreport['expecteddata']:
            data['createTime'] = str(data['createTime']).replace('-','/')
            if data['businessType'] ==1:
                data['type'] = "咨讯服务费"
            elif data['businessType'] ==2:
                data['type'] = "转结可提现"
            elif data['businessType'] ==100:
                data['type'] = "咨询费"                
            elif data['businessType'] ==101:
                data['type'] = "推广佣金"
            elif data['businessType'] ==102:
                data['type'] = "产品销售"
            elif data['businessType'] ==103:
                data['type'] = "云仓收益"
            elif data['businessType'] ==994:
                data['type'] = "后台充值"
            elif data['businessType'] ==995:
                data['type'] = "提现失败"                
            elif data['businessType'] ==996:
                data['type'] = "原路返还"
            elif data['businessType'] ==997:
                data['type'] = "退款" 
            elif data['businessType'] ==998:
                data['type'] = "提现"
            elif data['businessType'] ==999:
                data['type'] = "订单消费"                   
        return expectedreport

    def UserInvitationSpecial(self,expectedreport):
        print(expectedreport)
        return expectedreport

    
        
        