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
               "\t\terror_Log = ''\n" \
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
               "\t\tstatus_cod = '??????????????????????????????????????????'\n" \
               "\t\tresponse_cookies = '????????????????????????cookie'\n" \
               "\t\tresponse_result = '????????????'\n" \
               "\t\trun_time = 0\n" \
               "\t\tres = 'fail'\n" \
               "\t\turl = '????????????URL??????????????????'\n" \
               "\t\tmethod = '????????????????????????'\n" \
               "\t\terror_Log = str(e)\n\n" \
               "\treport_dict = report_data(res, error_Log, run_time, test_datas, test_data_copys, status_cod, response_cookies, url, method)\n" \
               "\treport_list.append(report_dict)\n" \
               "pt = pd.DataFrame(report_list)\n" \
               "filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'report/testReport.csv')\n" \
               "pt.to_csv(filepath, mode='a', index=False, header=False)".format(file_path_post,
                                                                              read_config("host", "host") + path,
                                                                              headers)
        file.write(cont)


def template_case_get(filename, file_path_post, path):
       with open(filename, 'w', encoding='utf8') as file:
              headers = {
                     'User-Agent': read_config("host", "UserAgent"),
                     'content-type': read_config("host", "content_type"),
                     'token': read_config("access_token", "token")
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
                     "report_list = []\n" \
                     "try:\n" \
                     "\tresponse = requests.get(url='{1}'," \
                     "\n\t\t\t\t\t\ttimeout=40, \n\t\t\t\t\t\t\theaders={2})\n" \
                     "\tret = response.content.decode('utf-8')\n" \
                     "\tret_dict = json.loads(ret)\n" \
                     "\trun_time = response.elapsed.total_seconds()\n" \
                     "\tstatus_cod = response.status_code\n" \
                     "\tresponse_cookies = response.cookies\n" \
                     "\turl = response.url\n" \
                     "\tmethod = response.request.method\n" \
                     "\tif len(ret_dict) == 4:\n" \
                     "\t\terror_Log = '??????????????????'\n" \
                     "\telse:\n" \
                     "\t\terror_Log = '??????????????????'\n" \
                     "except Exception as e:\n" \
                     "\tstatus_cod = '??????????????????????????????????????????'\n" \
                     "\tresponse_cookies = '????????????????????????cookie'\n" \
                     "\tresponse_result = '????????????'\n" \
                     "\trun_time = 0\n" \
                     "\tres = 'fail'\n" \
                     "\turl = '????????????URL??????????????????'\n" \
                     "\tmethod = '????????????????????????'\n" \
                     "\terror_Log = str(e)\n\n" \
                     "report_dict = report_data(error_Log=error_Log, run_time=run_time, status_cod=status_cod, response_cookies=response_cookies, url=url, method=method)\n" \
                     "report_list.append(report_dict)\n" \
                     "pt = pd.DataFrame(report_list)\n" \
                     "filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'report/testReport.csv')\n" \
                     "pt.to_csv(filepath, mode='a', index=False, header=False)".format(file_path_post,
                                                                                       read_config("host",
                                                                                                   "host") + path,
                                                                                       headers)
              file.write(cont)

def case_template_post_add():
    pass


def case_template_post_list():
    pass


