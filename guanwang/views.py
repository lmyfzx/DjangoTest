from django.shortcuts import render
from django.views import generic
from .models import *
# Create your views here.


class MenuView(generic.ListView):
    model = Menus

    template_name = 'guanwang/menu.html'


