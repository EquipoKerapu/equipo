from django.shortcuts import render
from .models import *
from django.views.generic import DetailView, ListView
# Create your views here.


class QuestionDetailView(DetailView):
	template_name = 'question_detail.html'
	context_object_name = 'question_detail'
	queryset = Question.objects.all()

class QuestionListView(ListView):
	template_name = 'question_list.html'
	context_object_name = 'question_list'
	queryset = Question.objects.all()


