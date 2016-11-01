from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^/?$', CourseListView.as_view(), name='course-list'),
    url(r'^(?P<pk>\d+)/?$', CourseDetailView.as_view(), name='course-detail'),
]