class FormatConversion:
    #字符串A.B转换成A[B]并返回值
    def FormatConversion(self,data,jsondata):
        relyeddata = data.split('.')
        for i in range(len(relyeddata)):
            if i == 0:
                data = jsondata[relyeddata[i]]
            else:
                data = data[relyeddata[i]]
        return  data

    #字符串A.B转换成A[B]并重新赋值的json返回
    def  FormatSet(self,reportdatavalue,todata,relyjson):
        parts = todata.split('.')
        par = relyjson
        key = parts.pop(0)
        if parts:
            while parts:
                par = par.setdefault(key,{})
                key = parts.pop(0)
                # par[key]  = reportdatavalue

        if key == 'Authorization':
            par[key] = 'Bearer '+ reportdatavalue
        else:
            par[key]  = reportdatavalue
