from random import choice
from common.gener_basedata import BaseData
from common.handle_data import read_config


class SetParams(object):
    def __init__(self):
        self.base_data = BaseData()

    # 设置id
    def set_id(self, ty="M"):
        """
        ty: 表示是否必填
        """
        ids = ""
        if ty == "M":
            ids= [
                # 格式为错误数据列表
                [0],
                # 格式为正确数据列表
                ["唯一"]
            ]
        elif ty == "get":
            ids = [
                [""],
                [128272524]
            ]
        return ids


    # 设置真实姓名
    def real_name(self, ty="M"):
        """
        ty: 表示是否必填
        """
        if ty == "M":
            rena= [
                # 格式为错误数据列表
                ["", "费敏杰"],
                # 格式为正确数据列表
                ["唯一"]
            ]
        return rena

    # 手机号码
    def phone(self, ty="M"):
        if ty == "M":
            phon= [
                # 格式为错误数据列表
                ["", "13537847218"],
                # 格式为正确数据列表
                ["唯一"]
            ]
        return phon

    # 昵称
    def nick_name(self, ty="M"):
        nina = ""
        if ty == "O":
            nina= [
                # 格式为正确数据列表
                [self.base_data.unsize_word(length=20, types="ne")]
            ]
        return nina

    # 密码
    def password(self, ty="M"):
        if ty == "M":
            paw= [
                [""],
                # 格式为正确数据列表
                ["Aa123456"]
            ]
        return paw

    # 是否删除
    def is_delete(self):
        return [[0]]

    # 是否订阅
    def is_sub(self):
        return [[0]]




if __name__ == "__main__":
    pa = SetParams()
