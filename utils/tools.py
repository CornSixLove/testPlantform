# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 13:00
---------
@summary:
---------
@author: LiFree
"""
import base64
import calendar
import datetime
from datetime import datetime as dt
import functools
import hashlib
import inspect
import json
import os
import random
import re
import string
import time
import traceback
import uuid
from random import shuffle
from typing import Union, overload, AnyStr
from urllib import parse

from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

from log import logger
from .typeshed import BytesPath, StrOrBytesPath, StrPath, DateFormat

_regexs = {}


def aes_encrypt_ecb(key: bytes, plaintext: str, is_hex: bool = False) -> Union[bytes, str]:
    if isinstance(key, str):
        key = key.encode()
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    if is_hex:
        return bytes.hex(ciphertext)
    else:
        return base64.b64encode(ciphertext)


def aes_decrypt_ecb(key, ciphertext):
    if isinstance(key, str):
        key = key.encode()
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    encrypted_data = bytes.fromhex(ciphertext)
    decrypted_data = cipher.decrypt(encrypted_data)
    de_plaintext = unpad(decrypted_data, AES.block_size)

    return de_plaintext.decode('utf-8')


def b64encode(context, decode: bool = True) -> Union[str, bytes]:
    if isinstance(context, bytes):
        encoded_bytes = base64.b64encode(context)
    else:
        encoded_bytes = base64.b64encode(ensure_str(context).encode('utf-8'))

    return encoded_bytes.decode('utf-8') if decode else encoded_bytes


def b64decode(context: str, decode: bool = True) -> Union[str, bytes]:
    decoded_bytes = base64.b64decode(ensure_str(context))

    return decoded_bytes.decode('utf-8') if decode else decoded_bytes


def delay_time(sleep_time=60):
    """
    @summary: 睡眠  默认1分钟
    ---------
    @param sleep_time: 以秒为单位
    ---------
    @result:
    """

    time.sleep(sleep_time)


def dirname(p: AnyStr, level: int = 0) -> AnyStr:
    """ 默认返回当前文件的绝对路径 """
    abspath = os.path.abspath(p)

    if level <= 0:
        return abspath

    for _ in range(level):
        abspath = os.path.dirname(abspath)

    return abspath


def format_seconds(seconds):
    """
    @summary: 将秒转为时分秒
    ---------
    @param seconds:
    ---------
    @result: 2天3小时2分49秒
    """

    seconds = int(seconds + 0.5)  # 向上取整

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    times = ""
    if d:
        times += "{}天".format(d)
    if h:
        times += "{}小时".format(h)
    if m:
        times += "{}分".format(m)
    if s:
        times += "{}秒".format(s)

    return times


def ensure_str(text) -> str:
    if not text:
        return ""
    else:
        return str(text)


def ensure_int(text) -> int:
    if not text:
        return 0
    else:
        return int(text)


def ensure_float(text) -> float:
    if not text:
        return 0.0
    else:
        return float(text)


def generate_random_string(length):
    # 生成包含大小写字母和数字的可选字符集
    choices = string.ascii_letters + string.digits
    # 从可选字符集中随机选择 length 个字符，组成一个字符串并返回
    return ''.join(random.choice(choices) for _ in range(length))


def get_cache_expire(
        current_time: bool = False,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        microseconds: int = 0,
        milliseconds: int = 0,
        weeks: int = 0
) -> datetime.datetime:
    """
    current_time: True 表示现在的时间; False 凌晨零点的时间
    """
    current_date = datetime.datetime.now()
    timedelta = datetime.timedelta(
        days=days, hours=hours, minutes=minutes, seconds=seconds,
        microseconds=microseconds, milliseconds=milliseconds, weeks=weeks
    )

    if not current_time:
        # 创建凌晨零点的时间
        current_date = datetime.datetime.combine(current_date, datetime.datetime.min.time())

    current_date += timedelta

    return current_date


def get_cache_expire_at(now: bool = False) -> int:
    """
    now: is False 获取第二天凌晨零点的时间戳(秒级)
        is True 获取当天凌晨零点的时间戳(秒级)
    """
    current_date = datetime.datetime.now().date()
    if now:
        # 创建一个表示今天凌晨零点的 datetime 对象
        midnight = datetime.datetime.combine(current_date, datetime.datetime.min.time())

        # 将 datetime 对象转换为时间戳
        timestamp = midnight.timestamp()

    else:
        # 获取第二天日期
        next_day = current_date + datetime.timedelta(days=1)

        # 创建一个表示第二天凌晨零点的 datetime 对象
        midnight = datetime.datetime.combine(next_day, datetime.datetime.min.time())

        # 将 datetime 对象转换为时间戳
        timestamp = midnight.timestamp()
    return int(timestamp)


def get_cache_expire_time() -> int:
    """ 获取到凌晨零点的时间差 """
    now = datetime.datetime.now()

    # 计算距离第二天凌晨 12 点的时间差
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    expire_time = (midnight - now).seconds
    return expire_time


def get_cache_expire_at_week() -> int:
    """ 计算下一个周一的时间戳 """
    # 获取当前日期
    current_date = datetime.datetime.now()
    # 计算距离下一个周一的天数
    days_to_next_monday = (8 - current_date.isoweekday())
    # 计算下个周一的日期
    next_monday = current_date + datetime.timedelta(days=days_to_next_monday)
    # 设置为零点
    next_monday = next_monday.replace(hour=0, minute=0, second=0, microsecond=0)
    # 转换为时间戳
    timestamp = int(next_monday.timestamp())
    return timestamp


def get_md5(*args):
    """
    @summary: 获取唯一的32位md5
    ---------
    @param args: 参与联合去重的值
    ---------
    @result: 7c8684bcbdfcea6697650aa53d7b1405
    """

    m = hashlib.md5()
    for arg in args:
        m.update(str(arg).encode())

    return m.hexdigest()


def get_sha1(arg):
    """
    @summary: 获取唯一的32位md5
    ---------
    @result: 356a192b7913b04c54574d18c28d46e6395428ab
    """
    if isinstance(arg, str):
        arg = arg.encode('utf-8')

    return hashlib.sha1(arg).hexdigest()


def get_max_days(year: int, month: int) -> int:
    """ 获取指定年月的最大天数 """
    return calendar.monthrange(year, month)[1]


def get_month_range(date_str=None, is_str: bool = False) -> tuple:
    """ 获取指定日期的月份范围， 默认当月 """
    if date_str:
        now = date_str
        if isinstance(now, str) and len(now) == 7:
            now = datetime.datetime.strptime(now, '%Y-%m').date()
        elif not isinstance(now, datetime.date):
            now = datetime.datetime.strptime(now, '%Y-%m-%d').date()
    else:
        now = datetime.date.today()  # 获取当前日期时间

    first_day = now.replace(day=1)  # 本月第一天
    # 上个月的结束日期
    last_day = first_day.replace(day=calendar.monthrange(first_day.year, first_day.month)[1])
    if is_str:
        return str(first_day), str(last_day)
    else:
        return first_day, last_day


def get_now_timestamp(msec: bool = True):
    if msec:
        return int(time.time() * 1000)
    else:
        return int(time.time())


def get_uuid():
    return uuid.uuid4()


def random_HubCode():
    get_English = string.ascii_uppercase
    random_code = [random.choice(get_English) for random_code in range(4)]
    get_code = ''.join(random_code)
    two_digit_number = str(random.randint(10, 99)).zfill(2)
    get_code = get_code + two_digit_number
    return get_code

def isdir(s: Union[StrOrBytesPath, int]) -> bool:
    return os.path.isdir(s)


def isfile(s: Union[StrOrBytesPath, int]) -> bool:
    return os.path.isfile(s)


def is_base64(s: str):
    try:
        b64decode(s)
    except Exception as e:
        logger.warning(e)
        return False
    else:
        return True


@overload
def join_path(__path: StrPath, *paths: StrPath) -> str: ...


def join_path(__path: BytesPath, *paths: BytesPath) -> bytes:
    return os.path.join(__path, *paths)


def json_dumps(data, indent=4, ensure_ascii: bool = False, sort_keys=False, separators: tuple = None):
    """
    @summary: 序列化json
    ---------
    @param data: json格式的字符串或json对象
    @param indent: 格式化的缩进长度
    @param sort_keys: 是否排序
    @param ensure_ascii: 是否转为ascii编码
    @param separators: 是否转为最紧凑的json格式
    ---------
    @result: 格式化后的字符串
    """

    if isinstance(data, str):
        return data
    else:
        if not indent:
            separators = (',', ':')

        data = json.dumps(
            data,
            ensure_ascii=ensure_ascii,
            indent=indent,
            skipkeys=True,
            separators=separators,
            sort_keys=sort_keys,
            default=str,
        )
    return data


def json_loads(obj) -> Union[dict, list]:
    if isinstance(obj, (dict, list)):
        return obj

    return json.loads(obj)


def jsonp_to_json(jsonp):
    """jsonp转字典"""
    """ 方法一 """
    # start_index = jsonp.index('(') + 1
    # end_index = jsonp.rindex(')')
    # # callback_name = jsonp[:start_index - 1]
    # data_str = jsonp[start_index:end_index]
    # return json_loads(data_str)

    """ 方法二 """
    result = ''.join(re.findall(r'\w+[(](.*)[)]', jsonp, re.S))
    return json_loads(result)


def key2underline(key: str, strict=True):
    """
    >>> key2underline("HelloWord")
    'hello_word'
    >>> key2underline("SHData", strict=True)
    's_h_data'
    >>> key2underline("SHData", strict=False)
    'sh_data'
    >>> key2underline("SHDataHi", strict=False)
    'sh_data_hi'
    >>> key2underline("SHDataHi", strict=True)
    's_h_data_hi'
    >>> key2underline("dataHi", strict=True)
    'data_hi'
    """
    regex = "[A-Z]*" if not strict else "[A-Z]"
    capitals = re.findall(regex, key)

    if capitals:
        for capital in capitals:
            if not capital:
                continue
            if key.startswith(capital):
                if len(capital) > 1:
                    key = key.replace(
                        capital, capital[:-1].lower() + "_" + capital[-1].lower(), 1
                    )
                else:
                    key = key.replace(capital, capital.lower(), 1)
            else:
                if len(capital) > 1:
                    key = key.replace(capital, "_" + capital.lower() + "_", 1)
                else:
                    key = key.replace(capital, "_" + capital.lower(), 1)

    return key.strip("_")


def list2str(datas):
    """
    列表转字符串
    :param datas: [1, 2]
    :return: (1, 2)
    """
    data_str = str(tuple(datas))
    data_str = re.sub(r",\)$", ")", data_str)
    return data_str


def mkdir(path) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


def print_parent_caller(level: int = 1, types: bool = False):
    """
    打印函数父级调用者的装饰器
    Arg:
        level: 打印父级调用者 level=1, 打印祖父级调用者 level=2
        types:
    """

    def _print_parent_caller(func):
        def wrapper(*args, **kwargs):
            if types:
                frames = inspect.getouterframes(inspect.currentframe(), 2)
                if len(frames) > level:
                    parent_frame = frames[level]  # 直属父级调用者帧对象
                    parent_name = parent_frame[3]  # 直属父级调用者函数名
                    parent_line = parent_frame[2]  # 直属父级调用者行号
                    parent_file = parent_frame[1]  # 直属父级调用者文件路径
                    logger.info(f"File: {parent_file}, Line: {parent_line}, Function: {parent_name}")
                else:
                    logger.info("No parent caller found.")
            else:
                stack = traceback.extract_stack()
                for frame in stack[:-1]:
                    frame_file, frame_line, frame_func, _ = frame
                    logger.info(f"File: {frame_file}, Line: {frame_line}, Function: {frame_func}")

            return func(*args, **kwargs)

        return wrapper

    return _print_parent_caller


def path_exists(_path: str) -> bool:
    return os.path.exists(_path)


def random_choices(datas: list, limit: int = 3) -> list:
    """ 随机从列表中取值 """
    return random.choices(datas, k=limit)


def random_random():
    return random.random()


def remove_temp_file(path) -> None:
    """ 删除临时文件 """
    os.remove(path)


def retry(retry_times=3, interval=0, tag=False):
    """
    普通函数的重试装饰器
    Args:
        retry_times: 重试次数
        interval: 每次重试之间的间隔
        tag: 自定义的异常返回值
    Returns:

    """

    def _retry(func):
        @functools.wraps(func)  # 将函数的原来属性付给新函数
        def wapper(*args, **kwargs):
            for i in range(retry_times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(
                        "函数 {} 执行失败 重试 {} 次. error {}".format(func.__name__, i, e)
                    )
                    time.sleep(interval)
                    if i >= retry_times:
                        return tag

        return wapper

    return _retry


def rsa_encrypt(key: str, data: str):
    public_key = RSA.import_key(base64.b64decode(key))
    rsa = PKCS1_v1_5.new(public_key)
    encrypt_msg = rsa.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypt_msg).decode()


def shuffle_str(s):
    """ 随机打乱字符串顺序 """
    str_list = list(s)
    # 调用random模块的shuffle函数打乱列表
    shuffle(str_list)
    return ''.join(str_list)


def str2datetime(date_str: str, _format: Union[str, DateFormat] = DateFormat.Y_M_D) -> datetime.datetime:
    """ 字符串格式化为datetime类型 """
    return datetime.datetime.strptime(date_str, _format)


def timestamp_to_date(timestamp, time_format="%Y-%m-%d %H:%M:%S"):
    """
    @summary:
    ---------
    @param timestamp: 将时间戳转化为日期
    @param time_format: 日期格式
    ---------
    @result: 返回日期
    """
    if timestamp is None:
        raise ValueError("timestamp is null")

    date = time.localtime(timestamp)
    return time.strftime(time_format, date)


def url_quote(urls, plus: bool = False):
    """url编码"""
    if plus:
        return parse.quote_plus(urls)

    return parse.quote(urls)


def url_unquote(urls):
    """url解码"""
    return parse.unquote(urls)


def url_encode(url: str, params: dict):
    query_string = parse.urlencode(params)
    full_url = url + '?' + query_string
    return full_url


def with_save(file_path, content, mode="wb", encoding="utf-8") -> bool:
    try:
        if 'b' in mode:
            encoding = None

        if isinstance(content, str):
            mode = "w"

        if isinstance(content, (list, dict)):
            mode = 'w'
            content = json_dumps(content, indent=0)

        with open(file_path, mode, encoding=encoding) as fp:
            fp.write(content)
    except Exception as e:
        logger.error(e)
        return False
    else:
        logger.success(f"{file_path} 保存成功")
        return True


def with_open(file_path, mode="r", encoding="UTF-8", ignore: bool = False) -> AnyStr:
    if 'b' in mode:  # 二进制文件不允许编码
        encoding = None

    with open(file_path, mode=mode, encoding=encoding) as fp:
        file = fp.read()

    if ignore:
        return file.encode('gb2312', 'ignore').decode('gb2312')
    else:
        return file


def Unix_current_timestamp():
    return int(dt.utcnow().timestamp())