from django.contrib import admin
from .models import Menus, BannerImage, NewsArtile, Category, MenuItem
# Register your models here.


# class MenuInline(admin.TabularInline):
#     model = ChildMenus
#     extra = 2


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    ordering = ('position',)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'slug', 'base_url', 'status')
    list_filter = ('status', )
    ordering = ('position', )
    inlines = [MenuItemInline, ]


class BannerImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'imagePath', 'image')


class NewsArtileAdmin(admin.ModelAdmin):
    list_filter = ('ctime',)
    list_display = ('title', 'ctime', 'status', 'abstract')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


# class SlugAdmin(admin.ModelAdmin):
#     list_display = ('name',)


# class ChildMenusAdmin(admin.ModelAdmin):
#     list_display = ('name', 'id', 'code', 'url', 'child_parentId', 'position', 'status')
#     list_filter = ('child_parentId', )
#     ordering = ('child_parentId', 'position', )

admin.site.register(Menus, MenuAdmin)
# admin.site.register(ChildMenus,ChildMenusAdmin)
admin.site.register(BannerImage,BannerImageAdmin)
admin.site.register(NewsArtile,NewsArtileAdmin)
admin.site.register(Category,CategoryAdmin)
# admin.site.register(Slug,SlugAdmin)