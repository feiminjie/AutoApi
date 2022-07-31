from common.handle_data import read_config


def template_case_post(filename, file_path_post, path):
    with open(filename, 'w', encoding='utf8') as file:
        headers = {
            'User-Agent': read_config("host", "UserAgent"),
            'content-type': read_config("host", "content_type"),
        }
        cont = "# coding=utf-8\n" \
               "import json\n" \
               "import pandas as pd\n" \
               "import os\n" \
               "from common.set_params import SetParams \n" \
               "from common.handle_data import fath_sub, report_data\n" \
               "import base64\n" \
               "import requests\n\n\n" \
               "params_List = SetParams()\n\n" \
               "test_case_data = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '{0}'), keep_default_na=False)\n" \
               "test_case_data_dict = test_case_data.to_dict('records')\n\n" \
               "report_list = []\n" \
               "for test_data in test_case_data_dict:\n" \
               "\ttest_data_copys = test_data.copy()\n" \
               "\tasserts = test_data['asserts']\n" \
               "\ttest_datas = fath_sub(test_data)\n" \
               "\ttry:\n" \
               "\t\tresponse = requests.post(url='{1}',\n\t\t\t\t\t\t\tdata=json.dumps(test_datas), " \
               "\n\t\t\t\t\t\t\ttimeout=40, \n\t\t\t\t\t\t\theaders={2})\n" \
               "\t\tret = response.content.decode('utf-8')\n" \
               "\t\tret_dict = json.loads(ret)\n" \
               "\t\trun_time = response.elapsed.total_seconds()\n" \
               "\t\tstatus_cod = response.status_code\n" \
               "\t\tresponse_cookies = response.cookies\n" \
               "\t\turl = response.url\n" \
               "\t\tmethod = response.request.method\n" \
               "\t\tif 'detail' in ret_dict.keys():\n" \
               "\t\t\terror_Log = ret_dict['detail']\n" \
               "\t\t\tresult = 'fail'\n" \
               "\t\telse:\n" \
               "\t\t\tresult = ''\n" \
               "\t\t\tif ret_dict['result'] == 1:\n" \
               "\t\t\t\terror_Log = ret_dict['message']\n" \
               "\t\t\t\tresult = 'success'\n" \
               "\t\tif result == asserts:\n" \
               "\t\t\tres = 'success'\n" \
               "\t\telse:\n" \
               "\t\t\tres = 'fail'\n" \
               "\texcept Exception as e:\n" \
               "\t\tstatus_cod = '环境挂掉了或者是接口链接错了'\n" \
               "\t\tresponse_cookies = '都没请求通哪来的cookie'\n" \
               "\t\tresponse_result = '没请求通'\n" \
               "\t\trun_time = 0\n" \
               "\t\tres = 'fail'\n" \
               "\t\turl = '检查检查URL是不是写错了'\n" \
               "\t\tmethod = '检查一下请求方式'\n" \
               "\t\terror_Log = str(e)\n\n" \
               "\treport_dict = report_data(res, error_Log, run_time, test_datas, test_data_copys, status_cod, response_cookies, url, method)\n" \
               "\treport_list.append(report_dict)\n" \
               "pt = pd.DataFrame(report_list)\n" \
               "filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'report/testReport.csv')\n" \
               "pt.to_csv(filepath, mode='a', index=False, header=False)".format(file_path_post,
                                                                              read_config("host", "host") + path,
                                                                              headers)
        file.write(cont)


def case_template_post_add():
    pass


def case_template_post_list():
    pass


def case_template_get_list():
    pass
