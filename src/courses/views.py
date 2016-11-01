from django.shortcuts import render
from .models import *
from django.views.generic import DetailView, ListView
# Create your views here.
from students import models as user_models


class CourseDetailView(DetailView):
	template_name = 'course_detail.html'
	context_object_name = 'course_detail'
	queryset = Course.objects.all()

	def students(self):
		"""
		Returns the students (mapping) in this course
		"""
		pk = self.kwargs['pk']
		return user_models.StudentCourseMapping.objects.filter(course=pk)

	def professor(self):
		"""
		Returns the professor (mapping) of this ourse 
		"""
		pk = self.kwargs['pk']
		return user_models.ProfessorCourseMapping.objects.get(course=pk)

	#def get_queryset(self):



class CourseListView(ListView):
	template_name = 'student_list.html'
	context_object_name = 'course_list'
	queryset = Course.objects.all()


