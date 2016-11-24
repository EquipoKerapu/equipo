from django.shortcuts import render
from .models import *
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView
from forms import CourseForm
from django.http import HttpResponse
from students.forms import get_course_string, RankForm
from django.forms.formsets import formset_factory
from django.shortcuts import redirect 
from equipo.utils import *

def question_answer_mapping(pcm, scm):
    student_answers = []
    if pcm.config is not None:
        for question in pcm.config.questions.all():
            answer = {
                'question': question,
                'answer': None
            }
            for option in question.question_options.all():
                if option in scm.options.all():
                    answer['answer'] = option
            student_answers.append(answer)
    return student_answers  

def questions_answered(student_answers):
    answered = True
    for answer in student_answers:
        if answer['answer'] is None:
            answered = False
            break
    return answered

class StudentCourseDetailView(TemplateView):
    template_name = 'student_course_detail.html'
    context_object_name = 'student_course_detail'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentCourseDetailView, self).get_context_data(*args, **kwargs)
        scm = self.course_mapping()
        pcm = ProfessorCourseMapping.objects.select_related(
            'professor', 'course', 'config').get(course=scm.course)
        student_answers = question_answer_mapping(pcm, scm)
        context['student_answers'] = student_answers
        session = self.request.session
        session['course'] = scm.course.id
        context['course'] = scm.course.id
        return context

    def course_mapping(self):
        pk = self.kwargs['pk']
        course_pk = self.kwargs['course_pk']
        return StudentCourseMapping.objects.select_related(
            'course', 'student').prefetch_related(
            'options').get(
            course=course_pk, student=pk)


class StudentCourseListView(FormView):
    template_name = 'student_course_list.html'
    context_object_name = 'student_course_list'
    form_class = CourseForm
    success_url = 'student-course-list'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            user = SiteUser.objects.get(user=request.user)
            course = form.cleaned_data['course_choice']
            StudentCourseMapping.objects.create(student=user, course=course)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        

    def get(self, request, *args, **kwargs):
        context = super(StudentCourseListView, self).get_context_data(**kwargs)
        return super(StudentCourseListView, self).get(request, *args, **kwargs)

    def get_courses(self, site_user):
        return Course.objects.filter(
            id__in=site_user.student_courses.select_related(
            'course').prefetch_related(
            'student_mappings', 'professor_mapping').values_list('course', flat=True))

    def get_context_data(self, *args, **kwargs):
        context = super(StudentCourseListView, self).get_context_data(*args, **kwargs)
        site_user = self.request.user.site_user

        courses = self.get_courses(site_user)
        course_list = []
        for course in courses:
            course_map = {
                        'course_title': '{0}: {1}'
                            .format(course.course_number, course.course_title),
                        'course_quarter': course.course_quarter,
                        'course_year': course.course_year,
                        'course_id': course.id
                    }
            pcm = ProfessorCourseMapping.objects.select_related(
                'professor', 'config').get(course=course)
            scm = course.student_mappings.prefetch_related('options').get(student=site_user)
            
            course_map['professor'] = pcm.professor

            student_answers = question_answer_mapping(pcm, scm)
            answered = questions_answered(student_answers)

            course_map['answered'] = answered
            course_map['rank'] = scm.rank

            course_list.append(course_map)
        context['course_list'] = course_list

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        student_courses = StudentCourseMapping.objects.filter(
            student=SiteUser.objects.get(
            user=self.request.user)).values_list(
            'course', flat=True)
        other_courses = Course.objects.exclude(id__in=student_courses)
        choices = []
        for course in other_courses:
            choices.append((course.id, get_course_string(course)))
        form.fields['course_choice'].queryset = other_courses
        context['form'] = form
   
        return context

    def student(self):
        return SiteUser.objects.get(pk=self.kwargs['pk'])


class ProfessorCourseDetailView(DetailView):
    template_name = 'professor_course_detail.html'
    context_object_name = 'professor_course_detail'

    def get_object(self):
        pk = self.kwargs['pk']
        course_pk = self.kwargs['course_pk']
        return ProfessorCourseMapping.objects.select_related(
            'professor', 'course', 'config').get(
            course=course_pk, professor=pk).course

    def students(self):
        course_pk = self.kwargs['course_pk']
        return StudentCourseMapping.objects.select_related(
            'course', 'student').prefetch_related(
            'options').filter(course=course_pk)

    def post(self, request, *args, **kwargs):
        course_pk = self.kwargs['course_pk']
        professor_pk = self.kwargs['pk']
        print request.POST
        if 'form-type' in request.POST and request.POST['form-type'] == 'form':
            print "in post"
            form = RankForm(request.POST)
            if form.is_valid():

                scms = self.students()
                pcm = scms[0].course.professor_mapping
                ranked = rank_students(scms, pcm)
                size = form.cleaned_data['average_group_size']
                groups = group_students(size, ranked)
                for index, group in enumerate(groups):
                    for student in group:
                        student.group = index + 1
                        student.save()


        return redirect('professor-course-detail', pk=professor_pk, course_pk=course_pk)



    def get_context_data(self, *args, **kwargs):
        context = super(ProfessorCourseDetailView, self).get_context_data(*args, **kwargs)
        form = RankForm(self.request.POST or None)
        context['form'] = form
        pcm = self.course_mapping()
        scms = self.students()
        course_students = []
        for scm in scms:
            student_answers = question_answer_mapping(pcm, scm)
            student = {}
            student['username'] = scm.student.user.username
            student['rank'] = scm.rank
            student['group'] = scm.group
            student['answers'] = student_answers
            student['all_questions_answered'] = questions_answered(student_answers)
            course_students.append(student)
        context['course_students'] = sorted(course_students, key=lambda k: k['group'])
        return context

    def course_mapping(self):
        pk = self.kwargs['pk']
        course_pk = self.kwargs['course_pk']
        return ProfessorCourseMapping.objects.select_related(
            'professor', 'course', 'config').get(
            course=course_pk, professor=pk)

class ProfessorCourseListView(ListView):
    template_name = 'professor_course_list.html'
    context_object_name = 'professor_course_list'

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Course.objects.filter(id__in=ProfessorCourseMapping.objects.filter(professor=pk).values_list('course'))

    def professor(self):
        return SiteUser.objects.get(pk=self.kwargs['pk'])

