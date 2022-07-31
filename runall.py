import os
from datetime import datetime
import jinja2
import sys
import time
#导入模板
import pandas as pd
from common.handle_data import pandas_database,read_config
from generate import AutoInter


# jinja2的调用方式
env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
temp = env.get_template('report/template_report.html')

# 测试报告地址
reportfile = os.path.join(os.path.dirname(__file__), 'report/result.html')
filepath = os.path.join(os.path.dirname(__file__), 'report/testReport.csv')

paths = os.path.abspath(os.path.join(os.getcwd(), "test_case"))

start = time.time()          # 开始时间

delete_time = datetime.now().strftime('%Y-%m-%d')

# 运行测试用例
# def runall():
#     inter = AutoInter()
#     inter.grab_inter(["/projectWorker/addProjectWorker", "/workerTeam/addTeam", "/projectInfo/addProjectInfo", "/projectInfo/addParticipatingUnits"])
#     time.sleep(2)
#     for root, dirs, files in os.walk(paths):
#         for f in files:
#             if os.path.splitext(f)[1] == '.py':
#                 os.chdir(root)
#                 os.system("python " + f)
# runall()

end = time.time()          # 结束时间

## 回收测试数据
# 删除项目
# pandas_database(types="d", table_name="project", values=delete_time, k2="contractor_corp_code", v2=read_config("project", "corp_code"))
# # 删除参建单位和参建项目关联表数据
# pandas_database(types="d", table_name="participating_units", values=delete_time, k2="project_id", v2=read_config("project", "pro_id"))
# # 删除考勤
# pandas_database(types="ds", table_name="attendance_info", values=delete_time, k2="project_id", v2=read_config("project", "pro_id"))
# # 删除工人
# pandas_database(types="d", table_name="worker", values=delete_time, k2="project_id", v2=read_config("project", "pro_id"))
# # 删除班组
# pandas_database(types="d", table_name="team", values=delete_time, k2="project_id", v2=read_config("project", "pro_id"))


# 写入测试报告
report_data = pd.read_csv(filepath, header=None)  # 读取数据默认第一行为header
report_data = report_data.reset_index()
report_data.columns = ["index", "test_case", "result", "log", "run_time", "url", "prams", "prams2", "method", "status_code", 'cookies']
report_data = report_data.sort_values(by=['result'])
success_count = report_data.loc[(report_data["result"] == "success")]
if success_count.empty == True:
    success = 0
else:
    success = len(success_count)
fail_count = report_data.loc[(report_data["result"] == "fail")]
if fail_count.empty == True:
    fail = 0
else:
    fail = len(fail_count)

report_data = report_data.to_dict("records")

temp_out = temp.render(
    all_count=str(success) + '/' + str(fail) + '/0/0',
    now_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
    all_time=str(round(end-start, 3))+'s',
    python_version=sys.version,
    result_data=report_data
)

with open(reportfile, 'w', encoding='utf8') as file:
    file.writelines(temp_out)
    file.close()

with open(filepath, 'w', encoding='utf8') as file:
    file.writelines("")





