import pymysql
from tools import ReadConfig
import json
import datetime
import os

# from pymysql import converters

class ReadDB:
    def __init__(self):
        configdata = ReadConfig.ReadConfig()
        self.db_ip = configdata.get_data('DATABASE','db_ip')
        self.db_port = configdata.get_data('DATABASE','db_port')
        self.db_username = configdata.get_data('DATABASE','db_username')
        self.db_password = configdata.get_data('DATABASE','db_password')
        self.db_dbname = configdata.get_data('DATABASE','db_dbname')

        # self.converions = converters.conversions
        # self.converions[pymysql.FIELD_TYPE.BIT] = lambda x: False if '\x00' else True

    #打开数据库
    def read_db(self):
        try:
            self.conn = pymysql.connect(
                host = self.db_ip, 
                port = int(self.db_port),
                user = self.db_username,
                password = self.db_password,
                database = self.db_dbname,
                charset = "utf8",
                # conv=self.converions#pymysql在读取bit类型时显示x00的解决办法
            )
            self.cur = self.conn.cursor(cursor = pymysql.cursors.DictCursor)#数据和字段名称一起带回
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)
    
    #关闭数据库
    def close_db(self):
        try:
            if self.cur:
                self.cur.close()
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
        finally:
            try:
                if self.conn:
                    self.conn.close()
            except Exception as ex_results:
                print("程序终止,抓了一个异常：",ex_results,)

	#查询一条数据
    def search_one(self,sql):
        self.read_db()
        try:
            self.cur.execute(sql)
            result = self.cur.fetchone()  
            return result
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)
        finally:
            self.close_db()

	#查询所有数据
    def search_all(self,sql):
        self.read_db()
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            return result
        except Exception as ex_results:
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)
        finally:
            self.close_db()

	#增加/修改/删除一条数据
    def modify_data(self,sqlarr):
        self.read_db() 
        try:
            for sql in sqlarr:
                print('正在执行语句：'+ sql)
                self.cur.execute(sql) 
            self.conn.commit()
        except Exception as ex_results:
            self.conn.rollback()
            print("程序终止,抓了一个异常：",ex_results,)
            os._exit(0)
        finally:
            self.close_db()

# if __name__ == "__main__":
#     a = ReadDB()
#     sql = "delete from test where name ='wangdachuizi '"
#     a.modify_data(sql)
