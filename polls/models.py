from django.db import models
from django.utils import timezone
import datetime
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(verbose_name='问题描述', max_length=200)
    pub_date = models.DateTimeField(verbose_name='提交时间')


    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.short_description = '最新发布？'


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(verbose_name='选项', max_length=200)
    votes = models.IntegerField(verbose_name='票数', default=0)

    def __str__(self):
        return self.choice_text