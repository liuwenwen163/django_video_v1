# encoding: utf-8
"""该模型文件是普通用户认证的数据模型"""
import hashlib

from django.db import models

__author__ = 'bbw'


class ClientUser(models.Model):
    """网站普通用户的数据模型"""
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    avatar = models.CharField(max_length=500, default='')
    gender = models.CharField(max_length=1, default='')
    birthday = models.DateField(null=True, blank=True, default=None)
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Username:{}'.format(self.username)

    @classmethod
    def add(cls, username, password, avatar='', gender='', birthday=None):
        return cls.objects.create(
            username=username,
            password=cls.hash_passwrod(password),
            avatar=avatar,
            gender=gender,
            birthday=birthday,
            status=True
        )

    @classmethod
    def get_user(cls, username, password):
        """尝试根据用户传入的用户名和密码获取用户"""
        try:
            user = cls.objects.get(
                username=username,
                password=cls.hash_password(password)
            )
            return user
        except:
            return None

    def update_password(self, old_password, new_password):
        """更新用户的密码"""
        hash_old_password = self.hash_passwrd(old_password)
        if hash_old_password != self.password:
            return False

        hash_new_password = self.hash_password(new_password)
        self.password = hash_new_password
        self.save()
        return True

    def update_stats(self):
        """更新用户的可用状态"""
        self.status = not self.status
        self.save()
        return True

    @staticmethod
    def hash_passwrd(password):
        """静态方法，加密明文密码"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        return hashlib.md5(password).hexdigest().upper()

