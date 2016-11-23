from django import forms
from courses.models import Course

def get_course_string(course):
	return "{0}: {1}, {2} {3}".format(course.course_number, course.course_title, course.course_quarter, course.course_year)

def get_choices():# TODO need to filter this based on student user so they can't do duplicates
	choices = []
	courses = Course.objects.all()
	for course in courses:
		choices.append((course.id, get_course_string(course)))
	return tuple(choices)

class CourseForm(forms.Form):
    #course_choice = forms.ChoiceField(label="", choices=get_choices(), widget=forms.Select(attrs={'class': 'form-control'})) 
    #course_choice = forms.ChoiceField(label="", choices=((1,'1')), widget=forms.Select(attrs={'class': 'form-control'})) 
    course_choice = forms.ModelChoiceField(label="", queryset=Course.objects.all(), widget=forms.Select(attrs={'class': 'form-control'})) 





