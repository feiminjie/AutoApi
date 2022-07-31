import base64
import configparser
import hashlib
import os
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, DES
import time
from random import choice, randint
from sqlalchemy import create_engine
import pandas as pd
from common.gener_basedata import BaseData

base_data = BaseData()

cf = configparser.ConfigParser()
filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/standard/config.ini")
mytime = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/standard/mytime.csv")

# 读取CSV文件数据
def read_csv_data():
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/standard/bb.csv"), 'r',
              encoding='utf-8') as file:
        corpcodes_l = file.readlines()
        corpcodes = []
        for i in corpcodes_l:
            corpcodes.append(i.strip("\n"))
    print(corpcodes)


# 操作数据库
def pandas_database(table_name, values=None, types="q", key_name=None, k2=None, v2=None,):
    """
    :param key_name:     需要处理的字段名
    :param table_name:   需要处理的表名
    :param values:       表示按照哪个条件处理
    :param types:        表示做什么操作 c:创建 q:查询 d:删除 u:改
    """
    conn = create_engine('xxxxxx')
    if types == "q":
        sql = "SELECT {0} FROM {1} where {0}='{2}';".format(key_name, table_name, values)
        pf = pd.read_sql(sql, conn)
        if pf.empty:
            return 0
        else:
            return 1
    elif types == "qv":
        sql = "SELECT {0} FROM {1};".format(key_name, table_name)
        pf = pd.read_sql(sql, conn)
        pf = pf[key_name].values
        pft = choice(pf)
        return pft
    elif types == "d":
        sql = "DELETE FROM {0} where create_time > '{1}' and {2}='{3}';".format(table_name, values, k2, v2)
        try:
            pf = pd.read_sql(sql, conn)
        except Exception as e:
            pass
    elif types == "ds":
        sql = "DELETE FROM {0} where modify_time > '{1}' and {2}='{3}';".format(table_name, values, k2, v2)
        try:
            pf = pd.read_sql(sql, conn)
        except Exception as e:
            pass


# 数据写入配置文件
def write_config(sess, key, value):
    cf.add_section(sess)
    cf.set(sess, key, value)
    cf.write(open(filename, 'r+'))


# 读取配置文件数据
def read_config(sess, key):
    cf.read(filename, encoding="utf-8")
    value = cf.get(sess, key)
    return value


# rsa加密
def encrypts(k, mat_str):
    rsa_public_key = '''-----BEGIN PUBLIC KEY-----
    {}
-----END PUBLIC KEY-----'''.format(mat_str)
    key = RSA.import_key(rsa_public_key)
    passwd = PKCS1_v1_5.new(key)
    text = base64.b64encode(passwd.encrypt(bytes(k, encoding='utf-8')))
    return text.decode()


# md5加密
def md5_hash(token, key, code):
    # 时间戳
    dates = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    str = token + key + code + dates
    str_md5 = hashlib.md5(str.encode(encoding='utf-8')).hexdigest()
    return str_md5

# DES 加密 可以调整block_size
class Des:
    def __init__(self, block_size=8):
        """
        :param block_size: 填充的块大小，默认为16，有些是8
        """
        self.__block_size = block_size
        self.__modes = {
            'CBC': DES.MODE_CBC,
            'ECB': DES.MODE_ECB
        }
        self.__padding_s = {
            'pkcs7': self.__pkcs7padding,
            'pkcs5': self.__pkcs5padding,
            'zero': self.__zeropadding,
        }

    def __pkcs7padding(self, plaintext):
        """
        明文使用PKCS7填充
        :param plaintext: 明文
        """
        block_size = self.__block_size

        text_length = len(plaintext)
        bytes_length = len(plaintext.encode('utf-8'))
        len_plaintext = text_length if (bytes_length == text_length) else bytes_length
        return plaintext + chr(block_size - len_plaintext % block_size) * (block_size - len_plaintext % block_size)

    def __pkcs5padding(self, plaintext):
        """
        PKCS5Padding 的填充
        :param plaintext: 明文
        """
        block_size = self.__block_size

        text_length = len(plaintext)
        bytes_length = len(plaintext.encode('utf-8'))
        len_plaintext = text_length if (bytes_length == text_length) else bytes_length
        return plaintext + chr(block_size - len_plaintext % block_size) * (block_size - len_plaintext % block_size)

    def __zeropadding(self, plaintext):
        """
        zeropadding 的填充
        :param plaintext: 明文
        """
        block_size = self.__block_size

        text_length = len(plaintext)
        bytes_length = len(plaintext.encode('utf-8'))
        len_plaintext = text_length if (bytes_length == text_length) else bytes_length
        return plaintext + chr(0) * (block_size - len_plaintext % block_size)

    @staticmethod
    def __unpad(plaintext):
        pad_ = ord(plaintext[-1])
        return plaintext[:-pad_]

    def des_encrypt(self, padding: str, plaintext: str, key: str, mode: str, iv=None, *args):
        """
        :param padding: 填充方式,
        :param plaintext: 明文
        :param key:
        :param mode:
        :param iv:
        :param args: 跟DES.new 的参数一样
        :return:
        """
        key = key.encode('utf-8')
        iv = iv.encode('utf-8')
        if mode == 'ECB':
            des = DES.new(key, self.__modes[mode], *args)
        else:
            des = DES.new(key, self.__modes[mode], iv, *args)
        content_padding = self.__padding_s[padding](plaintext)  # 处理明文, 填充方式
        encrypt_bytes = des.encrypt(content_padding.encode('utf-8'))  # 加密
        return str(base64.b64encode(encrypt_bytes), encoding='utf-8')  # 重新编码

    def des_decrypt(self, padding: str, ciphertext: str, key: str, mode: str, iv=None, *args):
        key = key.encode('utf-8')
        iv = iv.encode('utf-8')
        if mode == 'ECB':
            des = DES.new(key, self.__modes[mode], *args)
        else:
            des = DES.new(key, self.__modes[mode], iv, *args)
        ciphertext = base64.b64decode(ciphertext)
        plaintext = des.decrypt(ciphertext).decode('utf-8')
        if padding == 'zero':
            return plaintext
        return self.__unpad(plaintext)

