# @Time    : 2023/8/13 19:54
# @Author  : Lan
# @File    : utils.py
# @Software: PyCharm
import datetime
import hashlib
import os
import random
import re
import string
import time
from core.settings import settings


async def get_random_num():
    """
    获取随机数
    :return:
    """
    return random.randint(10000, 99999)


r_s = string.ascii_uppercase + string.digits


async def get_random_string():
    """
    获取随机字符串
    :return:
    """
    return "".join(random.choice(r_s) for _ in range(5))


async def get_now():
    """
    获取当前时间
    :return:
    """
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))


async def get_select_token(code: str):
    """
    获取下载token
    :param code:
    :return:
    """
    token = settings.admin_token
    return hashlib.sha256(
        f"{code}{int(time.time() / 1000)}000{token}".encode()
    ).hexdigest()


async def get_file_url(code: str):
    """
    对于需要通过服务器中转下载的服务，获取文件下载地址
    :param code:
    :return:
    """
    return f"/share/download?key={await get_select_token(code)}&code={code}"


async def max_save_times_desc(max_save_seconds: int):
    """
    获取最大保存时间的描述
    :param max_save_seconds:
    :return:
    """

    def gen_desc_zh(value: int, desc: str):
        if value > 0:
            return f"{value}{desc}"
        else:
            return ""

    def gen_desc_en(value: int, desc: str):
        if value > 0:
            ret = f"{value} {desc}"
            if value > 1:
                ret += "s"
            ret += " "
            return ret
        else:
            return ""

    max_timedelta = datetime.timedelta(seconds=max_save_seconds)
    desc_zh, desc_en = "最长保存时间：", "Max save time: "
    desc_zh += gen_desc_zh(max_timedelta.days, "天")
    desc_en += gen_desc_en(max_timedelta.days, "day")
    desc_zh += gen_desc_zh(max_timedelta.seconds // 3600, "小时")
    desc_en += gen_desc_en(max_timedelta.seconds // 3600, "hour")
    desc_zh += gen_desc_zh(max_timedelta.seconds % 3600 // 60, "分钟")
    desc_en += gen_desc_en(max_timedelta.seconds % 3600 // 60, "minute")
    desc_zh += gen_desc_zh(max_timedelta.seconds % 60, "秒")
    desc_en += gen_desc_en(max_timedelta.seconds % 60, "second")
    return desc_zh, desc_en


async def sanitize_filename(filename: str) -> str:
    """
    安全处理文件名：
    1. 剥离路径只保留文件名
    2. 替换非法字符
    3. 处理空文件名情况
    """
    filename = os.path.basename(filename)
    illegal_chars = r'[\\/*?:"<>|\x00-\x1F]'  # 包含控制字符
    # 替换非法字符为下划线
    cleaned = re.sub(illegal_chars, '_', filename)
    # 处理空格（可选替换为_）
    cleaned = cleaned.replace(' ', '_')
    # 处理连续下划线
    cleaned = re.sub(r'_+', '_', cleaned)
    # 处理首尾特殊字符
    cleaned = cleaned.strip('._')
    # 处理空文件名情况
    if not cleaned:
        cleaned = 'unnamed_file'
    # 长度限制（按需调整）
    return cleaned[:255]
