import random
from random import choice
from common.set_params import SetParams
import pandas as pd
import requests
import json
from common.handle_data import read_config
from common.template_case import template_case_post, template_case_get
from common.create_test_data import gener_param_post, gener_param_get
from common.gener_basedata import BaseData


class AutoInter(object):
    def __init__(self):
        self.params = SetParams()
        self.base_data = BaseData()

    # 请求接口文档地址
    def grab_inter(self, opt):
        """
        :param opt:  all表示整个文档的接口都生成，否则就是单个接口
        """
        rep = requests.get(read_config("host", "openapi_doc"))
        interface_info = rep.content.decode("utf-8")
        interface_info_dict = json.loads(interface_info)
        path_list = interface_info_dict["paths"].keys()
        if opt == "all":
            for path in path_list:
                self.write_case(interface_info_dict, path)
        else:
            for path in opt:
                self.write_case(interface_info_dict, path)

    # 根据模板写测试用例
    def write_case(self, interface_info_dict, path):
        test_case_file_path = "test_case/test_case{}.py".format(path.replace("/", "_"))
        # 生成测试用例路径
        methods = interface_info_dict["paths"][path].keys()
        path_last = path.split("/")
        # 得到该接口的请求方式
        for method in methods:
            if method == "post":
                originalRefs = interface_info_dict["paths"][path][method]["requestBody"]["content"]["application/json"]["schema"]["$ref"]
                originalRef = originalRefs.split("/")[-1]
                # 调用获取参数的函数，得到具体的参数字典
                params_post = self.grap_parameters(interface_info_dict, originalRef)
                # 根据参数路径创建测试数据文件路径
                file_path_post = "data/test_data/" + originalRef + path_last[-1] + ".csv"
                # 调用数据生成函数生成测试数据
                test_data_dict = gener_param_post(params_post, self.params, path_last)
                # 写入测试数据文件
                self.write_test_case_csv(test_data_dict, file_path_post)
                # 调用模板生成测试用例
                template_case_post(test_case_file_path, file_path_post, path)
            elif method == "get":
                originalRefs = interface_info_dict["paths"][path][method]
                # 根据参数路径创建测试数据文件路径
                file_path_get = "data/test_data/" + path + ".csv"
                if "parameters" in originalRefs.keys():
                    # 调用获取参数的函数，得到具体的参数字典
                    params_post = self.grap_parameters_get(originalRefs)
                    # 调用数据生成函数生成测试数据
                    test_data_dict = gener_param_get(params_post, self.params, path_last)
                    # 写入测试数据文件
                    self.write_test_case_csv(test_data_dict, file_path_get)
                    # 调用模板生成测试用例
                    template_case_get(test_case_file_path, file_path_get, path)
                else:
                    # 调用模板生成测试用例
                    template_case_get(test_case_file_path, file_path_get, path)

    # 找出所有的参数
    def grap_parameters(self, interface_info_dict, originalRef):
        paramsp = {}
        parameters_list = interface_info_dict["components"]["schemas"][originalRef]["properties"]
        # 循环参数key值列表
        for parameters in parameters_list.keys():
            # 参数中包含items表示有子参数
            if "items" in parameters_list[parameters].keys():
                # 获取子参数的definitions
                subparamter = parameters_list[parameters]["items"]["originalRef"]
                # 得到子参数
                subparameters_list = interface_info_dict["definitions"][subparamter]["properties"]
                for subp in subparameters_list.keys():
                    # 循环子参数，将参数与子参数拼接
                    paramsp[parameters + "|" + subp] = subparameters_list[subp]["type"]
            else:
                description = parameters_list[parameters]["type"]
                paramsp[parameters] = description
        # 返回该接口参数字典
        return paramsp

    # 找到get方式的所有参数
    def grap_parameters_get(self, oRefs):
        paramsp = {}
        parameters_list = oRefs["parameters"]
        for parame in parameters_list:
            if parame["in"] == "path":
                paramsp[parame["name"]] = paramsp[parame["in"]]
        return paramsp

    # 写测试数据模板
    def write_test_case_csv(self, test_data, filpath):
        test_case = []
        case_param_list = test_data.keys()
        for case_param in case_param_list:
            # 循环第一个参数，取第一参数的值，其他参数的都取正确值
            test_data_copy = test_data.copy()
            if len(test_data[case_param]) == 2:
                # 取出错误的参数的值作为一个单独的列表
                test_data_copy_error = test_data[case_param][0]
                # 取出正确的参数作为一个单独的列表
                test_data_copy_yes = test_data[case_param][1]
                # 删除复制的数据中的这个参数
                del test_data_copy[case_param]
                # 循环错误数据
                for pas in test_data_copy_error:
                    test_data_dict = {"step":random.randint(1,20000)}
                    # 选出一个错误数据加入到字典中
                    test_data_dict[case_param] = pas
                    for copy_pa in test_data_copy.keys():
                        test_data_dict[copy_pa] = choice(test_data_copy[copy_pa][-1])
                    # 预期该条用力成功还是失败，当有一个错误数据时，用例预期就是fail
                    test_data_dict["asserts"] = "fail"
                    test_data_dict["reas"] = str(case_param) + "|" + str(pas) + "|错误"
                    test_case.append(test_data_dict)
                # 循环正确数据
                for pas in test_data_copy_yes:
                    test_data_dict_yes = {"step": random.randint(20000, 200000)}
                    test_data_dict_yes[case_param] = pas
                    for copy_pa in test_data_copy.keys():
                        # 全都是正确数据
                            test_data_dict_yes[copy_pa] = choice(test_data_copy[copy_pa][-1])
                    test_data_dict_yes["asserts"] = "success"
                    test_data_dict_yes["reas"] = str(case_param) + "|" + str(pas) + "|正确"
                    test_case.append(test_data_dict_yes)
        pf = pd.DataFrame(test_case)
        pf.to_csv(filpath, index=False)


if __name__ == "__main__":
    inter = AutoInter()
    inter.grab_inter(["/api/v1/shuini"])
