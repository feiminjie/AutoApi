# coding=utf-8
import json
import pandas as pd
import os
from common.set_params import SetParams 
from common.handle_data import fath_sub, report_data
import base64
import requests


params_List = SetParams()

test_case_data = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/test_data/MyUserregist.csv'), keep_default_na=False)
test_case_data_dict = test_case_data.to_dict('records')

report_list = []
for test_data in test_case_data_dict:
	test_data_copys = test_data.copy()
	asserts = test_data['asserts']
	test_datas = fath_sub(test_data)
	try:
		response = requests.post(url='http://119.29.3.184:8001/api/v1/user/regist',
							data=json.dumps(test_datas), 
							timeout=40, 
							headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36', 'content-type': 'application/json'})
		ret = response.content.decode('utf-8')
		ret_dict = json.loads(ret)
		run_time = response.elapsed.total_seconds()
		status_cod = response.status_code
		response_cookies = response.cookies
		url = response.url
		method = response.request.method
		error_Log = ''
		if 'detail' in ret_dict.keys():
			error_Log = ret_dict['detail']
			result = 'fail'
		else:
			result = ''
			if ret_dict['result'] == 1:
				error_Log = ret_dict['message']
				result = 'success'
		if result == asserts:
			res = 'success'
		else:
			res = 'fail'
	except Exception as e:
		status_cod = '环境挂掉了或者是接口链接错了'
		response_cookies = '都没请求通哪来的cookie'
		response_result = '没请求通'
		run_time = 0
		res = 'fail'
		url = '检查检查URL是不是写错了'
		method = '检查一下请求方式'
		error_Log = str(e)

	report_dict = report_data(res, error_Log, run_time, test_datas, test_data_copys, status_cod, response_cookies, url, method)
	report_list.append(report_dict)
pt = pd.DataFrame(report_list)
filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'report/testReport.csv')
pt.to_csv(filepath, mode='a', index=False, header=False)