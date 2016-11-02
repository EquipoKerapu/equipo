from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login

class LoginView(FormView):

	form_class = AuthenticationForm
	template_name = 'login_form.html'

	def form_valid(self, form):
		login(self.request, form.get_user())

	def get_success_url(self):
		return 'users/professors/10/courses'

class HomeView(TemplateView):
	template_name = 'home.html'
