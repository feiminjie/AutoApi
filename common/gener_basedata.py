import base64
import os
import time
from datetime import datetime, timedelta
from random import randint, choice
import pandas as pd


class BaseData(object):
    def __init__(self):
        # 统一社会信用代码路径
        self.image_200kb = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/standard/image/167kb.jpg")
        self.image_1kb = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/standard/image/1kb.jpg")
        self.image_49kb = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/standard/image/49kb.jpg")
        self.image_100kb = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/standard/image/97kb.jpg")
        self.image_200kb = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/standard/image/167kb.jpg")
        self.image_300kb = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/standard/image/224kb.jpg")
        self.letters = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
        self.spe_letter = choice(["!", "@", "#", "$", "%", "^", "&", "*", "(", "]", "}", "/", "<", "?"])
        self.numbers = "987654321"

    # 生成基础汉字
    def gb2312_zh(self):
        self.zh_word = ""
        for i in range(3000):
            head = randint(0xb0, 0xf7)
            body = randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
            val = f'{head:x}{body:x}'
            name = bytes.fromhex(val).decode('gb2312')
            self.zh_word = self.zh_word + name

    # 生成不定长汉字
    def unsize_word(self, low=1, length=10, types="one"):
        """
        :param low:   最小长度
        :param length:  最大长度
        :one: 是否只生成单个字母，gt表示大于当前最大长度的字符串，lt表示小时当前最小长度的字母串,ne表示在最小和最大之间的字符串
        """
        self.gb2312_zh()
        words = ""
        if types == "one":
            return choice(self.zh_word)
        if types == "gt":
            for _ in range(length+1):
                words = words + choice(self.zh_word)
        if types == "lt":
            for _ in range(low-1):
                words = words + choice(self.zh_word)
        if types == "ne":
            for _ in range(randint(low, length)):
                words = words + choice(self.zh_word)
        return words

    # 生成不定长数字
    def unsize_number(self, low=1, length=10, types="one"):
        """
        :param low:   最小长度
        :param length:  最大长度
        :one: 是否只生成单个字母，gt表示大于当前最大长度的字符串，lt表示小时当前最小长度的字母串,ne表示在最小和最大之间的字符串
        """
        num = "1"
        if low == 0:
            return 0
        if types == "one":
            return int(choice(self.numbers))
        if types == "gt":
            for _ in range(length+1):
                num = num + choice(self.numbers)
        if types == "lt":
            for _ in range(low-1):
                num = num + choice(self.numbers)
        if types == "ne":
            for _ in range(low, length):
                num = num + choice(self.numbers)
        return int(num)

    # 生成不定长英文
    def unsize_letter(self, low=1, length=10, types="one"):
        """
        :param low:   最小长度
        :param length:  最大长度
        :one: 是否只生成单个字母，gt表示大于当前最大长度的字符串，lt表示小时当前最小长度的字母串,ne表示在最小和最大之间的字符串
        """
        lett = ""
        if types == "one":
            return choice(self.letters)
        if types == "gt":
            for _ in range(length+1):
                lett = lett + choice(self.letters)
        if types == "lt":
            for _ in range(low-1):
                lett = lett + choice(self.letters)
        if types == "ne":
            for _ in range(low, length):
                lett = lett + choice(self.letters)
        return lett

    # 生成汉字数字组合
    def zh_num_combain(self, low, length):
        """
        :param low:   最小长度
        :param length:  最大长度
        """
        self.gb2312_zh()
        co = choice(self.zh_word) + choice(self.numbers)
        for i in range(randint(int(low)-2, int(length)-2)):
            co = co + choice(self.zh_word + self.numbers)
        return co

    # 生成数字字母组合
    def number_letter(self, low, length):
        """
        :param low:   最小长度
        :param length:  最大长度
        """
        nl = choice(self.letters) + choice(self.numbers)
        for i in range(randint(int(low)-2, int(length)-2)):
            nl = nl + choice(self.letters + self.numbers)
        return nl

    # 生成字母汉字组合
    def letter_zh(self, low, length):
        """
        :param low:   最小长度
        :param length:  最大长度
        """
        self.gb2312_zh()
        lz = choice(self.zh_word) + choice(self.letters)
        for i in range(randint(int(low)-2, int(length)-2)):
            lz = lz + choice(self.zh_word + self.letters)
        return lz

    # 生成汉字字母数字组合
    def letter_zh_number(self, low, length):
        """
        :param low:   最小长度
        :param length:  最大长度
        """
        self.gb2312_zh()
        lzn = choice(self.letters) + choice(self.numbers) + choice(self.zh_word)
        for i in range(randint(int(low)-3, int(length)-3)):
            lz = lzn + choice(self.letters + self.numbers + self.zh_word)
        return lzn

    # 生成汉字字母数字特殊字符组合
    def letter_zh_number_spe(self, low, length):
        """
        :param low:   最小长度
        :param length:  最大长度
        """
        self.gb2312_zh()
        lzn = choice(self.letters) + choice(self.numbers) + choice(self.zh_word) +choice(self.spe_letter)
        for i in range(randint(int(low)-4, int(length)-4)):
            lzn = lzn + choice(self.letters)
        return lzn

    # 生成正确的身份证号
    def gener_idnumber(self):
        # 列表里面的都是一些地区的前六位号码
        area = pd.read_csv("../data/standard/sys_area.csv")
        first_list = []
        for cods in area["code"]:
            first_list.append(cods)
        first = choice(first_list)
        '''生成年份'''""
        now = time.strftime('%Y')
        # 1948为第一代身份证执行年份,now-18直接过滤掉小于18岁出生的年份
        second = randint(1948, int(now) - 18)
        # 生成月份
        three = randint(1, 12)
        if three < 10:
            three = '0' + str(three)
        '''生成日期'''
        four = randint(1, 31)
        # 日期小于10以下，前面加上0填充
        if four < 10:
            four = '0' + str(four)
        '''生成身份证15-17位'''
        # 生成0-999（不包含括号右边1000）内随机一个数字，zfill固定位数为3位，不足3位的前面加上0填充
        five = str(randint(0, 1000)).zfill(3)
        # 前面17位合起来
        a = str(first) + str(second) + str(three) + str(four) + str(five)
        # 算第十八位
        b = (int(a[0]) * 7 + int(a[1]) * 9 + int(a[2]) * 10 + int(a[3]) * 5 + int(a[4]) * 8 + int(a[5]) * 4 + int(
            a[6]) * 2 + int(a[7]) + int(a[8]) * 6 + int(a[9]) * 3 + int(a[10]) * 7 + int(a[11]) * 9 + int(
            a[12]) * 10 + int(a[13]) * 5 + int(a[14]) * 8 + int(a[15]) * 4 + int(a[16]) * 2) % 11
        last = ""
        if b == 0:
            last = 1
        elif b == 1:
            last = 0
        elif b == 2:
            last = "X"
        elif b == 3:
            last = 9
        elif b == 4:
            last = 8
        elif b == 5:
            last = 7
        elif b == 6:
            last = 6
        elif b == 7:
            last = 5
        elif b == 8:
            last = 4
        elif b == 9:
            last = 3
        elif b == 10:
            last = 2
        return str(a) + str(last)

    # 生成时间
    def create_time(self, tim="d", types="d", day=1):
        """
        :param tim:  表示需要获取当前的时间还是过去的时间，now为当前，last表示过去，future 表示未来
        :param types: 表示格式类型，d到天，s到秒
        :param day: 表示要离当前时间距离多少天的时间
        :return:
        """
        date_time = ""
        if types == "d":
            if tim == "d":
                date_time = datetime.now().strftime('%Y-%m-%d')
            if tim == "l":
                my_time = datetime.now() + timedelta(days=-day)
                date_time = my_time.strftime('%Y-%m-%d')
            if tim == "f":
                my_time = datetime.now() + timedelta(days=day)
                date_time = my_time.strftime('%Y-%m-%d')
        if types == "s":
            if tim == "d":
                date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if tim == "l":
                my_time = datetime.now() + timedelta(days=-40)
                date_time = my_time.strftime('%Y-%m-%d %H:%M:%S')
            if tim == "f":
                my_time = datetime.now() + timedelta(days=50)
                date_time = my_time.strftime('%Y-%m-%d %H:%M:%S')
        if types == "m":
            if tim == "d":
                date_time = datetime.now().strftime('%Y-%m')
            elif tim == "l":
                my_time = datetime.now() + timedelta(days=-40)
                date_time = my_time.strftime('%Y-%m')
            elif tim == "f":
                my_time = datetime.now() + timedelta(days=50)
                date_time = my_time.strftime('%Y-%m')
        return str(date_time)

    # 图片编码
    def base64_image(self, size=5):
        if size == 5:
            with open(self.image_1kb, "rb") as f:  # 转为二进制格式
                base64_data = base64.b64encode(f.read())  # 使用base64进行加密
                s = base64_data.decode()
                image_str = "data:image/jpg;base64,%s"%s
        if size == 50:
            with open(self.image_49kb, "rb") as f:  # 转为二进制格式
                base64_data = base64.b64encode(f.read())  # 使用base64进行加密
                s = base64_data.decode()
                image_str = "data:image/jpg;base64,%s"%s
        if size == 100:
            with open(self.image_100kb, "rb") as f:  # 转为二进制格式
                base64_data = base64.b64encode(f.read())  # 使用base64进行加密
                s = base64_data.decode()
                image_str = "data:image/jpg;base64,%s"%s
        if size == 200:
            with open(self.image_200kb, "rb") as f:  # 转为二进制格式
                base64_data = base64.b64encode(f.read())  # 使用base64进行加密
                s = base64_data.decode()
                image_str = "data:image/jpg;base64,%s"%s
        if size == 300:
            with open(self.image_300kb, "rb") as f:  # 转为二进制格式
                base64_data = base64.b64encode(f.read())  # 使用base64进行加密
                s = base64_data.decode()
                image_str = "data:image/jpg;base64,%s"%s
        return image_str

    # 金额
    def amounts(self, bit=1, ze=0):
        amounts = 0
        if bit == 1 and ze == 0:
            amounts = self.unsize_number(types="one")
        if bit == 2 and ze == 0:
            amounts = self.unsize_number(types="one") * 10
        if bit == 3 and ze == 0:
            amounts = self.unsize_number(types="one") * 100
        if bit == 4 and ze == 0:
            amounts = self.unsize_number(types="one") * 100
        if bit == 9 and ze == 2:
            amounts = str(self.unsize_number(types="one") * 100000000) + ".01"
        if bit == 1 and ze == 1:
            amounts = str(self.unsize_number(types="one")) + ".1"
        if bit == 2 and ze == 1:
            amounts = str(self.unsize_number(types="one")) * 10 + ".1"
        if bit == 2 and ze == 2:
            amounts = str(self.unsize_number(types="one")) * 10 + ".01"
        if bit == 2 and ze == 3:
            amounts = str(self.unsize_number(types="one")) * 10 + ".001"
        if bit == 2 and ze == 4:
            amounts = str(self.unsize_number(types="one")) * 10 + ".0001"
        if bit == 2 and ze == 5:
            amounts = str(self.unsize_number(types="one")) * 10 + ".00001"
        return float(amounts)


    def get_mobile(self):
        mobiles = ['130', '131', '132', '133', '134']
        number  = str(int(time.time()))[2:]
        mobile  = choice(mobiles)+number
        return mobile

if __name__ == "__main__":
    data = BaseData()
    data.get_mobile()
