from django.shortcuts import render
from .models import *
from django.views.generic import DetailView, ListView
# Create your views here.


class StudentDetailView(DetailView):
	template_name = 'student_detail.html'
	context_object_name = 'student_detail'
	queryset = SiteUser.objects.filter(is_professor=False)

class StudentListView(ListView):
	template_name = 'student_list.html'
	context_object_name = 'student_list'
	queryset = SiteUser.objects.filter(is_professor=False)

