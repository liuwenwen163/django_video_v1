# encoding: utf-8
from django.views.generic import View
from django.views.generic import View
from app.libs.base_render import render_to_response

__author__ = 'bbw'


class Base(View):
    TEMPLATE = 'dashboard/nav.html'
    
    def get(self, request):

        return render_to_response(request, self.TEMPLATE)
