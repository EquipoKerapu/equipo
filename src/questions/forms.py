from django import forms
from questions.models import Question

def get_options(question):
	choices = []
	options = question.question_options.all()
	for option in options:
		choices.append((option.id, option.option))
	return tuple(choices)


class AnswerForm(forms.Form):
	def __init__(self, *args, **kwargs):
		question = kwargs.pop('question')
		super(AnswerForm, self).__init__(*args, **kwargs)
		self.fields['options'] = forms.ChoiceField(label=question.question_text, choices=get_options(question), widget=forms.Select(attrs={'class': 'form-control'}))

class QuestionForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = ['question_text',]