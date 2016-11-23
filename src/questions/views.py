from django.shortcuts import render
from .models import *
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView
from .forms import *
from django.shortcuts import redirect 
from students.models import *


class QuestionDetailView(TemplateView):
    template_name = 'answer_question.html'
    context_object_name = 'question_detail'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        form = context['form']
        if form.is_valid():
            return redirect("student-course-list", pk=request.user.id)
        else:
            pass #TODO

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(*args, **kwargs)
        question = Question.objects.get(id=kwargs['pk'])

        if self.request.method == 'POST':
            form = AnswerForm(self.request.POST, question=question)
            if form.is_valid():
                option_id = form.cleaned_data['options']
                course_id = self.request.session['course']
                student = SiteUser.objects.get(user=self.request.user)
                scm = StudentCourseMapping.objects.get(course=course_id, student=student)
                scm.options.add(option_id)
                scm.save()                
            else:
                #TODO
                print form.errors
            context['form'] = form

        if self.request.method == 'GET':
            form = AnswerForm(question=question)
            context['form'] = form

        return context
        
class QuestionListView(ListView):
    template_name = 'question_list.html'
    context_object_name = 'question_list'
    queryset = Question.objects.all()


