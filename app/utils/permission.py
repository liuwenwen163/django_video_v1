# encoding: utf-8
import functools

from django.shortcuts import redirect
from django.urls import reverse

__author__ = 'bbw'


def dashboard_auth(func):
    """自定义装饰器验证用户是否登录，是否为管理员账户"""

    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        """两个可变参数，用来接收get函数传过来的可变参数"""
        user = request.user
        if not user.is_authenticated or not user.is_superuser:
            return redirect('{}?to={}'.format(reverse('dashboard_login'), request.path))

        return func(self, request, *args, **kwargs)

    return wrapper

