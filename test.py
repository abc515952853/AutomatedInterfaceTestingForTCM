import requests
import json


url = "https://appgateway.qianjifang.com.cn/api/v5.0/Square/search"
data = {
    "type":1
}
res = requests.get(url=url,params=data)
print(res.status_code,res.text)