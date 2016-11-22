
from django.conf.urls import url, include
from django.contrib import admin
from equipo import views

from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^courses/', include('courses.urls')),
    url(r'^users/', include('students.urls')),
    url(r'^questions/', include('questions.urls')),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^', views.HomeView.as_view(), name='home')
]

admin.site.site_header = 'Equipo Administration'
