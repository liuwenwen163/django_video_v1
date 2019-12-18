# encoding: utf-8

__author__ = 'bbw'

from django.urls import path, include
from .views.base import Base

urlpatterns = [
    path('base', Base.as_view())
]
