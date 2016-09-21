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


# class Slug(models.Model):
#     name = models.SlugField(verbose_name='文章别名')
#
#     class Meta:
#         verbose_name = '文章别名'
#         verbose_name_plural = '文章别名'
#
#     def __str__(self):
#         return self.name


# Create your models here.
class Menus(models.Model):
    # parentId = models.ForeignKey(verbose_name='导航ID', help_text='顶级Id为0', to='self', null=True, blank=True)
    position = models.IntegerField(verbose_name='导航位置', help_text='数字越少越靠前')
    # code = models.ForeignKey(Category,verbose_name='导航类别', help_text='导航那个类别的文章')
    name = models.CharField(verbose_name='导航名', max_length=20, help_text='在页面显示的导航名')
    base_url = models.CharField(verbose_name='导航Url', max_length=20, help_text='导航Url', null=True, blank=True)
    slug = models.SlugField(verbose_name='导航别名', null=True, blank=True)
    status = models.BooleanField(verbose_name='是否启用', help_text='编辑确定是否启用该导航')
    # is_top = models.BooleanField(verbose_name='是否一级', help_text='选中表明为一级导航，否则为二级导航！', default=0)

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = '菜单'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Re-order all items from 10 upwards, at intervals of 10.
        This makes it easy to insert new items in the middle of
        existing items without having to manually shuffle
        them all around.
        """
        super(Menus, self).save(*args, **kwargs)

        current = 10
        for item in MenuItem.objects.filter(menu=self).order_by('position'):
            item.position = current
            item.save()
            current += 10


class MenuItem(models.Model):
    menu = models.ForeignKey(to=Menus, verbose_name='菜单项')
    title = models.CharField(verbose_name='菜单项标题', max_length=100)
    position = models.IntegerField(verbose_name='菜单项位置', default=500)
    link_url = models.CharField(verbose_name='菜单项URL', max_length=100, help_text='内部Url或者外部Url')
    login_required = models.BooleanField(verbose_name='已登陆用户可见？', blank=True, help_text='是否仅对已登陆用户可见')
    anonymous_only = models.BooleanField(verbose_name='仅匿名用户可见?', blank=True, help_text='是否仅对匿名用户可见')

    class Meta:
        verbose_name = '菜单项'
        verbose_name_plural = '菜单项'

    def __str__(self):
        return self.title
# class ChildMenus(Menus):
#     child_parentId = models.ForeignKey(Menus, verbose_name="父导航ID", related_name='ChildMenus_childParentId')
#
#     class Meta:
#         verbose_name = '二级菜单'
#         verbose_name_plural = '二级菜单'
#
#     def __str__(self):
#         return self.name


class BannerImage(models.Model):
    name = models.CharField(verbose_name='图片名称', max_length=20, )
    link = models.URLField(verbose_name='图片链接地址')
    image = models.ImageField(verbose_name='上传图片', upload_to='image')

    def imagePath(self):
        return self.image.path
    imagePath.short_description = '图片路径'

    class Meta:
        verbose_name = '首页Banner图片'
        verbose_name_plural = '首页Banner图片'


class NewsArtile(models.Model):
    menuid = models.ForeignKey(MenuItem, verbose_name='导航栏目')
    title = models.CharField(verbose_name='标题', max_length=80)
    ctime = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    status = models.BooleanField(verbose_name='发布？', help_text='创建的文章是否在前台展示！')
    # type = models.ForeignKey(Category, verbose_name='文章类别')
    # slug = models.ForeignKey(Slug, verbose_name='文章别名', blank=True)
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
