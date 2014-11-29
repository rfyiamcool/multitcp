#coding:utf-8
import datetime
"""
时间戳
"""

def to_int(num):
    try:
        return int(num)
    except:
        return 0


def msgpk_decode_datetime(obj):
    if b'__datetime__' in obj:
        obj = datetime.datetime.strptime(obj["as_str"], "%Y-%m-%dT%H:%M:%S.%f")
    return obj


def msgpk_encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return {'__datetime__': True, 'as_str': obj.strftime("%Y-%m-%dT%H:%M:%S.%f")}
    return obj
