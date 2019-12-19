# encoding: utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth

__author__ = 'bbw'


class Login(View):
    """/dashboard/login"""
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))

        data = {'error': ''}

        # 设置跳转参数，如果有跳转参数就按照参数跳转
        to = request.GET.get('to', '')
        data['to'] = to

        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        data = {}
        # print(username, password)
        exists = User.objects.filter(username=username).exists()

        if not exists:
            data['error'] = '不存在该用户'
            return render_to_response(request, self.TEMPLATE, data=data)

        user = authenticate(username=username, password=password)
        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data=data)

        if not user.is_superuser:
            data['error'] = '您无权登录'
            return render_to_response(request, self.TEMPLATE, data=data)

        login(request, user)

        # 如果url中有to参数，就跳转到目标to参数的链接
        to = request.GET.get('to', '')
        if to:
            return redirect(to)

        return redirect('dashboard_index')


class Logout(View):
    """用户注销的视图函数逻辑"""
    def get(self, request):
        logout(request)
        return redirect(reverse('dashboard_login'))


class AdminManager(View):
    """
    /dashboard/admin/manager
    dashboard页面管理用户的视图逻辑
    """
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        users = User.objects.filter()

        page = request.GET.get('page', 1)
        p = Paginator(users, 3)  # 实例化分页器对象，第一个参数是对象列表，第二个参数是每页的数据量
        total_page = p.num_pages

        if int(page) <= 1:
            page = 1

        # 通过get_page获取对应的page页面，通过object_list拿到对应的显示数据
        current_page = p.get_page(int(page)).object_list

        data = {'users': current_page, 'total': total_page, 'page_num': int(page)}
        return render_to_response(request, self.TEMPLATE, data=data)


class UpdateAdminStatus(View):
    def get(self, request):
        status = request.GET.get('status', 'on')
        id = request.GET.get('id')

        _status = True if status == 'on' else False
        user = User.objects.get(id=id)
        user.is_superuser = _status
        user.save()

        return redirect(reverse('admin_manager'))




