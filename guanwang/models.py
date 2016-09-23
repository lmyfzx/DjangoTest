from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType


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
    name = models.CharField(verbose_name='导航名', max_length=20, help_text='在页面显示的导航名，建议需要有一个“首页”的导航。')
    base_url = models.CharField(verbose_name='导航Url', max_length=20, help_text='导航Url', null=True, blank=True)
    slug = models.SlugField(verbose_name='导航别名', null=True, blank=True)
    status = models.BooleanField(verbose_name='是否启用', help_text='编辑确定是否启用该导航')
    # is_top = models.BooleanField(verbose_name='是否一级', help_text='选中表明为一级导航，否则为二级导航！', default=0)

    class Meta:
        verbose_name = '导航菜单'
        verbose_name_plural = '导航菜单'

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


class SliderImageCategory(models.Model):

    name = models.CharField(verbose_name=' 分类名称', max_length=128)
    slug = models.SlugField(verbose_name='分类别名', max_length=128)

    class Meta:
        verbose_name = '图片分类'
        verbose_name_plural = '图片分类'

    def __str__(self):
        return self.name


class SliderImage(models.Model):
    title = models.CharField(max_length=256, verbose_name='图片标题')
    description = models.CharField(max_length=512, verbose_name='图片描述', blank=True, )
    link_text = models.CharField(max_length=512, verbose_name='链接文字', blank=True)
    category = models.ForeignKey(SliderImageCategory, verbose_name='类别', null=True, blank=True)
    # name = models.CharField(verbose_name='图片名称', max_length=20, )
    # link = models.URLField(verbose_name='图片链接地址')
    image = models.ImageField(verbose_name='上传图片', upload_to='image')
    position = models.PositiveIntegerField(verbose_name='图片位置')
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    external_url = models.CharField(verbose_name='外部URL', max_length=120, blank=True)
    text_position_top = models.IntegerField(verbose_name='顶部文字位置', blank=True, null=True)

    text_position_bottom = models.IntegerField(
        verbose_name='底部文字位置',
        blank=True, null=True,
    )

    text_position_left = models.IntegerField(
        verbose_name='左方文字位置',
        blank=True, null=True,
    )

    text_position_right = models.IntegerField(
        verbose_name='右方文字位置',
        blank=True, null=True,
    )

    is_published = models.BooleanField(
        verbose_name='已发布？',
        default=False,
    )

    def image_path(self):
        return self.image.path
    image_path.short_description = '图片路径'

    def get_item_url(self):
        """Returns the url of the connected item."""
        try:
            return self.content_object.get_absolute_url()
        except AttributeError:
            return self.external_url
    get_item_url.short_description = '图片URL'

    class Meta:
        verbose_name = '图片管理'
        verbose_name_plural = '图片管理'

    def __str__(self):
        return self.title


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
