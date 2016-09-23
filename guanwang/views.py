from django.shortcuts import render
from django.views import generic
from .models import *
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'guanwang/index.html'

    def get_queryset(self):
        menus_list = MenuItem.objects.all()
        slide_image_item = SliderImage.objects.all()
        return {'menus_list': menus_list, 'slide_image_item': slide_image_item}


class MenuView(generic.ListView):
    model = Menus
    template_name = 'guanwang/head.html'



# class SliderImageView(generic.DetailView):
#     model = SliderImage
#     context_object_name = 'slider_image'
#     template_name = 'guanwang/menu.html'

