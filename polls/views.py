from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Question
# Create your views here.


def index(request):
    last_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
        'last_question_list': last_question_list,
    })
    return HttpResponse(template.render(context))


def index2(request):
    last_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'last_question_list': last_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
