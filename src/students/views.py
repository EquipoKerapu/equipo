from django.shortcuts import render
from .models import *
from django.views.generic import DetailView, ListView
# Create your views here.


class StudentCourseDetailView(DetailView):
	template_name = 'student_course_detail.html'
	context_object_name = 'student_course_detail'

	def get_object(self):
		pk = self.kwargs['pk']
		course_pk = self.kwargs['course_pk']
		return StudentCourseMapping.objects.get(course=course_pk, student=pk).course

	def get_context_data(self, *args, **kwargs):
		context = super(StudentCourseDetailView, self).get_context_data(*args, **kwargs)

		return context

class StudentCourseListView(ListView):
	template_name = 'student_course_list.html'
	context_object_name = 'student_course_list'

	def get_queryset(self):
		pk = self.kwargs['pk']
		return Course.objects.filter(id__in=StudentCourseMapping.objects.filter(student=pk).values_list('course'))

	def get_context_data(self, *args, **kwargs):
		context = super(StudentCourseListView, self).get_context_data(*args, **kwargs)
		courses = self.get_queryset()
		course_list = []
		for course in courses:
			course_map = {
						'course_title': '{0}: {1}'
							.format(course.course_number, course.course_title),
						'course_quarter': course.course_quarter,
						'course_id': course.id
					}
			pcm = ProfessorCourseMapping.objects.get(course=course)
			scm = self.student_mapping()
			course_map['professor'] = pcm.professor

			questions = pcm.questions.all()
			student_options = scm.options.all()

			answered = True

			for question in questions:
				for option in question.question_options.all():
					if option not in student_options:
						answered = False
						break
				if answered == False:
					break
			course_map['answered'] = answered
			course_map['rank'] = scm.rank

			course_list.append(course_map)
		context['course_list'] = course_list
		return context

	def student_mapping(self):
		return StudentCourseMapping.objects.get(student=SiteUser.objects.get(pk=self.kwargs['pk']))


class ProfessorCourseDetailView(DetailView):
	template_name = 'professor_course_detail.html'
	context_object_name = 'professor_course_detail'

	def get_object(self):
		pk = self.kwargs['pk']
		course_pk = self.kwargs['course_pk']
		return ProfessorCourseMapping.objects.get(course=course_pk, professor=pk).course

	def students(self):
		course_pk = self.kwargs['course_pk']
		return StudentCourseMapping.objects.filter(course=course_pk)

	def get_context_data(self, *args, **kwargs):
		context = super(ProfessorCourseDetailView, self).get_context_data(*args, **kwargs)
		
		course_mapping = self.course_mapping()
		student_mappings = self.students()
		course_students = []
		for student_mapping in student_mappings:
			student_answers = []
			for question in course_mapping.questions.all():
				answer = {
					'question': question,
					'answer': None
				}
				for option in question.question_options.all():
					if option in student_mapping.options.all():
						answer['answer'] = option
				student_answers.append(answer)
			student = {}
			student['username'] = student_mapping.student.user.username
			student['rank'] = student_mapping.rank
			student['answers'] = student_answers
			student['all_questions_answered'] = student_mapping.all_questions_answered
			course_students.append(student)
		context['course_students'] = course_students
		return context

	def course_mapping(self):
		pk = self.kwargs['pk']
		course_pk = self.kwargs['course_pk']
		return ProfessorCourseMapping.objects.get(course=course_pk, professor=pk)

class ProfessorCourseListView(ListView):
	template_name = 'professor_course_list.html'
	context_object_name = 'professor_course_list'

	def get_queryset(self):
		pk = self.kwargs['pk']
		return Course.objects.filter(id__in=ProfessorCourseMapping.objects.filter(professor=pk).values_list('course'))

	def professor(self):
		return SiteUser.objects.get(pk=self.kwargs['pk'])

