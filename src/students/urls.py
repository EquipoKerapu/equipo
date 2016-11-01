from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^students/(?P<pk>\d+)/courses/?$', StudentCourseListView.as_view(), name='student-course-list'),
    url(r'^students/(?P<pk>\d+)/courses/(?P<course_pk>\d+)/?$', StudentCourseDetailView.as_view(), name='student-course-detail'),
    url(r'^professors/(?P<pk>\d+)/courses/?$', ProfessorCourseListView.as_view(), name='professor-course-list'),
    url(r'^professors/(?P<pk>\d+)/courses/(?P<course_pk>\d+)/?$', ProfessorCourseDetailView.as_view(), name='professor-course-detail'),
]
