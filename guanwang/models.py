from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField, RichTextUploadingFormField

class Category(models.Model):
    name = models.CharField(verbose_name='文章类别', max_length=40)
    alias = models.CharField(verbose_name='类别别名', max_length=40, blank=True)

    class Meta:
        verbose_name = '文章类别'
        verbose_name_plural = '文章类别'

    def __str__(self):
        return self.name


class Slug(models.Model):
    name = models.SlugField(verbose_name='文章别名')

    class Meta:
        verbose_name = '文章别名'
        verbose_name_plural = '文章别名'

    def __str__(self):
        return self.name


# Create your models here.
class Menus(models.Model):
    # parentId = models.IntegerField(verbose_name='导航ID', help_text='顶级Id为0')
    position = models.IntegerField(verbose_name='导航位置', help_text='数字越少越靠前')
    code = models.ForeignKey(Category,verbose_name='导航类别', help_text='导航那个类别的文章')
    name = models.CharField(verbose_name='导航名', max_length=20, help_text='在页面显示的导航名')
    url = models.CharField(verbose_name='导航Url', max_length=20, help_text='导航Url')
    status = models.BooleanField(verbose_name='是否启用', help_text='编辑确定是否启用该导航')

    class Meta:
        verbose_name = '一级菜单'
        verbose_name_plural = '一级菜单'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class ChildMenus(Menus):
    child_parentId = models.ForeignKey(Menus, verbose_name="父导航ID", related_name='ChildMenus_childParentId')

    class Meta:
        verbose_name = '二级菜单'
        verbose_name_plural = '二级菜单'

    def __str__(self):
        return self.name


class BannerImage(models.Model):
    name = models.CharField(verbose_name='图片名称', max_length=20, )
    link = models.URLField(verbose_name='图片链接地址')
    image = models.ImageField(verbose_name='上传图片', upload_to='image')

    def imagePath(self):
        return self.image.path
    imagePath.short_description = '图片路径'

    class Meta:
        verbose_name = '首页Banner图片'
        verbose_name_plural= '首页Banner图片'


class NewsArtile(models.Model):
    menuid = models.ForeignKey(ChildMenus,verbose_name='导航栏目')
    title = models.CharField(verbose_name='标题', max_length=80)
    ctime = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    status = models.BooleanField(verbose_name='发布？', help_text='创建的文章是否在前台展示！')
    type = models.ForeignKey(Category, verbose_name='文章类别')
    slug = models.ForeignKey(Slug, verbose_name='文章别名', blank=True)
    position = models.IntegerField(verbose_name='文章排序', help_text='数字越少越靠前')
    isnew = models.BooleanField(verbose_name='新文章？', help_text='创建的文章是否显示new标志')
    headimg = models.ImageField(verbose_name='文章缩略图', upload_to='image')
    abstract = RichTextUploadingField(verbose_name='文章摘要', max_length=300, config_name='simple')
    content = RichTextUploadingField(verbose_name='文章内容')

    class Meta:
        verbose_name = '新建文章'
        verbose_name_plural = '新建文章'

    def __str__(self):
        return self.title
