import requests
import json

class RunMethod:
	def post_main(self,url,data,header=None):
		res = None
		try:
			if header !=None:
				if header['Content-Type'] =='application/x-www-form-urlencoded':
					res = requests.post(url=url,data=data,headers=header)
				else:
					res = requests.post(url=url,data=json.dumps(data),headers=header)
			else:
				res = requests.post(url=url,data=json.dumps(data))
			return res
		except Exception as ex_results:
			print("程序终止,抓了一个异常：",ex_results,)

	def get_main(self,url,data=None,header=None):
		res = None
		try:
			if header !=None:
				if data != None:
					res = requests.get(url=url,params=data,headers=header)
				else:
					res = requests.get(url=url,headers=header)
			else:
				if data != None:
					res = requests.get(url=url,params=data)
				else:
					res = requests.get(url=url)
			return res
		except Exception as ex_results:
			print("程序终止,抓了一个异常：",ex_results,)
			
	def put_main(self,url,data,header=None):
		res = None
		try:
			if header !=None:
				if header['Content-Type'] =='application/x-www-form-urlencoded':
					res = requests.put(url=url,data=data,headers=header)
				else:
					res = requests.put(url=url,data=json.dumps(data),headers=header)
			else:
				res = requests.put(url=url,data=json.dumps(data))
			return res
		except Exception as ex_results:
			print("程序终止,抓了一个异常：",ex_results,)
	
	def delete_main(self,url,data,header=None):
		res = None
		try:
			if header !=None:
				if header['Content-Type'] =='application/x-www-form-urlencoded':
					res = requests.delete(url=url,data=data,headers=header)
				else:
					res = requests.delete(url=url,data=json.dumps(data),headers=header)
			else:
				res = requests.delete(url=url,data=json.dumps(data))
			return res
		except Exception as ex_results:
			print("程序终止,抓了一个异常：",ex_results,)

	def run_main(self,url,method,header=None,data=None):
		res = None
		if method == 'POST':	
			res = self.post_main(url,data,header)
		elif method == 'GET':
			res = self.get_main(url,data,header)
		elif method == 'PUT':
			res = self.put_main(url,data,header)
		else:
			res = self.delete_main(url,data,header)
		return res

    