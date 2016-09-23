from django.conf.urls import url

from . import views


app_name = 'guanwang'
urlpatterns = [
    # url(r'^$', views, name='index'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^menu/$', views.MenuView.as_view(), name='menu'),
]
