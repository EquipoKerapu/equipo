from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, View
from django.shortcuts import redirect 

from students.models import SiteUser

class HomeView(View):
    '''
    Redirects users based on whether they are a professor or student,
    or to admin if they are a superuser
    '''
    def get(self, request):
        print "in home get"
        user = self.request.user 
        print user
        if user.is_authenticated():
            try:
                user = SiteUser.objects.get(user=user)
                if user.is_professor:
                    return redirect("professor-course-list", pk=user.id)
                else:
                    return redirect("student-course-list", pk=user.id)
            except:
                if user.is_superuser:
                    return redirect("admin:index")

        return redirect("login")

class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/home/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login_form.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)