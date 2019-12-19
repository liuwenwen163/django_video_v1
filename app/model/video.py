# encoding: utf-8
from django.db import models
from .enums import VideoType, FromType, NationalityType

__author__ = 'bbw'


class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=20, null=False, default=FromType.custom.value)
    nationality = models.CharField(max_length=20, default=NationalityType.other.value)
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        """联合索引，保证字段不会重复"""
        unique_together = ('name', 'video_type', 'from_to', 'nationality')

    def __str__(self):
        return 'video name:{}'.format(self.name)


class VideoStar(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_star',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')  # 演员身份

    class Meta:
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return 'video_star:{}, video_name{}'.format(self.name, self.video.name)


class VideoSub(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)  # 集数

    class Meta:
        """联合索引"""
        unique_together = ('video', 'number')

    def __str__(self):
        return 'video:{}, number:{}'.format(self.video.name, self.number)

