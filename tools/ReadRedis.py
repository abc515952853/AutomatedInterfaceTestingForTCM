import redis
from tools import ReadConfig
import os

class ReadRedis:
    def __init__(self):
        configdata = ReadConfig.ReadConfig()
        self.host =  configdata.get_data('REDIS','redis_host')
        self.port =  configdata.get_data('REDIS','redis_port')

    #打开redis
    def read_redis(self):
        try:
            pool = redis.ConnectionPool(host=self.host, port=self.port , decode_responses=True,db = 0)
            self.r = redis.Redis(connection_pool=pool)
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)

    #查询hash数据
    def hashgetall(self,name):
        self.read_redis()
        try:
            self.r.hgetall(name)
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)
    
    #删除hash数据
    def hashdelall(self,name,key):
        self.read_redis()
        try:
            self.r.hdel(name,key)
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)

    #添加hash数据
    def hashsetall(self,name,key,value):
        self.read_redis()
        try:
            self.r.hset(name,key,str(value).replace("'",'"').replace("False","false").replace("True","true"))
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)
    
    #判断 member 元素是否是集合 key 的成员
    def setsismember(self,name,key):
        self.read_redis()
        try:
            result = self.r.sismember(name,key)
            return result
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)


