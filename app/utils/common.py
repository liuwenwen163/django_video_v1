# encoding: utf-8

__author__ = 'bbw'


def check_and_get_video_type(type_obj, type_value, message):
    """验证用户传入的视频类型，国籍，来源，是否是我们定义的枚举类型"""
    try:
        type_obj(type_value)
    except:
        return {'code': -1, 'msg': message}

    return {'code': 0, 'msg': 'success'}