def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


def pkcs7padding(text):
    """
    明文使用PKCS7填充
    """
    bs = 16
    length = len(text)
    bytes_length = len(text.encode('utf-8'))
    padding_size = length if (bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    padding_text = chr(padding) * padding
    coding = chr(padding)
    return text + padding_text


# aes加密
def aes_hash(data, project_key, token):
    ivstr = project_key + token[:8]
    key = iv = bytes(ivstr, encoding="utf-8")
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    text = pkcs7padding(data).encode("utf-8")
    cipher_text = cryptos.encrypt(text)
    cipher_text_base = base64.b64encode(cipher_text).decode('utf8')
    return cipher_text_base


# 将值为列表的拆分成正确的值
def fath_sub(datas):
    del datas['asserts']
    del datas['step']
    del datas["reas"]
    sub_keys_dict = {}
    sub_keys_dict_all = {}
    fa_sub_key = []
    sub_keys_dict2 = {}
    da2 = {}
    keys = "entryAttachmentsattachments"  # in 不区分大小写
    for test_data_key in datas.keys():
        '''如果_在字典key中，就拆开，再组合成一个新的列表'''
        if "|" in test_data_key:
            sub_keys = test_data_key.split("_")
            fa_sub_key.append(test_data_key)
            if sub_keys[0] in keys:
                if sub_keys[1] == "data" and datas[test_data_key] == "小于50":
                    sub_keys_dict[sub_keys[1]] = base_data.base64_image(size=50)
                    sub_keys_dict_all[sub_keys[0]] = sub_keys_dict
                else:
                    sub_keys_dict[sub_keys[1]] = datas[test_data_key]
                    sub_keys_dict_all[sub_keys[0]] = sub_keys_dict
            else:
                sub_keys_dict2[sub_keys[1]] = datas[test_data_key]
                sub_keys_dict_all[sub_keys[0]] = sub_keys_dict2
    for s_key in fa_sub_key:
        del datas[s_key]
    for key in sub_keys_dict_all.keys():
        print(sub_keys_dict_all)
        da2[key] = [sub_keys_dict_all[key]]
    # 处理唯一值
    for key in datas.keys():
        # 办卡照片 头像
        if key in ["id"]:
            if datas[key] == "唯一":
                da2[key] = base_data.unsize_number(length=9, types="ne")
        elif key in ["realname"]:
            if datas[key] == "唯一":
                da2[key] = base_data.unsize_word(length=20, types="ne")
        elif key in ["phone"]:
            if datas[key] == "唯一":
                da2[key] = base_data.unsize_number(length=11, types="ne")
        else:
            da2[key] = datas[key]
    return da2


# 生成报告数据
def report_data(res, error_Log, run_time, test_datas, test_datas_copy, status_cod, response_cookies, url, method):
    report_dict = {'testcase': url}
    report_dict['result'] = res
    report_dict['message'] = error_Log
    report_dict['run_time'] = run_time
    report_dict['url'] = url
    report_dict['prams'] = test_datas
    report_dict['test_case'] = test_datas_copy
    report_dict['method'] = method
    report_dict['status_code'] = status_cod
    report_dict['cookies'] = response_cookies
    return report_dict
