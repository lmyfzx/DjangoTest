from django.shortcuts import render
from django.views import generic
from .models import *
# Create your views here.


class MenuView(generic.ListView):
    model = Menus
    context_object_name = 'slug'
    template_name = 'guanwang/menu.html'


